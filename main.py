import os
import requests
import datetime
import json

# --- 1. 配置区 ---
TG_TOKEN = os.getenv("TG_BOT_TOKEN")
CH_ID = os.getenv("CHANNEL_ID")
# 物理路径：你的收款地址
MY_WALLET = "CjBusumcVax2DtzLWVMd6KKXSHDeV7tbNRYdaVHL5SJf"

# --- 2. 鲁棒性工具：安全除法 ---
def safe_div(n, d):
    """物理对冲：防止除零导致 Bot 停机"""
    try:
        return float(n) / float(d) if float(d) > 0 else 0
    except:
        return 0

def send_tg_message(text):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {"chat_id": CH_ID, "text": text, "parse_mode": "Markdown", "disable_web_page_preview": True}
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e: print(f"发送失败: {e}")

# --- 3. 核心计算引擎 ---
def calculate_v23_score(p):
    score = 0
    liq = p.get('liquidity', {}).get('usd', 0)
    fdv = p.get('fdv', 0)
    
    # 物理修复：使用 safe_div 防止镜像链路异常
    risk_ratio = safe_div(fdv, liq)
    
    if liq > 400000: score += 20
    if risk_ratio < 10: score += 20
    if p.get('info', {}).get('audits'): score += 20
    
    return round(score, 1)

# --- 4. 自动化任务 ---
def hunt_solana_v23():
    url = "https://api.dexscreener.com/latest/dex/chains/solana"
    try:
        response = requests.get(url, timeout=10).json()
        pairs = response.get('pairs', [])
        unique_tokens = []
        seen = set()
        
        for p in pairs:
            addr = p['baseToken']['address']
            if addr not in seen and p.get('liquidity', {}).get('usd', 0) > 400000:
                unique_tokens.append(p)
                seen.add(addr)
            if len(unique_tokens) >= 3: break
                for p in pairs:
    base_token = p.get('baseToken', {})
    symbol = base_token.get('symbol', '').upper()
    
    # 物理过滤：如果币名里带 SOL，直接跳过，看下一个
    if symbol in ["SOL", "WSOL", "WRAPPED SOL"]:
        continue
        
    # 原有的流动性判断逻辑...
    if p.get('liquidity', {}).get('usd', 0) > 400000:
        unique_tokens.append(p)
            
        report = f"💎 **百万美金终极收割系统 (V23.1)**\n"
        report += f"状态：物理修复完成 | 监听中...\n\n"
        
        for p in unique_tokens:
            score = calculate_v23_score(p)
            price = float(p.get('priceUsd', 0))
            entry = price * 0.94
            
            report += f"- **{p['baseToken']['name']}**\n"
            report += f"  🏆 综合评分: `{score}`\n"
            report += f"  🎯 建议入场: `${entry:.6f}`\n"
            # 关键修复：此处缩进已严格对齐，防止 IndentationError
            report += f"  💳 佣金打赏(20%): `{MY_WALLET}`\n"
            report += f"  [实时追踪]({p['url']})\n\n"
            
        return report
    except Exception as e:
        return f"❌ 物理链路同步异常: {e}"

def main():
    if not TG_TOKEN or not CH_ID: 
        print("缺少环境变量")
        return
    # 执行并发送
    content = hunt_solana_v23()
    send_tg_message(content)

if __name__ == "__main__":
    main()
