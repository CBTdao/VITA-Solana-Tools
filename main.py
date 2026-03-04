import requests
import os
import time

# ================= 物理配置修正区 =================
# 这里修改为和你 GitHub Settings (图 15) 一致的名字
TG_TOKEN = os.getenv('TG_BOT_TOKEN')
TG_CHAT_ID = os.getenv('CHANNEL_ID')
# 门槛维持在 3w 确保今天能抓到信号
MIN_LIQUIDITY = 30000 
# ===============================================

def fetch_alpha():
    url = "https://api.dexscreener.com/latest/dex/search?q=solana%20raydium"
    try:
        res = requests.get(url, timeout=15)
        pairs = res.json().get('pairs', [])
        results = []
        for p in pairs:
            liq = float(p.get('liquidity', {}).get('usd', 0))
            symbol = p.get('baseToken', {}).get('symbol', 'Unknown')
            # 排除 SOL 本身
            if symbol.upper() not in ['SOL', 'WSOL'] and liq >= MIN_LIQUIDITY:
                results.append({"name": symbol, "liq": liq, "url": p.get('url')})
        return results
    except: return []

def deliver_signal(s):
    # 物理验证日志
    print(f"📡 尝试发射信号至 ID: {TG_CHAT_ID}")
    
    if not TG_TOKEN or not TG_CHAT_ID:
        print("❌ 物理故障：代码里的变量名与 GitHub Secrets 依然不匹配！")
        return

    report = f"🚨 *Alpha 发现*\n代币: #{s['name']}\n流动性: ${s['liq']:,.0f}\n🔗 [查看]({s['url']})"
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    
    try:
        resp = requests.post(url, json={
            "chat_id": TG_CHAT_ID, 
            "text": report,
            "parse_mode": "Markdown"
        }, timeout=10)
        
        if resp.status_code == 200:
            print(f"✅ TG 物理反馈：发送成功！")
        else:
            print(f"❌ TG 报错：{resp.text}")
    except Exception as e:
        print(f"🚨 网络崩溃: {e}")

if __name__ == "__main__":
    signals = fetch_alpha()
    if not signals:
        print("市场太冷，没抓到 3w 以上的代币。")
    else:
        # 先发一个测通链路
        deliver_signal(signals[0])
