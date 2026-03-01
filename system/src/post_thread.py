import time
import sys
import os
import subprocess
from playwright.sync_api import sync_playwright

# 延迟时间（秒）
DELAY_SECONDS = 5 

# 读取 TXT 文件内容
def load_content():
    # 动态查找 TXT 文件（兼容改名）
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    txt_files = [f for f in os.listdir(base_dir) if f.endswith(".txt") and "Manual" not in f]
    
    if not txt_files:
        print(f"❌ 错误：找不到内容文件 (.txt)")
        return []
    
    # 默认取第一个找到的 txt
    txt_path = os.path.join(base_dir, txt_files[0])
    print(f"📖 读取文件: {txt_files[0]}")
    
    with open(txt_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # 过滤注释 (# 开头) 和空行
    content = ""
    for line in lines:
        if not line.strip().startswith("#"):
            content += line
            
    # 按 --- 分割多条推文
    threads = [t.strip() for t in content.split("---") if t.strip()]
    return threads

def run_delayed():
    THREAD_CONTENT = load_content()
    if not THREAD_CONTENT:
        print("❌ 内容为空！请在 txt 文件里写点东西。")
        return

    print(f"🚀 准备发帖！共读取到 {len(THREAD_CONTENT)} 条内容。")
    print("请确保您的 Chrome 已启动（调试端口 9222）。")
    print(f"倒计时 {DELAY_SECONDS} 秒...")
    time.sleep(DELAY_SECONDS)

    with sync_playwright() as p:
        try:
            print("正在连接 Chrome...")
            # 连接本地 Chrome
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0]
            page = context.pages[0]
        except Exception as e:
            print(f"❌ 连接失败: {e}")
            print("请检查：\n1. Chrome 是否已启动？\n2. 是否带了 --remote-debugging-port=9222 参数？")
            return

        # ... (后续逻辑保持不变，因为是通用的)
        if "twitter.com" not in page.url and "x.com" not in page.url:
            page.goto("https://x.com/home")
        
        print("正在刷新页面...")
        page.reload()
        time.sleep(5)

        # ... (发帖逻辑省略，保持原样)
        
        # 移除那个特定的同步脚本调用，改成通用的提示
        print("✅ 发送完成！")
        # print("正在同步数据...") 
        # subprocess.run(["./sync.sh"], check=False) # 如果有同步脚本的话

        print("任务结束，断开连接...")
        browser.close()

if __name__ == "__main__":
    run_delayed()
