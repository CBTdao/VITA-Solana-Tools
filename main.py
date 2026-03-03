import os
import requests
import datetime

# --- 1. 物理配置区 (100万目标基石) ---
TG_TOKEN = os.getenv("TG_BOT_TOKEN")
CH_ID = os.getenv("CHANNEL_ID")
# 物理路径：资产回收唯一地址
MY_WALLET = "CjBusumcVax2DtzLWVMd6KKXSHDeV7tbNRYdaVHL5SJf"

def send_tg_message(text):
    if not TG_TOKEN or not CH_ID: return
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {
        "chat_id": CH_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    try:
        requests.post(url, data=payload, timeout=15)
    except:
        pass

# --- 2. 核心扫描引擎 (V23.1 稳定框架) ---
def hunt_solana_v23():
    # 物理修复：改用 Solana 全链活跃接口，跳过关键词搜索限制
    url = "https://api.dexscreener.com/latest/dex/chains/solana"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=20).json()
        pairs = response.get('pairs', [])
        
        unique_tokens = []
        seen = set()
        
        # 物理黑名单：排除 SOL 原生及包装资产
        BLACK_LIST = ["SOL", "WSOL", "WRAPPED SOL"]
        
        for p in pairs:
            base = p.get('baseToken', {})
            addr = base.get('address', '')
            sym = base.get('symbol', '').upper()
            liq = float(p.get('liquidity', {}).get('usd', 0))
            
            # 物理过滤逻辑：1.不重复 2.不在黑名单 3.流动性 > 35w (略微下调以增加样板量)
            if (addr not in seen and 
                sym not in BLACK_LIST and 
                liq > 350000):
                
                unique_tokens.append(p)
                seen.add(addr)
            
            if len(unique_tokens) >= 5: break
            
        if not unique_tokens:
            return "⏳ **扫描报告**：Solana 链上暂未发现 35w 流动性以上的高价值新信号。"

        report = f"🚀 **Solana 生态 Alpha 预警 (V23.1.2)**\n"
        report += f"状态：已物理屏蔽 SOL | 全链监测中\n\n"
        
        for p in unique_tokens:
            sym = p['baseToken']['symbol']
            price = p.get('priceUsd', '0')
            liq = int(p['liquidity']['usd'])
            
            report += f"- **{sym}**\n"
            report += f"  💰 流动性: `${liq:,}`\n"
            report += f"  🎯 现价: `${price}`\n"
            report += f"  💳 佣金打赏: `{MY_WALLET}`\n"
            report += f"  [查看行情]({p['url']})\n\n"
            
        return report
    except Exception as e:
        return f"❌ 物理链路抖动，正在自愈... (Err: {str(e)[:20]})"

# --- 3. 执行入口 ---
def main():
    content = hunt_solana_v23()
    send_tg_message(content)

if __name__ == "__main__":
    main()
