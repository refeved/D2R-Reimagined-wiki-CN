#!/usr/bin/env bash
# 构建本地预览站。首次运行会在仓库根目录创建 .venv 并安装依赖。
#   tools/build.sh              -> 生成 _site/
#   tools/build.sh --serve      -> 生成并启动 http://127.0.0.1:8787
set -euo pipefail

cd "$(dirname "$0")/.."

if [ ! -x .venv/bin/python ]; then
  echo "首次运行：创建 Python 虚拟环境 .venv"
  python3 -m venv .venv
fi

if ! .venv/bin/python -c "import markdown" >/dev/null 2>&1; then
  echo "安装依赖：markdown"
  .venv/bin/pip install -q --disable-pip-version-check -r tools/requirements.txt
fi

exec .venv/bin/python tools/build.py "$@"
