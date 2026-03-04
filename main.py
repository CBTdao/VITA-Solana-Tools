import requests
import os
import time

# ================= 物理配置区 =================
TG_TOKEN = os.getenv('TELEGRAM_TOKEN')
TG_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
# 验证阶段门槛设为 2w
MIN_LIQUIDITY = 20000 
# =============================================

def fetch_real_alpha():
    # 物理升级：直接访问 Solana 链的高活跃度交易池总览
    url = "https://api.dexscreener.com/latest/dex/search?q=solana%20raydium"
    print(f"[{time.strftime('%H:%M:%S')}] 深度钻取启动，正在物理绕开 SOL 干扰...")
    
    try:
        response = requests.get(url, timeout=15)
        data = response.json()
        pairs = data.get('pairs', [])
        
        results = []
        # 严格排除审计列表
        exclude_list = ['SOL', 'WSOL', 'USDC', 'USDT', 'UXD', 'MSOL', 'JITOSOL']
        
        for p in pairs:
            if p.get('chainId') != 'solana': continue
            
            liq = float(p.get('liquidity', {}).get('usd', 0))
            symbol = p.get('baseToken', {}).get('symbol', 'Unknown')
            
            # 日志仅打印非 SOL 的代币，方便我们排查
            if symbol.upper() not in exclude_list:
                print(f"🔍 发现代币: {symbol} | 流动性: ${liq:,.0f}")
                if liq >= MIN_LIQUIDITY:
                    print(f"✅ 审计通过: {symbol}")
                    results.append({
                        "name": symbol, "liq": liq, 
                        "price": p.get('priceUsd', '0'),
                        "url": p.get('url')
                    })
        return results
    except Exception as e:
        print(f"🚨 链路异常: {str(e)}")
        return []

def deliver_signal(s):
    if not TG_TOKEN or not TG_CHAT_ID: return
    report = (
        f"🚨 *Alpha 信号 (2w+)*\n\n"
        f"💎 代币: #{s['name']}\n"
        f"💰 流动性: ${s['liq']:,.0f}\n"
        f"💵 价格: ${s['price']}\n\n"
        f"🔗 [查看详情]({s['url']})"
    )
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    try:
        requests.post(url, json={
            "chat_id": TG_CHAT_ID, "text": report,
            "parse_mode": "Markdown"
        }, timeout=10)
        print(f"🚀 TG 发射成功: {s['name']}")
    except: pass

if __name__ == "__main__":
    signals = fetch_real_alpha()
    print(f"--- 最终捕获 {len(signals)} 个非 SOL 信号 ---")
    for sig in signals:
        deliver_signal(sig)
        time.sleep(1)
