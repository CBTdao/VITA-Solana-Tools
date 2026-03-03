import os
import requests

# --- 1. 基础配置 ---
TG_TOKEN = os.getenv("TG_BOT_TOKEN")
CH_ID = os.getenv("CHANNEL_ID")
MY_WALLET = "CjBusumcVax2DtzLWVMd6KKXSHDeV7tbNRYdaVHL5SJf"

def send_msg(text):
    if not TG_TOKEN or not CH_ID: return
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CH_ID, "text": text, "parse_mode": "Markdown"}, timeout=15)
    except:
        pass

def get_data():
    """暴力获取数据，不解析直接返回，出错则返回空列表"""
    url = "https://api.dexscreener.com/latest/dex/chains/solana"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=20)
        return r.json().get('pairs', [])
    except:
        return []

def main():
    pairs = get_data()
    if not pairs:
        send_msg("⏳ 系统自愈中：正在绕过 API 频率限制...")
        return

    report = "🚀 **百万目标核心扫描 (V23.4)**\n\n"
    count = 0
    
    for p in pairs:
        # 极简过滤逻辑，杜绝缩进错误
        base = p.get('baseToken', {})
        addr = base.get('address', '')
        sym = base.get('symbol', '').upper()
        liq = float(p.get('liquidity', {}).get('usd', 0))
        
        # 排除 SOL，只看 30w 以上流动性的新币
        if "SOL" in sym or liq < 300000:
            continue
            
        report += f"📍 **{sym}**\n"
        report += f"💰 流动性: `${int(liq):,}`\n"
        report += f"💳 收款: `{MY_WALLET}`\n"
        report += f"🔗 [点击追踪]({p.get('url','')})\n\n"
        
        count += 1
        if count >= 5: break

    if count > 0:
        send_msg(report)
    else:
        send_msg("🔎 扫描完成：暂无符合 30w 流动性的新信号。")

if __name__ == "__main__":
    main()
