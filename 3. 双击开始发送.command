#!/bin/bash
# 发帖脚本

# 获取脚本所在目录
BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SYSTEM_DIR="$BASE_DIR/system"

# 激活虚拟环境
source "$SYSTEM_DIR/venv/bin/activate"

# 运行 Python 脚本
python3 "$SYSTEM_DIR/src/post_thread.py"
