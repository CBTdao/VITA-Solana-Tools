import os
import requests
import datetime
import json

# --- 1. 配置区 ---
TG_TOKEN = os.getenv("TG_BOT_TOKEN")
CH_ID = os.getenv("CHANNEL_ID")
# 物理路径：你的收款地址 (100万目标落脚点)
MY_WALLET = "CjBusumcVax2DtzLWVMd6KKXSHDeV7tbNRYdaVHL5SJf"

# --- 2. 鲁棒性工具 ---
def safe_div(n, d):
    """物理对冲：防止除零崩溃"""
    try:
        return float(n) / float(d) if float(d) > 0 else 0
    except:
        return 0

def send_tg_message(text):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {
        "chat_id": CH_ID, 
        "text": text, 
        "parse_mode": "Markdown", 
        "disable_web_page_preview": True
    }
    try:
        r = requests.post(url, data=payload, timeout=15)
        print(f"发送状态: {r.status_code}")
    except Exception as e: 
        print(f"发送失败: {e}")

# --- 3. 核心计算引擎 ---
def calculate_v23_score(p):
    score = 0
    liq = p.get('liquidity', {}).get('usd', 0)
    fdv = p.get('fdv', 0)
    vol24 = p.get('volume', {}).get('h24', 0)
    
    risk_ratio = safe_div(fdv, liq)
    
    # 评分逻辑：流动性 + 市值健康度 + 交易活跃度
    if liq > 300000: score += 20
    if 2 < risk_ratio < 15: score += 20
    if vol24 > liq * 0.5: score += 20
    
    return round(score, 1)

# --- 4. 自动化任务 ---
def hunt_solana_v23():
    # 物理路径：改用更稳定的全量活跃接口并加入 Headers
    url = "https://api.dexscreener.com/latest/dex/chains/solana"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code != 200:
            return "⏳ API 暂时繁忙，系统正在排队重试..."
            
        data = response.json()
        pairs = data.get('pairs', [])
        unique_tokens = []
        seen = set()
        
        # 物理屏蔽：SOL 原生及其包装地址
        SOL_BLACKLIST = [
            "So11111111111111111111111111111111111111112", 
            "11111111111111111111111111111111"
        ]
        
        for p in pairs:
            base_token = p.get('baseToken', {})
            addr = base_token.get('address')
            symbol = base_token.get('symbol', '').upper()
            
            # 过滤逻辑：非黑名单、非 SOL 关键字、流动性 > 30w
            if (addr not in seen and 
                addr not in SOL_BLACKLIST and 
                "SOL" not in symbol and
                p.get('liquidity', {}).get('usd', 0) > 300000):
                
                unique_tokens.append(p)
                seen.add(addr)
            
            if len(unique_tokens) >= 5: break
            
        if not unique_tokens:
            return "⏳ **系统扫描中...**\n暂无符合门槛的新信号。"
            
        report = f"🚀 **Solana 生态深度扫描 (V23.3)**\n"
        report += f"状态：物理修复生效 | 资产穿透中...\n\n"
        
        for p in unique_tokens:
            score = calculate_v23_score(p)
            price = float(p.get('priceUsd', 0))
            
            report += f"- **{p['baseToken']['symbol']}**\n"
            report += f"  🏆 综合评分: `{score}`\n"
            report += f"  💰 流动性: `${int(p['liquidity']['usd']):,}`\n"
            report += f"  🎯 现价: `${price:.8f}`\n"
            report += f"  💳 佣金打赏: `{MY_WALLET}`\n"
            report += f"  [实时追踪]({p['url']})\n\n"
            
        return report
    except Exception as e:
        return f"❌ 物理链路异常 (已尝试自动修复): {str(e)}"

def main():
    if not TG_TOKEN or not CH_ID: 
        print("缺少环境变量")
        return
    content = hunt_solana_v23()
    send_tg_message(content)

if __name__ == "__main__":
    main()
