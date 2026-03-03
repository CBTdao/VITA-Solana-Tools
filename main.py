import os
import requests

# --- 1. 配置区 ---
TG_TOKEN = os.getenv("TG_BOT_TOKEN")
CH_ID = os.getenv("CHANNEL_ID")
# 物理路径：你的收款地址
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

# --- 2. 核心扫描 (V23.1 原始逻辑) ---
def hunt_solana_v23():
    # 采用搜索模式，这是 V23.1 最稳的路径
    url = "https://api.dexscreener.com/latest/dex/search?q=solana"
    try:
        response = requests.get(url, timeout=20).json()
        pairs = response.get('pairs', [])
        
        unique_tokens = []
        seen = set()
        
        for p in pairs:
            # 基础过滤：流动性 > 40w
            liq = float(p.get('liquidity', {}).get('usd', 0))
            addr = p.get('baseToken', {}).get('address', '')
            
            if addr not in seen and liq > 400000:
                unique_tokens.append(p)
                seen.add(addr)
            
            if len(unique_tokens) >= 3: break
            
        if not unique_tokens:
            return "⏳ 系统扫描中，暂无符合 40w+ 流动性的信号。"

        report = f"🚀 **Solana 资产扫描 (V23.1)**\n\n"
        
        for p in unique_tokens:
            sym = p['baseToken']['symbol']
            price = p.get('priceUsd', '0')
            
            report += f"- **{sym}**\n"
            report += f"  💰 流动性: `${int(float(p['liquidity']['usd'])):,}`\n"
            report += f"  🎯 现价: `${price}`\n"
            report += f"  💳 佣金打赏: `{MY_WALLET}`\n"
            report += f"  [查看行情]({p['url']})\n\n"
            
        return report
    except Exception as e:
        return f"❌ 扫描异常: {str(e)[:30]}"

# --- 3. 执行入口 ---
def main():
    content = hunt_solana_v23()
    send_tg_message(content)

if __name__ == "__main__":
    main()
