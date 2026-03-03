import os, requests, datetime

# --- 配置区 ---
TG_TOKEN = os.getenv("TG_BOT_TOKEN")
CH_ID = os.getenv("CHANNEL_ID")
WEBHOOK_URL = os.getenv("TWITTER_WEBHOOK") # 预留给自动发推工具

def send_tg(text):
    if not TG_TOKEN or not CH_ID: return
    requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage", 
                 data={"chat_id": CH_ID, "text": text, "parse_mode": "Markdown"})

# --- 懒人策略：自动化变现情报 ---
def get_lazy_strategy():
    now = datetime.datetime.now()
    # 周期性自动更换变现主题，无需人工干预
    strategies = [
        "【被动引流】将本频道置顶信号转发至 3 个 Solana Meme 社群，设置机器人自动回复。",
        "【资产锚定】检查地址，若有打赏则自动触发‘感谢名单’，建立社群归属感。",
        "【流量套利】开启 Webhook 自动同步，今日无需手动发推，关注私信即可。"
    ]
    return strategies[now.day % len(strategies)]

def hunt_v23_1_4():
    # 沿用最稳的搜索路径
    url = "https://api.dexscreener.com/latest/dex/search?q=solana"
    try:
        r = requests.get(url, timeout=20).json()
        pairs = r.get('pairs', [])[:3] # 只取前3，保持简洁
        
        report = f"🤖 **V23.1.4 自动化收割机**\n"
        report += f"💡 **今日躺平策略**：{get_lazy_strategy()}\n"
        report += f"---"
        
        for p in pairs:
            if float(p.get('liquidity', {}).get('usd', 0)) > 400000:
                report += f"\n📍 **{p['baseToken']['symbol']}** | Liq: ${int(float(p['liquidity']['usd'])):,}"
                report += f"\n🔗 [点击分析]({p['url']})\n"
        
        report += f"\n💳 100w目标回收站: `CjBusumcVax2DtzLWVMd6KKXSHDeV7tbNRYdaVHL5SJf`"
        return report
    except: return "⏳ 链路自愈中..."

if __name__ == "__main__":
    send_tg(hunt_v23_1_4())
