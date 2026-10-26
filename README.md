# D2R Reimagined Wiki 中文译文

wiki.d2r-reimagined.com 的简体中文译文仓库。英文原文以 **只读 submodule** 方式引入，
本仓库只存译文和工具，不复制正文与图片。

## 目录

```
upstream/          git submodule -> https://github.com/D2R-Reimagined/wiki-content
                   英文页面 + 图片，一个字都不改
zh/                中文译文，路径与上游英文页完全一致（大小写、.md/.html 都照抄）
manifest.json      每篇译文核对过的英文版本（git blob + commit），增量翻译的依据
tools/             构建与校验脚本
_site/             构建产物（已 gitignore）
```

`zh/` 的目录约定就是 Wiki.js 2.x Git 存储对非默认语言的存放方式（`<locale>/<路径>`），
所以将来要回流官方，把 `zh/` 整个拷进上游仓库提交即可，不需要改任何路径。

## 日常流程

```bash
git submodule update --init --remote --recursive   # 拉上游最新内容
python3 tools/sync.py                              # 只看需要动的那几篇
python3 tools/sync.py --diff                       # 附带英文侧变更片段
# ...改 zh/ ...
python3 tools/check_i18n.py                        # 结构自查
python3 tools/sync.py --accept <页名>               # 标记已对齐当前上游
tools/build.sh --serve                             # 本地浏览 http://127.0.0.1:8787
```

`sync.py` 把每篇页面分成四类：**待复核**（上游改了英文）、**未译**、**已同步**、
**上游已删**。上游一次提交改几十页时，只需要处理落在「待复核」里的那几篇。

首次克隆后如果 `upstream/` 是空的，执行 `git submodule update --init`。
**不要用 `--depth 1`**，`--diff` 出增量需要上游的完整历史。

## 翻译约定

写译文前请看这几条，`check_i18n.py` 会按这些规则报错：

1. 文件放 `zh/`，路径、文件名、大小写、扩展名都与原文一致；frontmatter 里的
   `editor:` 照抄（`markdown` 或 `ckeditor`）。
2. frontmatter 的 `date:` 写译文自己的日期，`dateCreated:` 保留原值。
3. HTML 页只替换文本节点，**标签的数量与顺序不能变**（含 `<strong>` 这类行内标签）。
4. 标题保留英文锚点，深链才不会断：
   - Markdown：`## 玩法改动 {#gameplay-changes}`
   - HTML：`<h6 id="act-1-rogue">第一幕 · 罗格</h6>`
5. 图片路径、`<code>` 里的命令行、安装路径原样保留（构建脚本会把站内链接改成本地路径）。
6. 术语优先用暗黑破坏神 2 官方简中。已定译：护身符、符文、暗金、套装、手工、无形、
   恐惧地带、破免护身符、赦免令牌、赫拉迪克方块、地裂猛击、铁狼、罗格。

## 构建脚本

- `tools/build.py`：把 `upstream/` + `zh/` 渲染成 `_site/`，双语侧边栏树、Ctrl+K 搜索、
  页内「中/EN」切换；未翻译的页面自动回退英文并提示「本页暂无中文译文」。
- `tools/check_i18n.py`：孤儿页、标签结构差异（精确到第几个标签）、译文过期、分目录进度。
- `tools/sync.py`：增量待办，只用标准库，不需要 venv。
- `tools/build.sh`：自动创建 `.venv` 并装 `markdown`，然后调 `build.py`。
