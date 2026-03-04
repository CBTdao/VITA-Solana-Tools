import requests
import os
import time

# ================= 物理配置区 =================
TG_TOKEN = os.getenv('TELEGRAM_TOKEN')
TG_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
MIN_LIQUIDITY = 30000 # 维持 3w 确保有币
# =============================================

def fetch_alpha():
    url = "https://api.dexscreener.com/latest/dex/search?q=solana%20raydium"
    try:
        res = requests.get(url, timeout=15)
        pairs = res.json().get('pairs', [])
        results = []
        for p in pairs:
            liq = float(p.get('liquidity', {}).get('usd', 0))
            symbol = p.get('baseToken', {}).get('symbol', 'Unknown')
            if symbol.upper() not in ['SOL', 'WSOL', 'USDC'] and liq >= MIN_LIQUIDITY:
                results.append({"name": symbol, "liq": liq, "url": p.get('url')})
        return results
    except: return []

def deliver_debug(s):
    # 物理打印：让我们在日志里看到底发没发出去
    print(f"📡 正在尝试投递: {s['name']} (目标 ID: {TG_CHAT_ID})")
    
    if not TG_TOKEN or not TG_CHAT_ID:
        print("❌ 物理故障：Secrets 里没填 Token 或 ID！")
        return

    report = f"🚨 物理链路自检\n代币: {s['name']}\n流动性: ${s['liq']:,.0f}\n链接: {s['url']}"
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    
    try:
        resp = requests.post(url, json={
            "chat_id": TG_CHAT_ID, 
            "text": report
        }, timeout=10)
        
        # 物理报错捕获
        if resp.status_code == 200:
            print(f"✅ TG 物理反馈：发送成功！")
        else:
            print(f"❌ TG 物理反馈错误：代码 {resp.status_code} | 信息: {resp.text}")
    except Exception as e:
        print(f"🚨 网络层物理崩溃: {e}")

if __name__ == "__main__":
    print(f"--- 物理链路全扫描开始 ---")
    signals = fetch_alpha()
    if not signals:
        print("当前市场暂无符合 3w 门槛的币。")
    else:
        # 只测第一个，节省日志空间
        deliver_debug(signals[0])
