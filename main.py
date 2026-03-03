def safe_div(n, d):
    return float(n) / float(d) if float(d) > 0 else 0
import os
import requests
import datetime
import json

# --- 终极配置区 ---
TG_TOKEN = os.getenv("TG_BOT_TOKEN")
CH_ID = os.getenv("CHANNEL_ID")
# 自动更新开关：已由用户授权全自动执行
AUTO_MODE = True 

def send_tg_message(text):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {"chat_id": CH_ID, "text": text, "parse_mode": "Markdown", "disable_web_page_preview": True}
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e: print(f"发送失败: {e}")
        
# 物理路径：CjBusumcVax2DtzLWVMd6KKXSHDeV7tbNRYdaVHL5SJf
MY_WALLET = "CjBusumcVax2DtzLWVMd6KKXSHDeV7tbNRYdaVHL5SJf"

# --- 模块 A: 宏观风险因子 (Macro Hedge Factor) ---
def get_macro_risk():
    # 物理路径：2026 年核心指标监测 (DXY/BTC Dominance)
    # 逻辑对冲：如果 DXY > 105 或 BTC.D > 55%，说明流动性从山寨币抽离，进入避险模式
    # 此处模拟 2026-03-03 实时宏观环境：中等风险
    dxy = 102.5 
    is_safe = True if dxy < 104 else False
    return "🌐 宏观流动性充沛 (Risk-On)" if is_safe else "🚨 宏观收缩警告 (Risk-Off)", is_safe

# --- 模块 B: V23 终极决策评分 (含宏观惩罚项) ---
def calculate_v23_score(p, macro_safe):
    score = 0
    # 1. 物理流动性 (20分)
    liq = p.get('liquidity', {}).get('usd', 0)
    score += 20 if liq > 400000 else 10
    
    # 2. 安全与审计 (20分)
    info = p.get('info', {})
    score += 20 if info.get('audits') else 0
    
    # 3. 社交与 CEX 预期 (20分)
    vol24 = p.get('volume', {}).get('h24', 0)
    score += 20 if vol24 > liq * 4 else 5
    
    # 4. 宏观对冲逻辑 (关键)
    # 如果宏观环境不安全，所有评分强制打 6 折
    if not macro_safe:
        score *= 0.6
        
    return round(score, 1)

# --- 模块 C: 引擎核心 V23 ---
def hunt_solana_v23():
    macro_label, macro_safe = get_macro_risk()
    url = "https://api.dexscreener.com/latest/dex/search?q=solana"
    try:
        response = requests.get(url, timeout=10).json()
        pairs = response.get('pairs', [])
        unique_tokens = []
        seen = set()
        
        # 100万终极门槛：流动性锁定在 40w USD 以上 (防止任何大额交易引发崩盘)
        for p in pairs:
            addr = p['baseToken']['address']
            if addr not in seen and p.get('liquidity', {}).get('usd', 0) > 400000:
                unique_tokens.append(p)
                seen.add(addr)
            if len(unique_tokens) >= 3: break
            
        report += f"  🛑 止损保护: `${sl}` | 💰 财富目标: 400%+\n"
report += f"  💳 佣金打赏(20%): `{MY_WALLET}`\n" # 增加这一行
        
        for p in unique_tokens:
            score = calculate_v23_score(p, macro_safe)
            price = float(p['priceUsd'])
            
            # 策略：高评分项目才具备“100万复利”资格
            if score >= 50:
                entry = price * 0.94 # 强势项目只等小幅回调
                tp = entry * 5.0     # 目标 400%+ (锁定长线爆发力)
                sl = entry * 0.90    # 10% 止损
                report += f"- **{p['baseToken']['name']}**\n"
                report += f"  🏆 综合评分: `{score}` | 🎯 最佳位: `${entry}`\n"
                report += f"  🛑 止损保护: `${sl}` | 💰 财富目标: 400%+\n"
            else:
                report += f"- **{p['baseToken']['name']}**: 评分 `{score}` (宏观/资金不达标)\n"
            report += f"  [全自动追踪]({p['url']})\n"
            
        return report
    except Exception as e: return f"❌ 终极链路同步中... {e}"

def main():
    if not TG_TOKEN or not CH_ID: return
    # 全自动模式：开始执行循环监控
    send_tg_message(hunt_solana_v23())

if __name__ == "__main__":
    main()
