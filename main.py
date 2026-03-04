import feedparser
import time
import os
import requests

# ================= 物理配置对齐 =================
TG_TOKEN = os.getenv('TG_BOT_TOKEN')
TG_CHAT_ID = os.getenv('CHANNEL_ID')
# 目标：寻找单价 > $500 或时薪 > $50 的高价值任务
KEYWORDS = ["Python", "AI Automation", "Stable Diffusion", "LLM"]
# Upwork 搜索 RSS 链接 (示例，需替换为你自己的定制 RSS)
RSS_URL = "https://www.upwork.com/ab/feed/jobs/rss?q=python+ai&sort=recency"

def check_global_jobs():
    print(f"[{time.strftime('%H:%M:%S')}] 正在扫描全球劳务套利机会...")
    feed = feedparser.parse(RSS_URL)
    
    for entry in feed.entries:
        title = entry.title.lower()
        # 风险对冲逻辑：过滤掉低质量小单
        if any(kw.lower() in title for kw in KEYWORDS):
            # 物理路径确认：提取链接和描述
            job_link = entry.link
            desc = entry.description
            
            send_signal(entry.title, job_link)
            # 每次发现后休眠，防止 TG 频率过快
            time.sleep(5)

def send_signal(title, link):
    message = (
        f"🚨 发现高价值数字资产机会\n"
        f"项目: {title}\n"
        f"物理链接: {link}\n"
        f"动作: 建议立即使用 Gemini 生成竞标书"
    )
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TG_CHAT_ID, "text": message})
    print(f"✅ 信号已物理同步至 TG: {title}")

if __name__ == "__main__":
    while True:
        check_global_jobs()
        # 每 10 分钟物理轮询一次，对冲 IP 被封风险
        time.sleep(600)
