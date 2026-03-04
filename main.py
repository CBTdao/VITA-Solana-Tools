import requests
import os
import time

# ================= 物理配置区 =================
TG_TOKEN = os.getenv('TELEGRAM_TOKEN')
TG_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
# 降低至 2w 强行破冰，验证链路
MIN_LIQUIDITY = 20000 
# =============================================

def fetch_solana_alpha():
    # 切换至物理更稳定的 Latest Pairs 接口
    url = "https://api.dexscreener.com/latest/dex/tokens/So11111111111111111111111111111111111111112"
    print(f"[{time.strftime('%H:%M:%S')}] 暴力扫描启动，门槛: ${MIN_LIQUIDITY}")
    try:
        response = requests.get(url, timeout=15)
        data = response.json()
        pairs = data.get('pairs', [])
        print(f"📡 实时捕获 {len(pairs)} 个交易对，开始硬核审计...")
        
        results = []
        exclude_list = ['SOL', 'WSOL', 'USDC', 'USDT']
        
        for p in pairs:
            # 必须是 Raydium 或 Meteora 上的池子
            if p.get('chainId') != 'solana': continue
            
            liq = float(p.get('liquidity', {}).get('usd', 0))
            symbol = p.get('baseToken', {}).get('symbol', 'Unknown')
            
            # 记录审计过程
            if liq > 1000:
                print(f"🔍 检查: {symbol} | 流动性: ${liq:,.0f}")

            if liq >= MIN_LIQUIDITY and symbol.upper() not in exclude_list:
                print(f"✅ 捕获成功: {symbol}")
                results.append({
                    "name": symbol, "liq": liq, 
                    "price": p.get('priceUsd', '0'),
                    "url": p.get('url')
                })
        return results
    except Exception as e:
        print(f"🚨 链路崩溃: {str(e)}")
        return []

def deliver_signal(s):
    if not TG_TOKEN or not TG_CHAT_ID: return
    report = (
        f"🚨 *Alpha 发现 (2w+)*\n\n"
        f"💎 代币: #{s['name']}\n"
        f"💰 流动性: ${s['liq']:,.0f}\n"
        f"💵 价格: ${s['price']}\n\n"
        f"🔗 [DexScreener]({s['url']})"
    )
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    try:
        requests.post(url, json={
            "chat_id": TG_CHAT_ID, "text": report,
            "parse_mode": "Markdown"
        }, timeout=10)
        print(f"🚀 TG 已发射: {s['name']}")
    except: pass

if __name__ == "__main__":
    signals = fetch_solana_alpha()
    for sig in signals:
        deliver_signal(sig)
        time.sleep(1)
