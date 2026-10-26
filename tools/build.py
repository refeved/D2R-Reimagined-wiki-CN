#!/usr/bin/env python3
"""把 Wiki.js 内容渲染成本地可浏览的静态站点（en / zh 双语）。

仓库布局（英文只读、译文可写）：
    upstream/   git submodule -> https://github.com/D2R-Reimagined/wiki-content
                英文页面 + 图片等资源，本仓库不改它一个字
    zh/         中文译文，路径与上游英文页保持一致（含大小写与 .md/.html 格式）——
                这正是 Wiki.js 2.x Git 存储对非默认语言的存放约定，
                将来要回流官方只需把 zh/ 整个拷进上游
    _site/      构建产物，en/ 与 zh/ 两棵树，URL 与线上对齐

用法：
    tools/build.sh                # 构建到 _site/
    tools/build.sh --serve        # 构建并启动 http://127.0.0.1:8787
    tools/build.sh --strict       # 存在未解析链接等问题时以非 0 退出
    tools/build.sh --content /path/to/wiki-content   # 不用 submodule 时手动指定英文源
"""

from __future__ import annotations

import argparse
import functools
import html as html_mod
import http.server
import json
import os
import posixpath
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit

try:
    import markdown
except ImportError:  # pragma: no cover
    sys.exit("缺少依赖 markdown，请改用 tools/build.sh 运行（会自动创建 .venv）")

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_site"
THEME = Path(__file__).resolve().parent / "theme"
UPSTREAM = ROOT / "upstream"   # 英文原文（submodule，只读）
ZH_DIR = ROOT / "zh"           # 中文译文（本仓库，可写）
MANIFEST = ROOT / "manifest.json"

SITE_TITLE = "D2R Reimagined Wiki"
DEFAULT_LOCALE = "en"
LOCALES = {"en": "", "zh": "zh"}
LOCALE_LABELS = {"en": "EN", "zh": "中文"}
LIVE_ORIGIN = "https://wiki.d2r-reimagined.com"
INTERNAL_HOSTS = {"wiki.d2r-reimagined.com", "www.wiki.d2r-reimagined.com"}
# 线上站点自身的功能页，不带语言前缀
SITE_PAGES = {"register", "login", "logout", "admin", "profile", "_assets", "s"}

PAGE_EXTS = {".md", ".html", ".htm"}
EXCLUDE_DIRS = {".git", ".idea", ".venv", "tools", "_site", "__pycache__", "node_modules"}
SKIP_STEMS = {"README"}

# 侧边栏里希望排在前面的条目（其余按名称排序），想调整顺序改这里即可。
TOP_ORDER = [
    "home",
    "new_player_guide",
    "Installs",
    "Updating_The_Mod",
    "FAQ",
    "ClassChanges",
    "Hirelings",
    "AreaLevels",
    "QualityUpgrading",
    "Oskills-and-CTCs",
    "Builds",
    "Items",
    "recipes",
    "installguides",
    "Patch_Notes",
]

# 中文界面下的目录名
DIR_LABELS_ZH = {
    "Builds": "构筑推荐",
    "Items": "物品",
    "Patch_Notes": "补丁说明",
    "recipes": "合成配方",
    "installguides": "安装指南",
    "newbieguide": "新手引导",
    "qualityupgrading": "品质升级",
    "maps": "地图",
    "easyinstall": "简易安装",
    "DesktopLauncher": "桌面启动器",
}

HEADING_RE = re.compile(r"<h([1-6])(\s[^>]*)?>(.*?)</h\1>", re.S | re.I)
ATTR_RE = re.compile(r'\b(href|src)\s*=\s*"([^"]*)"', re.I)
TAG_RE = re.compile(r"<[^>]+>")
EXT_ANCHOR_RE = re.compile(r'<a\s+(?![^>]*\btarget=)([^>]*?href="(?:https?:)?//[^"]*"[^>]*)>', re.I)


# ---------------------------------------------------------------- 数据模型


def prettify(name):
    return name.replace("_", " ").replace("-", " ").strip()


class Page:
    __slots__ = ("stem", "locale", "path", "ext", "meta", "body")

    def __init__(self, stem, locale, path, ext, meta, body):
        self.stem = stem
        self.locale = locale
        self.path = path
        self.ext = ext
        self.meta = meta
        self.body = body

    @property
    def title(self):
        return self.meta.get("title") or prettify(self.stem.split("/")[-1])

    @property
    def description(self):
        return self.meta.get("description", "")

    @property
    def date(self):
        return self.meta.get("date", "")


# ---------------------------------------------------------------- 扫描


def walk_tree(root):
    """产出 (绝对路径, root 之下的相对路径)。"""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith("."))
        for name in sorted(filenames):
            if name.startswith("."):
                continue
            full = Path(dirpath) / name
            yield full, full.relative_to(root)


def parse_frontmatter(text, ext):
    meta = {}
    if ext == ".md":
        m = re.match(r"^\s*---\r?\n(.*?)\r?\n---[ \t]*\r?\n?", text, re.S)
        if not m:
            return meta, text
        block, body = m.group(1), text[m.end():]
    else:
        m = re.match(r"^\s*<!--(.*?)-->", text, re.S)
        if not m:
            return meta, text
        block, body = m.group(1), text[m.end():]

    for line in block.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or ":" not in stripped:
            continue
        key, _, value = stripped.partition(":")
        meta[key.strip()] = value.strip()
    return meta, body.lstrip("\r\n")


def scan(en_root, zh_root):
    """英文从上游目录读，中文从本仓库 zh/ 读；两边用同一个 slug 对得上。"""
    pages = {loc: {} for loc in LOCALES}
    assets = []
    conflicts = []

    for locale, root in ((DEFAULT_LOCALE, en_root), ("zh", zh_root)):
        if not root.is_dir():
            continue
        for full, rel in walk_tree(root):
            ext = full.suffix.lower()

            if ext in PAGE_EXTS:
                stem_path = rel.with_suffix("")
                if stem_path.parts[0] in SKIP_STEMS:
                    continue
                stem = stem_path.as_posix()
                text = full.read_text(encoding="utf-8", errors="replace")
                meta, body = parse_frontmatter(text, ext)
                page = Page(stem, locale, full, ext, meta, body)

                # 同一个 stem 同时存在 .md 与 .html 时，Wiki.js 里只有一条记录：
                # 取 frontmatter date 较新的那个，日期相同则优先 ckeditor 的 .html。
                old = pages[locale].get(stem)
                if old is not None:
                    keep_new = page.date > old.date or (page.date == old.date and page.ext == ".html")
                    chosen, dropped = (page, old) if keep_new else (old, page)
                    conflicts.append(
                        "%s:%s 同时有 %s 与 %s，采用 %s"
                        % (locale, stem, old.path.name, page.path.name, chosen.path.name)
                    )
                    page = chosen
                pages[locale][stem] = page
            elif locale == DEFAULT_LOCALE:
                # 资源只有上游一份，zh/ 不放图片
                assets.append(rel)

    return pages, assets, conflicts


# ---------------------------------------------------------------- 渲染


def render_markdown(text):
    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "sane_lists", "attr_list", "md_in_html"],
        output_format="html5",
    )
    return md.convert(text)


# ---------------------------------------------------------------- 通用小工具


def rel_link(from_out, to_out):
    """两个路径都相对 _site/，返回可直接写进 HTML 的相对链接。"""
    return os.path.relpath(to_out.as_posix(), start=from_out.parent.as_posix()).replace(os.sep, "/")


def slugify(text, used):
    slug = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", text.lower(), flags=re.U).strip("-")[:60]
    slug = slug or "section"
    if slug in used:
        i = 2
        while "%s-%d" % (slug, i) in used:
            i += 1
        slug = "%s-%d" % (slug, i)
    used.add(slug)
    return slug


# ---------------------------------------------------------------- 链接重写


def rewrite_links(content, *, cur_out, tree, pages, asset_set, page_dir, where, warn):
    def repl(match):
        attr, raw = match.group(1).lower(), html_mod.unescape(match.group(2))
        if not raw or raw.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
            return match.group(0)

        path_part, frag, query = raw, "", ""
        if "#" in path_part:
            path_part, _, f = path_part.partition("#")
            frag = "#" + f
        if "?" in path_part:
            path_part, _, q = path_part.partition("?")
            query = "?" + q

        if path_part.startswith(("http://", "https://", "//")):
            url = "https:" + path_part if path_part.startswith("//") else path_part
            parsed = urlsplit(url)
            if parsed.netloc.lower() not in INTERNAL_HOSTS:
                return match.group(0)
            path = parsed.path
        elif path_part.startswith("/"):
            path = path_part
        elif path_part:
            path = posixpath.normpath(posixpath.join(page_dir, path_part))
        else:
            path = ""

        path = path.lstrip("/")
        for prefix in ("en/", "zh/"):
            if path.startswith(prefix):
                path = path[len(prefix):]
                break
        path = posixpath.normpath(path) if path else ""
        if path in (".", ""):
            path = "home"

        # 站内页面
        if attr == "href":
            stem = re.sub(r"\.(md|html?)$", "", path)
            if stem in pages[DEFAULT_LOCALE] or stem in pages["zh"]:
                target = Path(tree) / (stem + ".html")
                return '%s="%s"' % (attr, html_mod.escape(rel_link(cur_out, target) + query + frag, quote=True))
            # 目录链接 -> 目录下第一个页面（线上 wiki 的目录本身不是页面）
            prefix = path.rstrip("/") + "/"
            children = sorted(s for s in pages[DEFAULT_LOCALE] if s.startswith(prefix))
            if children and "." not in posixpath.basename(path):
                target = Path(tree) / (children[0] + ".html")
                return '%s="%s"' % (attr, html_mod.escape(rel_link(cur_out, target) + query + frag, quote=True))

        # 仓库里的静态资源（图片、压缩包等）
        if path in asset_set:
            return '%s="%s"' % (
                attr,
                html_mod.escape(rel_link(cur_out, Path(path)) + query + frag, quote=True),
            )

        # 兜底：指向线上站点
        head = path.split("/")[0]
        if head in SITE_PAGES:
            # 注册/登录等站点功能页，本来就不在内容仓库里，不算问题
            return '%s="%s"' % (attr, html_mod.escape(LIVE_ORIGIN + "/" + path + query + frag, quote=True))
        live_path = "/%s/%s" % (DEFAULT_LOCALE, path)
        warn("%s: 未找到本地目标 %r -> %s" % (where, raw, LIVE_ORIGIN + live_path))
        return '%s="%s"' % (attr, html_mod.escape(LIVE_ORIGIN + live_path + query + frag, quote=True))

    content = ATTR_RE.sub(repl, content)
    content = EXT_ANCHOR_RE.sub(lambda m: '<a target="_blank" rel="noopener" %s>' % m.group(1), content)
    return content


# ---------------------------------------------------------------- 标题锚点 / 目录


def add_heading_ids(content):
    toc = []
    used = set()

    def repl(match):
        level, attrs, inner = int(match.group(1)), match.group(2) or "", match.group(3)
        text = re.sub(r"\s+", " ", TAG_RE.sub("", inner)).strip()
        if not text:
            return match.group(0)
        found = re.search(r'id="([^"]+)"', attrs)
        if found:
            hid = found.group(1)
            used.add(hid)
        else:
            hid = slugify(text, used)
            attrs = ' id="%s"%s' % (hid, attrs)
        if level <= 3:
            toc.append((level, hid, text))
        return "<h%d%s>%s</h%d>" % (level, attrs, inner, level)

    return HEADING_RE.sub(repl, content), toc


# ---------------------------------------------------------------- 侧边栏


def build_nav(pages, tree, active_stem, cur_out):
    children = {}
    for stem in pages[DEFAULT_LOCALE]:
        parts = stem.split("/")
        for i in range(len(parts) - 1):
            children.setdefault("/".join(parts[:i]), {}).setdefault(parts[i], "dir")
        children.setdefault("/".join(parts[:-1]), {})[parts[-1]] = "page"

    def sort_key(parent, name, kind):
        stem = "%s/%s" % (parent, name) if parent else name
        try:
            priority = TOP_ORDER.index(stem)
        except ValueError:
            priority = len(TOP_ORDER)
        return (priority, kind != "dir", name.lower())

    def label_for(stem, name, kind):
        if kind == "dir":
            return DIR_LABELS_ZH.get(name, prettify(name)) if tree == "zh" else prettify(name)
        return (pages[tree].get(stem) or pages[DEFAULT_LOCALE][stem]).title

    def render(parent=""):
        entries = sorted(children.get(parent, {}).items(), key=lambda kv: sort_key(parent, kv[0], kv[1]))
        out = ['<ul class="nav">']
        for name, kind in entries:
            stem = "%s/%s" % (parent, name) if parent else name
            label = html_mod.escape(label_for(stem, name, kind))
            if kind == "dir":
                is_open = active_stem == stem or active_stem.startswith(stem + "/")
                out.append('<li class="nav-dir"><details%s><summary>%s</summary>' % (" open" if is_open else "", label))
                out.append(render(stem))
                out.append("</details></li>")
            else:
                badge = ""
                if tree == "zh" and stem not in pages["zh"]:
                    badge = ' <span class="badge" title="暂无中文译文，当前显示英文原文">EN</span>'
                elif tree == "en" and stem in pages["zh"]:
                    badge = ' <span class="badge zh" title="已有中文译文">中</span>'
                active = ' class="active"' if stem == active_stem else ""
                href = rel_link(cur_out, Path(tree) / (stem + ".html"))
                out.append('<li><a href="%s"%s>%s%s</a></li>' % (href, active, label, badge))
        out.append("</ul>")
        return "".join(out)

    return render()


# ---------------------------------------------------------------- 页面外壳


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="%(lang)s" data-root="%(root)s">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s - %(site)s</title>
<meta name="description" content="%(description)s">
<link rel="stylesheet" href="%(css)s">
</head>
<body>
<header class="topbar">
  <a class="brand" href="%(brand_href)s"><span class="logo">D2RR</span><span class="brand-text">%(site)s</span></a>
  <div class="search">
    <input id="q" type="search" placeholder="搜索页面…（Ctrl+K）" autocomplete="off" spellcheck="false">
    <div id="results" class="results" hidden></div>
  </div>
  <div class="langs">%(lang_switch)s</div>
</header>
<div class="layout">
  <nav class="sidebar">%(nav)s</nav>
  <main class="main">
    <div class="crumbs">%(crumbs)s</div>
%(banner)s%(heading)s    <article class="content">
%(content)s
    </article>
    <footer class="page-foot">%(foot)s</footer>
  </main>
  <aside class="toc">%(toc)s</aside>
</div>
<script src="%(js)s" defer></script>
</body>
</html>
"""


def render_crumbs(stem, pages, tree, cur_out):
    home = rel_link(cur_out, Path(tree) / "home.html")
    items = ['<a href="%s">%s</a>' % (home, "首页" if tree == "zh" else "Home")]
    parts = stem.split("/")
    for i in range(len(parts) - 1):
        sub = "/".join(parts[:i + 1])
        label = DIR_LABELS_ZH.get(parts[i], prettify(parts[i])) if tree == "zh" else prettify(parts[i])
        first = sorted(s for s in pages[DEFAULT_LOCALE] if s.startswith(sub + "/"))
        if first:
            href = rel_link(cur_out, Path(tree) / (first[0] + ".html"))
            items.append('<a href="%s">%s</a>' % (href, html_mod.escape(label)))
        else:
            items.append(html_mod.escape(label))
    items.append(html_mod.escape((pages[tree].get(stem) or pages[DEFAULT_LOCALE][stem]).title))
    return " / ".join(items)


def render_toc(toc):
    if not toc:
        return ""
    out = ['<div class="toc-title">本页目录</div><ul>']
    for level, hid, text in toc:
        out.append('<li class="lvl%d"><a href="#%s">%s</a></li>' % (level, hid, html_mod.escape(text)))
    out.append("</ul>")
    return "".join(out)


def render_lang_switch(tree, stem, pages, cur_out):
    has_zh = stem in pages["zh"]
    zh_link = rel_link(cur_out, Path("zh") / (stem + ".html"))
    en_link = rel_link(cur_out, Path("en") / (stem + ".html"))
    if tree == "zh":
        zh = '<a class="on" href="%s">中文</a>' % zh_link
        en = '<a href="%s">EN</a>' % en_link
    else:
        zh = ('<a href="%s">中文</a>' % zh_link) if has_zh else '<span class="off" title="暂无中文译文">中文</span>'
        en = '<a class="on" href="%s">EN</a>' % en_link
    return zh + en


# ---------------------------------------------------------------- 构建


def git_rev(repo, rev="HEAD", fmt="%h"):
    """读 git 提交信息，失败返回空串（非 git 目录时用 --content 指本地路径）。"""
    try:
        out = subprocess.run(
            ["git", "-C", str(repo), "log", "-1", "--date=short", "--format=" + fmt, rev],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except Exception:
        return ""
    return out


def build(args):
    en_root = Path(args.content).resolve() if args.content else UPSTREAM
    if not en_root.is_dir() or not any(en_root.iterdir()):
        sys.exit(
            "找不到英文原文：%s\n"
            "先拉取上游 submodule：git submodule update --init\n"
            "或者用 --content /path/to/wiki-content 指向本地检出。" % en_root
        )
    pages, assets, conflicts = scan(en_root, ZH_DIR)

    if OUT.exists():
        for entry in list(OUT.iterdir()):
            if entry.is_symlink() or entry.is_file():
                entry.unlink()
            else:
                shutil.rmtree(entry)
    OUT.mkdir(exist_ok=True)

    asset_set = {a.as_posix() for a in assets}
    for rel in assets:
        src = en_root / rel
        dest = OUT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        os.symlink(os.path.relpath(str(src), str(dest.parent)), dest)

    (OUT / "assets").mkdir(parents=True, exist_ok=True)
    shutil.copy(str(THEME / "site.css"), str(OUT / "assets" / "site.css"))
    shutil.copy(str(THEME / "site.js"), str(OUT / "assets" / "site.js"))

    warnings = []
    search = []
    written = 0
    zh_pages = set(pages["zh"])

    for tree in LOCALES:
        for stem in sorted(pages[DEFAULT_LOCALE]):
            en_page = pages[DEFAULT_LOCALE][stem]
            page = pages[tree].get(stem)
            fallback = page is None
            page = page or en_page
            cur_out = Path(tree) / (stem + ".html")

            content = render_markdown(page.body) if page.ext == ".md" else page.body
            content = rewrite_links(
                content,
                cur_out=cur_out,
                tree=tree,
                pages=pages,
                asset_set=asset_set,
                page_dir=posixpath.dirname(stem),
                where="%s/%s" % (tree, stem),
                warn=warnings.append,
            )
            content, toc = add_heading_ids(content)

            first = HEADING_RE.search(content)
            heading = ""
            if not first or int(first.group(1)) > 2:
                heading = '    <h1 class="page-title">%s</h1>\n' % html_mod.escape(page.title)

            banner = ""
            if fallback and tree == "zh":
                banner = (
                    '    <div class="banner">本页暂无中文译文，当前显示英文原文。'
                    '<a href="%s">查看英文页面</a></div>\n'
                    % rel_link(cur_out, Path("en") / (stem + ".html"))
                )
            elif not fallback and page.date and en_page.date and page.date < en_page.date:
                banner = (
                    '    <div class="banner warn">英文原文已于 %s 更新，本页译文可能已过期。</div>\n'
                    % html_mod.escape(en_page.date[:10])
                )

            try:
                source = page.path.relative_to(ROOT).as_posix()
            except ValueError:
                source = page.path.name
            foot = '源文件 <code>%s</code> · <a href="%s/%s/%s">线上原文</a>' % (
                html_mod.escape(source),
                LIVE_ORIGIN,
                DEFAULT_LOCALE,
                stem,
            )

            doc = PAGE_TEMPLATE % {
                "lang": tree,
                "root": rel_link(cur_out, Path(".")),
                "site": html_mod.escape(SITE_TITLE),
                "title": html_mod.escape(page.title),
                "description": html_mod.escape(page.description),
                "css": rel_link(cur_out, Path("assets/site.css")),
                "js": rel_link(cur_out, Path("assets/site.js")),
                "brand_href": rel_link(cur_out, Path(tree) / "home.html"),
                "lang_switch": render_lang_switch(tree, stem, pages, cur_out),
                "nav": build_nav(pages, tree, stem, cur_out),
                "crumbs": render_crumbs(stem, pages, tree, cur_out),
                "banner": banner,
                "heading": heading,
                "content": content.rstrip("\n"),
                "foot": foot,
                "toc": render_toc(toc),
            }
            dest = OUT / cur_out
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(doc, encoding="utf-8")
            written += 1

            text = re.sub(r"\s+", " ", TAG_RE.sub(" ", content)).strip()
            search.append(
                {
                    "t": page.title,
                    "p": "%s/%s" % (tree, stem),
                    "l": tree,
                    "z": 1 if stem in zh_pages else 0,
                    "x": text[:400],
                }
            )

    (OUT / "assets" / "search.json").write_text(
        json.dumps(search, ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
    )
    (OUT / "index.html").write_text(
        """<!DOCTYPE html>
<html lang="zh"><head><meta charset="utf-8"><title>D2R Reimagined Wiki 本地预览</title>
<script>location.replace((localStorage.getItem('d2rr-lang')||'zh')+'/home.html')</script>
</head><body style="background:#12161d;color:#d9dde3;font-family:system-ui;padding:40px">
<p>正在跳转…如果没有自动跳转，请点击：</p>
<p><a style="color:#e0b657" href="zh/home.html">中文</a> · <a style="color:#e0b657" href="en/home.html">English</a></p>
</body></html>
""",
        encoding="utf-8",
    )

    print("英文页 %d · 中文页 %d · 资源 %d · 生成文件 %d" % (
        len(pages[DEFAULT_LOCALE]), len(pages["zh"]), len(assets), written))
    rev = git_rev(en_root, fmt="%h %ad %s")
    if rev:
        print("英文原文版本：%s" % rev)
        if args.content:
            print("  （--content 指定的本地检出）")
    if conflicts:
        print("\n同路径多文件：")
        for item in conflicts:
            print("  - " + item)
    if warnings:
        print("\n未解析的链接 %d 条（已回退到线上地址）：" % len(warnings))
        for item in warnings[:args.max_warnings]:
            print("  - " + item)
        if len(warnings) > args.max_warnings:
            print("  ... 其余 %d 条省略，用 --max-warnings 调整" % (len(warnings) - args.max_warnings))
    else:
        print("\n所有内部链接均已解析。")
    print("\n产物目录：%s" % OUT)
    return {"warnings": warnings, "conflicts": conflicts}


def main():
    parser = argparse.ArgumentParser(description="构建 D2R Reimagined Wiki 本地预览站")
    parser.add_argument("--serve", action="store_true", help="构建后启动本地服务器")
    parser.add_argument("--port", type=int, default=8787, help="--serve 使用的端口")
    parser.add_argument("--strict", action="store_true", help="存在未解析链接时以非 0 退出")
    parser.add_argument("--max-warnings", type=int, default=20, help="最多打印多少条警告")
    parser.add_argument("--content", help="英文原文目录（默认用 upstream/ submodule）")
    args = parser.parse_args()

    stats = build(args)
    if args.serve:
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(OUT))
        addr = ("127.0.0.1", args.port)
        print("\n本地预览：http://%s:%d/zh/home.html  (Ctrl+C 停止)" % addr)
        try:
            with http.server.ThreadingHTTPServer(addr, handler) as httpd:
                httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n已停止")
    return 1 if (args.strict and stats["warnings"]) else 0


if __name__ == "__main__":
    sys.exit(main())
