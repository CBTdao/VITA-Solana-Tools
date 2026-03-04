import requests
import os
import time

# ================= 物理配置对齐 (图 15) =================
TG_TOKEN = os.getenv('TG_BOT_TOKEN')
TG_CHAT_ID = os.getenv('CHANNEL_ID')
# 设置高质量门槛
MIN_LIQUIDITY = 100000 
# =======================================================

def fetch_alpha():
    url = "https://api.dexscreener.com/latest/dex/search?q=solana%20raydium"
    print(f"[{time.strftime('%H:%M:%S')}] 100万目标自动化引擎运行中...")
    try:
        res = requests.get(url, timeout=15)
        pairs = res.json().get('pairs', [])
        results = []
        exclude = ['SOL', 'WSOL', 'USDC', 'USDT']
        
        for p in pairs:
            if p.get('chainId') != 'solana': continue
            liq = float(p.get('liquidity', {}).get('usd', 0))
            symbol = p.get('baseToken', {}).get('symbol', 'Unknown')
            
            if symbol.upper() not in exclude and liq >= MIN_LIQUIDITY:
                results.append({
                    "name": symbol, "liq": liq, "url": p.get('url')
                })
        return results
    except: return []

def deliver_to_webhook(s):
    # 采用 Make.com 最易识别的结构化文本
    report = (
        f"ALPHA_SIGNAL\n"
        f"TOKEN: {s['name']}\n"
        f"LIQUIDITY: ${s['liq']:,.0f}\n"
        f"LINK: {s['url']}"
    )
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    try:
        resp = requests.post(url, json={
            "chat_id": TG_CHAT_ID, 
            "text": report
        }, timeout=10)
        if resp.status_code == 200:
            print(f"✅ 物理发射成功: {s['name']}")
    except: pass

if __name__ == "__main__":
    signals = fetch_alpha()
    # 抓取前 3 个符合条件的信号
    for sig in signals[:3]:
        deliver_to_webhook(sig)
        time.sleep(2)
