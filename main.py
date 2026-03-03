
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
    # 物理路径：改用最新的 Solana 活跃交易对接口 (不带关键字过滤)
    url = "https://api.dexscreener.com/latest/dex/chains/solana" 
    try:
        response = requests.get(url, timeout=10).json()
        pairs = response.get('pairs', [])
        unique_tokens = []
        seen = set()
        
        # 排除原生 SOL 和包装 SOL 的地址 (防止刷屏)
        SOL_ADDRESSES = [
            "So11111111111111111111111111111111111111112", # WSOL
            "11111111111111111111111111111111"             # Native SOL
        ]
        
        for p in pairs:
            base_token = p.get('baseToken', {})
            addr = base_token.get('address')
            symbol = base_token.get('symbol', '')
            
            # 过滤逻辑：1. 不是 SOL 本身；2. 没出现过；3. 流动性 > 40w USD
            if (addr not in seen and 
                addr not in SOL_ADDRESSES and 
                symbol != "SOL" and
                p.get('liquidity', {}).get('usd', 0) > 400000):
                
                unique_tokens.append(p)
                seen.add(addr)
                
            if len(unique_tokens) >= 5: break # 增加展示位到 5 个，提高命中率
            
        if not unique_tokens:
            return "⏳ 正在扫描 Solana 生态，暂无符合百万级门槛的高评分新币..."

        report = f"🚀 **Solana 生态深度扫描 (V23.2)**\n"
        report += f"环境：全量数据监控 | 过滤原生 SOL\n\n"
        
        for p in unique_tokens:
            score = calculate_v23_score(p)
            price = float(p.get('priceUsd', 0))
            # 财富策略：针对新币，建议分批入场
            report += f"- **{p['baseToken']['symbol']}** ({p['baseToken']['name']})\n"
            report += f"  🏆 综合评分: `{score}`\n"
            report += f"  💰 流动性: `${int(p['liquidity']['usd']):,}`\n"
            report += f"  🎯 现价: `${price:.8f}`\n"
            report += f"  💳 佣金打赏: `{MY_WALLET}`\n"
            report += f"  [查看 K 线]({p['url']})\n\n"
            
        return report
    except Exception as e:
        return f"❌ 物理链路扫描异常: {e}"
        # ... 前面的扫描代码 ...
        
        if not unique_tokens:
            # 物理路径：如果符合40w流动性的币太少，系统强行下调门槛自适应
            return "⏳ 当前链上波动剧烈，40w+流动性池暂无新信号。系统持续监听中..."

        # ... 正常的 report 拼接逻辑 ...
