import os, requests, time

# --- 1. 物理配置区 ---
TG_TOKEN = os.getenv("TG_BOT_TOKEN")
CH_ID = os.getenv("CHANNEL_ID")
MY_WALLET = "CjBusumcVax2DtzLWVMd6KKXSHDeV7tbNRYdaVHL5SJf"

def send_msg(text):
    if not TG_TOKEN or not CH_ID: return
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    try: requests.post(url, data={"chat_id": CH_ID, "text": text, "parse_mode": "Markdown"}, timeout=15)
    except: pass

def get_data():
    """采用物理模拟请求，绕过 API 屏蔽"""
    url = "https://api.dexscreener.com/latest/dex/chains/solana"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    for _ in range(3): # 增加物理重试
        try:
            r = requests.get(url, headers=headers, timeout=20)
            if r.status_code == 200: return r.json().get('pairs', [])
        except: time.sleep(5)
    return []

# --- 2. 核心执行逻辑 (极简缩进模式) ---
def main():
    pairs = get_data()
    if not pairs:
        send_msg("⏳ **API 链路受限**：系统正在自动寻找镜像节点，请耐心等待...")
        return

    report = "🚀 **百万目标核心预警 (V23.6)**\n\n"
    count = 0
    for p in pairs:
        # 物理过滤：排除原生 SOL，筛选 30w+ 流动性资产
        sym = p.get('baseToken', {}).get('symbol', '').upper()
        liq = float(p.get('liquidity', {}).get('usd', 0))
        
        if "SOL" in sym or liq < 300000: continue
            
        report += f"📍 **{sym}**\n"
        report += f"💰 流动性: `${int(liq):,}`\n"
        report += f"🎯 价格: `${p.get('priceUsd', '0')}`\n"
        report += f"💳 佣金打赏: `{MY_WALLET}`\n"
        report += f"🔗 [查看追踪]({p.get('url','')})\n\n"
        
        count += 1
        if count >= 5: break

    if count > 0:
        send_msg(report)
    else:
        send_msg("🔎 扫描完成：当前链上暂无 30w 流动性以上的新爆发信号。")

if __name__ == "__main__":
    main()
