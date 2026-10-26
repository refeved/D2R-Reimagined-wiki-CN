#!/usr/bin/env python3
"""译文自查：结构校验 + 过期提示 + 翻译进度。

用法：
    python3 tools/check_i18n.py            # 全部检查
    python3 tools/check_i18n.py --only FAQ # 只看某个页面（子串匹配）

检查项：
    1. 孤儿页：zh/ 下有、上游英文没有对应页面
    2. 结构破坏：译文 HTML 的标签序列与英文原文不一致（翻译时误删/误加标签）
    3. 译文过期：英文原页的 frontmatter date 比译文新
    4. 翻译进度：逐目录统计已翻译 / 总页数

精确的上游增量比对靠 manifest.json，看 tools/sync.py。
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UPSTREAM = ROOT / "upstream"
ZH_DIR = ROOT / "zh"
PAGE_EXTS = {".md", ".html", ".htm"}
EXCLUDE_DIRS = {".git", ".idea", ".venv", "tools", "_site", "__pycache__", "node_modules"}
SKIP_STEMS = {"README"}

TAG_RE = re.compile(r"<\s*/?\s*([a-zA-Z][a-zA-Z0-9]*)")
SELF_CLOSING = {"br", "img", "hr", "input", "meta", "link", "wbr"}


def rel_pages(base: Path):
    """返回 {stem: path}，stem 是相对 base 的路径（去扩展名）。"""
    found = {}
    if not base.exists():
        return found
    for path in sorted(base.rglob("*")):
        if path.suffix.lower() not in PAGE_EXTS or not path.is_file():
            continue
        rel = path.relative_to(base)
        if any(part in EXCLUDE_DIRS or part.startswith(".") for part in rel.parts[:-1]):
            continue
        if rel.parts[0] in SKIP_STEMS:
            continue
        stem = rel.with_suffix("").as_posix()
        # 同一 stem 有 .md 和 .html 时，取 frontmatter date 较新的（与 build.py 一致）
        old = found.get(stem)
        if old is not None:
            old_date = frontmatter(old.read_text(encoding="utf-8", errors="replace")).get("date", "")
            new_date = frontmatter(path.read_text(encoding="utf-8", errors="replace")).get("date", "")
            if new_date < old_date or (new_date == old_date and old.suffix.lower() == ".html"):
                continue
        found[stem] = path
    return found


def strip_code(text: str) -> str:
    """去掉代码块/行内代码，避免把 <your user> 之类的占位符当成标签。"""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`\n]*`", " ", text)
    return text


def frontmatter(text: str):
    m = re.match(r"^\s*(?:---\r?\n(.*?)\r?\n---|<!--(.*?)-->)", text, re.S)
    if not m:
        return {}
    block = m.group(1) if m.group(1) is not None else m.group(2)
    meta = {}
    for line in block.splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
    return meta


def tag_signature(path: Path):
    text = strip_code(path.read_text(encoding="utf-8", errors="replace"))
    if path.suffix.lower() == ".md":
        # markdown 原文与译文都按源码比标签，主要用来抓误删的内联 HTML
        return TAG_RE.findall(text)
    body = text.split("-->", 1)[1] if text.lstrip().startswith("<!--") and "-->" in text else text
    return TAG_RE.findall(body)


def main():
    parser = argparse.ArgumentParser(description="译文自查")
    parser.add_argument("--only", default="", help="只检查名称包含该子串的页面")
    parser.add_argument("--content", help="英文原文目录（默认用 upstream/ submodule）")
    args = parser.parse_args()

    en_base = Path(args.content).resolve() if args.content else UPSTREAM
    if not en_base.is_dir():
        sys.exit("找不到英文原文目录：%s（先 git submodule update --init）" % en_base)
    en = rel_pages(en_base)
    zh = rel_pages(ZH_DIR)

    orphans = sorted(set(zh) - set(en))
    structure = []
    stale = []
    translated = []

    for stem, zh_path in sorted(zh.items()):
        if args.only and args.only.lower() not in stem.lower():
            continue
        en_path = en.get(stem)
        if not en_path:
            continue
        translated.append(stem)
        zh_meta, en_meta = frontmatter(zh_path.read_text(encoding="utf-8", errors="replace")), frontmatter(
            en_path.read_text(encoding="utf-8", errors="replace")
        )
        if zh_meta.get("date") and en_meta.get("date") and zh_meta["date"] < en_meta["date"]:
            stale.append((stem, en_meta["date"][:10], zh_meta["date"][:10]))
        if zh_path.suffix.lower() == en_path.suffix.lower():
            a, b = tag_signature(en_path), tag_signature(zh_path)
            if a != b:
                same = 0
                for x, y in zip(a, b):
                    if x != y:
                        break
                    same += 1
                structure.append((stem, len(a), len(b), same, a, b))
        elif zh_path.suffix.lower() != en_path.suffix.lower():
            print("提示：%s 的译文格式(%s)与原文(%s)不同，跳过结构校验"
                  % (stem, zh_path.suffix, en_path.suffix))

    print("=" * 60)
    print("翻译进度：%d / %d 页（%.0f%%）" % (len(translated), len(en), 100.0 * len(translated) / max(len(en), 1)))

    if orphans:
        print("\n[孤儿页] zh/ 下有、英文没有对应页面（%d）：" % len(orphans))
        for stem in orphans:
            print("  - " + stem)

    if structure:
        print("\n[结构异常] 译文标签序列与原文不一致（%d），请检查是否误删/误加标签：" % len(structure))
        for stem, na, nb, same, a, b in structure:
            print("  - %-52s 原文 %d 个标签 / 译文 %d 个，第 %d 个开始不同" % (stem, na, nb, same + 1))
            print("      原文: %s" % " ".join(a[max(0, same - 2):same + 4]))
            print("      译文: %s" % " ".join(b[max(0, same - 2):same + 4]))

    if stale:
        print("\n[译文过期] 英文页更新晚于译文（%d），建议复核：" % len(stale))
        for stem, en_date, zh_date in stale:
            print("  - %-52s 英文 %s / 译文 %s" % (stem, en_date, zh_date))

    if not (orphans or structure or stale):
        print("\n未发现问题。")

    # 目录维度进度
    stats = defaultdict(lambda: [0, 0])
    for stem in en:
        key = stem.split("/")[0] if "/" in stem else "(根目录)"
        stats[key][1] += 1
        if stem in zh:
            stats[key][0] += 1
    print("\n分目录进度：")
    for key in sorted(stats, key=lambda k: (-stats[k][1], k)):
        done, total = stats[key]
        print("  %-22s %3d / %3d" % (key, done, total))

    return 1 if (orphans or structure) else 0


if __name__ == "__main__":
    sys.exit(main())
