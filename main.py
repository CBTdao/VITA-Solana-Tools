import requests
import os
import time

# ================= 物理配置对齐 (图 15) =================
TG_TOKEN = os.getenv('TG_BOT_TOKEN')
TG_CHAT_ID = os.getenv('CHANNEL_ID')
# 设定 10w 高质量门槛，目标 100 万资产增长
MIN_LIQUIDITY = 100000 
# =======================================================

def fetch_alpha():
    url = "https://api.dexscreener.com/latest/dex/search?q=solana%20raydium"
    print(f"[{time.strftime('%H:%M:%S')}] 100万目标：高质量代币审计中...")
    try:
        res = requests.get(url, timeout=15)
        pairs = res.json().get('pairs', [])
        results = []
        exclude = ['SOL', 'WSOL', 'USDC', 'USDT', 'JITOSOL']
        
        for p in pairs:
            if p.get('chainId') != 'solana': continue
            liq = float(p.get('liquidity', {}).get('usd', 0))
            symbol = p.get('baseToken', {}).get('symbol', 'Unknown')
            
            if symbol.upper() not in exclude and liq >= MIN_LIQUIDITY:
                vol = float(p.get('volume', {}).get('h24', 0))
                # 质量审计：24h成交量必须活跃
                if vol > 50000:
                    results.append({
                        "name": symbol, "liq": liq, "vol": vol,
                        "price": p.get('priceUsd', '0'), "url": p.get('url')
                    })
        return results
    except: return []

def deliver_signal(s):
    # 物理文案优化：针对推特用户习惯
    report = (
        f"🔥 #Solana 链上异动预警\n\n"
        f"💎 代币: ${s['name']}\n"
        f"💰 流动性: ${s['liq']:,.0f}\n"
        f"📊 24h成交: ${s['vol']:,.0f}\n\n"
        f"✅ 审计结果：流动性充裕，具备 Alpha 潜力。\n"
        f"🔗 物理链路监控中：{s['url']}"
    )
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    try:
        requests.post(url, json={
            "chat_id": TG_CHAT_ID, "text": report, "parse_mode": "Markdown"
        }, timeout=10)
        print(f"🚀 已成功发射信号：{s['name']}")
    except: pass

if __name__ == "__main__":
    signals = fetch_alpha()
    # 严格限流，每轮只抓取最顶级的 2 个，对冲 X 封号风险
    for sig in signals[:2]:
        deliver_signal(sig)
        time.sleep(5)
