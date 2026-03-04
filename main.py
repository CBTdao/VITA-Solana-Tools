import requests
import os
import json
import time

# ================= 物理配置区 =================
TG_TOKEN = os.getenv('TELEGRAM_TOKEN')
TG_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
# 3w 门槛用于链路破冰验证
MIN_LIQUIDITY = 30000 
# =============================================

def fetch_solana_alpha():
    url = "https://api.dexscreener.com/latest/dex/search?q=solana"
    print(f"[{time.strftime('%H:%M:%S')}] 扫描启动，门槛: ${MIN_LIQUIDITY}")
    try:
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            print(f"❌ API 链路异常: HTTP {response.status_code}")
            return []
        data = response.json()
        pairs = data.get('pairs', [])
        print(f"📡 探测到 {len(pairs)} 个对，进入审计流程...")
        
        results = []
        exclude_list = ['SOL', 'WSOL', 'USDC', 'USDT', 'UXD']
        max_seen = 0
        
        for p in pairs:
            if p.get('chainId') != 'solana': continue
            liq = float(p.get('liquidity', {}).get('usd', 0))
            symbol = p.get('baseToken', {}).get('symbol', 'Unknown')
            
            if symbol.upper() not in exclude_list:
                max_seen = max(max_seen, liq)
                if liq >= MIN_LIQUIDITY:
                    print(f"✅ 审计通过: {symbol}")
                    results.append({
                        "name": symbol, "liq": liq, 
                        "price": p.get('priceUsd', '0'),
                        "vol_24h": p.get('volume', {}).get('h24', 0),
                        "url": p.get('url')
                    })
        if not results:
            print(f"ℹ️ 本次无信号。最高非SOL流动性: ${max_seen:,.0f}")
        return results
    except Exception as e:
        print(f"🚨 审计崩溃: {str(e)}")
        return []

def deliver_signal(s):
    if not TG_TOKEN or not TG_CHAT_ID: return
    report = (
        f"🚨 *Alpha 信号 (3w+)*\n\n"
        f"💎 代币: #{s['name']}\n"
        f"💰 流动性: ${s['liq']:,.0f}\n"
        f"📊 24h成交: ${s['vol_24h']:,.0f}\n"
        f"💵 价格: ${s['price']}\n\n"
        f"🔗 [DexScreener]({s['url']})"
    )
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    try:
        requests.post(url, json={
            "chat_id": TG_CHAT_ID, "text": report,
            "parse_mode": "Markdown", "disable_web_page_preview": False
        }, timeout=10)
        print(f"🚀 已投递: {s['name']}")
    except Exception as e:
        print(f"🚨 投递失败: {e}")

if __name__ == "__main__":
    signals = fetch_solana_alpha()
    for sig in signals:
        deliver_signal(sig)
        time.sleep(1)
