#!/usr/bin/env python3
"""上游增量追踪：只翻真正需要翻的页面。

原理：manifest.json 记录每篇译文「核对过的英文版本」——也就是该英文文件在
upstream submodule 里的 git blob 哈希，加上最后修改它的 commit。于是上游更新后
不必重读整篇原文，只看变更片段：

    待复核   上游改了英文页，译文需要跟着改（--diff 打印改了哪几段）
    未译     上游有、zh/ 还没有
    已同步   blob 一致，什么都不用做
    上游已删 / 游离译文   需要人工决定

用法：
    python3 tools/sync.py                       # 看报告
    python3 tools/sync.py --diff                # 待复核页附上英文侧变更片段
    python3 tools/sync.py --seed --base <ref>   # 首次建立 manifest（ref = 译文依据的上游版本）
    python3 tools/sync.py --accept home FAQ     # 确认这几篇已对齐当前上游
    python3 tools/sync.py --accept-all          # 所有已译页都标记为对齐
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UPSTREAM = ROOT / "upstream"
ZH_DIR = ROOT / "zh"
MANIFEST = ROOT / "manifest.json"

PAGE_EXTS = {".md", ".html", ".htm"}
EXCLUDE_DIRS = {".git", ".idea", ".venv", "tools", "_site", "__pycache__", "node_modules"}
SKIP_STEMS = {"README"}
UPSTREAM_URL = "https://github.com/D2R-Reimagined/wiki-content"


def git(repo, *args):
    """跑 git，失败返回 None（--content 指向非 git 目录时降级）。"""
    proc = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()


def blob_sha(path: Path):
    """算 git blob 哈希：sha1("blob <字节数>\\0" + 内容)，与 ls-tree/rev-parse 一致。"""
    data = path.read_bytes()
    head = b"blob %d\0" % len(data)
    return hashlib.sha1(head + data).hexdigest()


def frontmatter_date(path: Path):
    text = path.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^\s*(?:---\r?\n(.*?)\r?\n---|<!--(.*?)-->)", text, re.S)
    if not m:
        return ""
    block = m.group(1) if m.group(1) is not None else m.group(2)
    for line in block.splitlines():
        key, _, value = line.strip().partition(":")
        if key.strip() == "date":
            return value.strip()
    return ""


def keep_newer(cur: dict, new: dict):
    """同一 stem 同时有 .md 与 .html：取 date 新的，同日期优先 .html（与 build.py 一致）。"""
    if new["date"] > cur["date"]:
        return True
    return new["date"] == cur["date"] and new["path"].endswith((".html", ".htm"))


def walk(base: Path):
    """{stem: {"path": 绝对路径, "rel": 相对路径, "blob": git blob 哈希, "date": frontmatter date}}"""
    out = {}
    if not base.is_dir():
        return out
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = sorted(d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith("."))
        for name in sorted(filenames):
            if name.startswith("."):
                continue
            full = Path(dirpath) / name
            if full.suffix.lower() not in PAGE_EXTS:
                continue
            rel = full.relative_to(base)
            if rel.parts[0] in SKIP_STEMS:
                continue
            entry = {
                "path": str(full),
                "rel": rel.as_posix(),
                "blob": blob_sha(full),
                "date": frontmatter_date(full),
            }
            stem = rel.with_suffix("").as_posix()
            old = out.get(stem)
            if old is not None and not keep_newer(old, entry):
                continue
            out[stem] = entry
    return out


def last_commit(repo, ref, rel):
    """rel 在 ref 版本里最后一次被哪个 commit 改动（%H\t%ad）。"""
    return git(repo, "log", "-1", "--format=%H%x09%ad", "--date=short", ref, "--", rel)


def load_manifest():
    if not MANIFEST.exists():
        return None
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def save_manifest(data):
    MANIFEST.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def blank_record():
    return {"pages": {}}


# ---------------------------------------------------------------- 状态计算


def classify(up, zh, man):
    """返回 (已同步, 待复核, 未译, 上游已删, 游离译文)。"""
    synced, need_review, todo, gone, orphans = [], [], [], [], []
    pages = man.get("pages", {}) if man else {}

    for stem, cur in sorted(up.items()):
        rec = pages.get(stem)
        has_zh = stem in zh
        if has_zh:
            if rec is None:
                need_review.append((stem, cur, rec, "未记录（跑 --seed 或 --accept）"))
            elif rec["en_blob"] != cur["blob"]:
                need_review.append((stem, cur, rec, "上游已改"))
            else:
                synced.append((stem, cur, rec))
        elif rec is None:
            todo.append((stem, cur))
        else:
            need_review.append((stem, cur, rec, "译文缺失（被删了？）"))
    for stem in sorted(pages):
        if stem not in up:
            gone.append(stem)
    for stem in sorted(set(zh) - set(up)):
        orphans.append(stem)
    return synced, need_review, todo, gone, orphans


def show_diff(repo, rec, cur_rel, lines):
    """打印译文所依据的 commit 到当前 HEAD 之间，该文件的英文侧变更。"""
    base = (rec or {}).get("en_commit", "")
    if not base:
        if not (rec or {}).get("en_blob"):
            print("      （基线版本里还没有这个文件，等于整页新增）")
        else:
            print("      （没有基线 commit，无法出增量）")
        return
    diff = git(repo, "diff", "--unified=1", base, "HEAD", "--", cur_rel)
    if diff is None:
        print("      （基线 %s 不在本地历史里，git -C upstream fetch --unshallow 后重试）" % base[:9])
        return
    body = [l for l in diff.splitlines() if l.startswith(("@@", "+", "-")) and not l.startswith(("+++", "---"))]
    if not body:
        print("      （只有元数据变动）")
        return
    for line in body[:lines]:
        print("      " + line[:160])
    if len(body) > lines:
        print("      ... 其余 %d 行省略（--max-diff-lines 调整）" % (len(body) - lines))


def report(args):
    up_dir = Path(args.content).resolve() if args.content else UPSTREAM
    if not up_dir.is_dir():
        sys.exit("找不到 upstream/，先执行：git submodule update --init")
    en = walk(up_dir)
    zh = walk(ZH_DIR)
    man = load_manifest()
    head = git(up_dir, "rev-parse", "HEAD") or ""

    if man is None and not (args.seed or args.accept_all or args.accept):
        sys.exit("还没有 manifest.json，先建基线：\n  python3 tools/sync.py --seed --base <上游 commit>\n")

    man = man or blank_record()
    note = apply_action(args, man, up_dir, en, zh, head)
    if note:
        man = load_manifest() or blank_record()
    synced, need_review, todo, gone, orphans = classify(en, zh, man)

    print("上游 %s @ %s" % (up_dir.name, head[:9] or "（非 git 目录）"))
    print("总页数 %d · 译文 %d · 已同步 %d · 待复核 %d · 未译 %d"
          % (len(en), len(zh), len(synced), len(need_review), len(todo)))

    if need_review:
        print("\n[待复核] 英文侧已变，译文需要跟进（%d）：" % len(need_review))
        for stem, cur, rec, why in need_review:
            old_date = (rec or {}).get("en_date", "?")
            new_date = git(up_dir, "log", "-1", "--format=%ad", "--date=short", "HEAD", "--", cur["rel"]) or "?"
            print("  - %-40s %s  %s → %s" % (stem, why, old_date, new_date))
            if args.diff:
                show_diff(up_dir, rec, cur["rel"], args.max_diff_lines)
        if not args.diff:
            print("  （加 --diff 看具体改了哪几段）")

    if todo:
        print("\n[未译] 上游有、zh/ 没有（%d）：" % len(todo))
        groups = {}
        for stem, cur in todo:
            groups.setdefault(stem.split("/")[0] if "/" in stem else "(根目录)", []).append(stem)
        for key in sorted(groups, key=lambda k: (-len(groups[k]), k)):
            print("  %-22s %d 篇" % (key, len(groups[key])))
            for stem in groups[key][: args.list]:
                print("      " + stem)
            if len(groups[key]) > args.list:
                print("      ... 其余 %d 篇" % (len(groups[key]) - args.list))

    if gone:
        print("\n[上游已删] 译文可以一并删掉（%d）：%s" % (len(gone), "、".join(gone)))
    if orphans:
        print("\n[游离译文] zh/ 有、上游没有（%d）：%s" % (len(orphans), "、".join(orphans)))
    if note:
        print("\n" + note)
    return 0


def apply_action(args, man, up_dir, en, zh, head):
    """--seed / --accept 会重写 manifest，返回一行说明（没动作返回空串）。"""
    if args.seed:
        note = seed(man, up_dir, en, zh, args.base)
    elif args.accept_all or args.accept:
        wanted = sorted(zh) if args.accept_all else args.accept
        changed = 0
        for stem in wanted:
            if stem not in en:
                print("跳过 %s：上游没有这个页面" % stem)
                continue
            if stem not in zh:
                print("跳过 %s：zh/ 没有译文" % stem)
                continue
            changed += record(man, up_dir, en, zh, stem, "HEAD")
        note = "已把 %d 篇对齐到上游当前版本" % changed
    else:
        return ""
    man["upstream_url"] = UPSTREAM_URL
    man["head"] = head
    save_manifest(man)
    return note + "，manifest.json 已更新"


def record(man, up_dir, en, zh, stem, ref="HEAD"):
    """把 stem 的基线写成「上游 ref 版本的英文内容」。"""
    cur, zh_entry = en[stem], zh[stem]
    info = last_commit(up_dir, ref, cur["rel"])
    sha, date = (info.split("\t") + ["", ""])[:2] if info else ("", "")
    man["pages"][stem] = {
        "en_path": cur["rel"],
        "en_blob": cur["blob"],
        "en_commit": sha,
        "en_date": date,
        "zh_path": zh_entry["rel"],
        "zh_blob": zh_entry["blob"],
        "synced_at": datetime.date.today().isoformat(),
    }
    return 1


def seed(man, up_dir, en, zh, base):
    """首次建基线：以 base 为准，base 之后改过的已译页直接标成待复核。"""
    if not base:
        sys.exit("--seed 需要 --base <ref>，即译文依据的上游 commit")
    if git(up_dir, "rev-parse", "--verify", base + "^{commit}") is None:
        sys.exit("upstream 里没有 %s，先 git -C upstream fetch" % base)
    done = reviewed = 0
    for stem in sorted(zh):
        if stem not in en:
            continue
        rel = en[stem]["rel"]
        base_blob = git(up_dir, "rev-parse", "%s:%s" % (base, rel))
        if base_blob and base_blob == en[stem]["blob"]:
            record(man, up_dir, en, zh, stem, base)
            done += 1
        else:
            record(man, up_dir, en, zh, stem, base)           # 基线停在旧版本
            man["pages"][stem]["en_blob"] = base_blob or ""    # 记录旧 blob，于是 report 判定待复核
            reviewed += 1
    man["upstream_url"] = UPSTREAM_URL
    man["base_seed"] = git(up_dir, "rev-parse", base) or base
    return "已建立基线：%d 篇已同步，%d 篇标为待复核" % (done, reviewed)


def main():
    parser = argparse.ArgumentParser(description="上游增量追踪")
    parser.add_argument("--content", help="英文原文目录（默认用 upstream/ submodule）")
    parser.add_argument("--diff", action="store_true", help="待复核页附上英文侧变更片段")
    parser.add_argument("--max-diff-lines", type=int, default=40, help="每页最多打印多少行 diff")
    parser.add_argument("--list", type=int, default=8, help="每个目录最多列出多少篇未译")
    parser.add_argument("--seed", action="store_true", help="首次建立 manifest")
    parser.add_argument("--base", default="", help="--seed 时译文依据的上游 commit")
    parser.add_argument("--accept", nargs="+", metavar="STEM", help="把这些页对齐到上游当前版本")
    parser.add_argument("--accept-all", action="store_true", help="所有已译页都对齐到上游当前版本")
    return report(parser.parse_args())


if __name__ == "__main__":
    sys.exit(main())
