#!/bin/bash
# 强哥的 Twitter 机器人 - 全能启动器

BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SYSTEM_DIR="$BASE_DIR/system"
LOG_FILE="$SYSTEM_DIR/bot.log"

echo "🤖 正在启动强哥的机器人..."

# 1. 检查是否第一次运行
if [ ! -d "$SYSTEM_DIR/venv" ]; then
    echo "📦 检测到第一次运行，正在初始化环境..."
    
    # 检查 Python
    if ! command -v python3 &> /dev/null; then
        echo "❌ 错误：你的电脑没装 Python3！请先去 python.org 下载安装。"
        exit 1
    fi
    
    # 创建环境
    python3 -m venv "$SYSTEM_DIR/venv"
    source "$SYSTEM_DIR/venv/bin/activate"
    
    # 安装依赖
    echo "📦 正在安装依赖库..."
    pip install -r "$SYSTEM_DIR/requirements.txt"
    playwright install chromium
    
    echo "✅ 环境安装完成！"
else
    source "$SYSTEM_DIR/venv/bin/activate"
fi

# 2. 启动 Chrome
echo "🌐 正在启动 Chrome 浏览器..."
if ! pgrep -f "remote-debugging-port=9222" > /dev/null; then
    pkill -f "Google Chrome"
    sleep 1
    # Mac 标准路径
    /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 > /dev/null 2>&1 &
    echo "   Chrome 已启动！"
else
    echo "   Chrome 已经在运行中"
fi

# 3. 启动防睡眠
echo "☕️ 开启防睡眠模式..."
pkill -f "caffeinate -i -s"
caffeinate -i -s & 

echo "🎉 服务全部就绪！"
echo "👉 现在请去编辑 '2. 要把什么发推特.txt'，然后双击 '3. 开始发送.command'。"
