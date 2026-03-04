import requests
import os
import json

# ================= 配置区 =================
# 物理路径映射：请确保在 GitHub Secrets 中已配置这些变量
TG_TOKEN = os.getenv('TELEGRAM_TOKEN')
TG_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
# 阈值下调至 20w，兼顾 Alpha 捕捉与风险对冲
MIN_LIQUIDITY = 200000 
# ==========================================

def get_solana_signals():
    """
    抓取 Solana 链上高流动性代币的物理数据
    """
    url = "https://api.dexscreener.com/latest/dex/search?q=solana"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            print(f"物理链路抖动: HTTP {response.status_code}")
            return []
        
        data = response.json()
        pairs = data.get('pairs', [])
        
        filtered_signals = []
        for p in pairs:
            # 物理过滤逻辑：必须是 Solana 链且流动性 > 20w
            liq_usd = float(p.get('liquidity', {}).get('usd', 0))
            if p.get('chainId') == 'solana' and liq_usd > MIN_LIQUIDITY:
                # 排除原生 SOL 本身，只抓取代币
                if p.get('baseToken', {}).get('symbol') != 'SOL':
                    signal = {
                        "symbol": p.get('baseToken', {}).get('symbol'),
                        "price": p.get('priceUsd'),
                        "liq": liq_usd,
                        "vol_24h": p.get('volume', {}).get('h24', 0),
                        "url": p.get('url')
                    }
                    filtered_signals.append(signal)
        return filtered_signals
    except Exception as e:
        print(f"数据解析解析出错: {str(e)}")
        return []

def send_to_tg(message):
    """
    物理投递：将信号发送至 Telegram，供 Make.com 抓取
    """
    if not message:
        return
    
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {
        "chat_id": TG_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"投递失败: {e}")

if __name__ == "__main__":
    print("V23.1.15 引擎启动，正在物理扫描 Solana 链...")
    signals = get_solana_signals()
    
    if not signals:
        print("当前市场未发现 20w 流动性以上的优质代币（已过滤 $SOL）。")
    else:
        for s in signals:
            report = (
                f"🚨 *Alpha 信号 (20w+)*\n"
                f"代币: {s['symbol']}\n"
                f"价格: ${s['price']}\n"
                f"流动性: ${s['liq']:,.0f}\n"
                f"24h成交: ${s['vol_24h']:,.0f}\n"
                f"链接: [DexScreener]({s['url']})"
            )
            print(f"发现信号: {s['symbol']}")
            send_to_tg(report)
