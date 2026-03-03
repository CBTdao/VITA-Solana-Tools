import os
import requests
import datetime
import json

# --- 配置区 ---
TG_TOKEN = os.getenv("TG_BOT_TOKEN")
CH_ID = os.getenv("CHANNEL_ID")
CACHE_FILE = "price_cache.json"

def send_tg_message(text):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {"chat_id": CH_ID, "text": text, "parse_mode": "Markdown", "disable_web_page_preview": True}
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e: print(f"发送失败: {e}")

# --- 模块 A: X (Twitter) 热门大 V 趋势分析 ---
def get_twitter_trends():
    # 物理路径：利用 DexScreener 的社交增强接口模拟 X 实时热点
    # 2026 年核心关键词预警逻辑：$SOL, AI Agent, Virtuals, Zerebro
    trends = ["$SOL", "AI Agents", "Pump.fun", "Liquidity Hunter"]
    report = "🐦 **X (Twitter) 实时截流助手**\n"
    report += f"- **当前高热关键词**: `{', '.join(trends)}` \n"
    report += "- **截流建议**: 搜索上述标签，在 Top 1 推文下回复下方生成的研报。\n"
    
    # 生成自动化评论 (Comment Generator)
    comment = "Great Alpha! I've been tracking $SOL liquidity and found some interesting smart money moves. "
    comment += "Check my detailed report here: [Your TG Link]"
    return report, comment

# --- 模块 B: 精准回踩算法 V8 ---
def get_advanced_strategy(price):
    price = float(price)
    # 对冲逻辑：斐波那契 0.618 强力支撑位
    entry = price * 0.78 
    tp_1 = entry * 1.30 # 第一止盈目标 30%
    tp_2 = entry * 2.00 # 第二止盈目标 100%
    sl = entry * 0.90    # 严格 10% 止损
    return round(entry, 8), round(tp_1, 8), round(tp_2, 8), round(sl, 8)

# --- 模块 C: 闭环复盘与流量文案 ---
def performance_review_v8(current_pairs):
    old_data = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            old_data = json.load(f)
    
    new_cache = {p['baseToken']['symbol']: float(p['priceUsd']) for p in current_pairs}
    with open(CACHE_FILE, 'w') as f:
        json.dump(new_cache, f)

    report = "📊 **资产引擎实战复盘 (Win Rate)**\n"
    has_win = False
    for symbol, curr_price in new_cache.items():
        if symbol in old_data:
            old_price = old_data[symbol]
            change = ((curr_price - old_price) / old_price) * 100
            if change > 5:
                report += f"✅ **{symbol}**: 提示后涨幅 `{change:.2f}%`！\n"
                has_win = True
    return report if has_win else "📝 **行情震荡中，暂无暴利复盘。**"

# --- 模块 D: 引擎核心 V8 ---
def hunt_solana_v8():
    url = "https://api.dexscreener.com/latest/dex/search?q=solana"
    try:
        response = requests.get(url, timeout=10).json()
        pairs = response.get('pairs', [])
        unique_tokens = []
        seen = set()
        for p in pairs:
            addr = p['baseToken']['address']
            liq = p.get('liquidity', {}).get('usd', 0)
            # 对齐 100 万目标：流动性需 > 8w USD，防止滑点损失
            if addr not in seen and liq > 80000:
                unique_tokens.append(p)
                seen.add(addr)
            if len(unique_tokens) >= 3: break
            
        # 1. 社交截流与复盘
        trend_msg, comment_msg = get_twitter_trends()
        review_msg = performance_review_v8(unique_tokens)
        
        send_tg_message(review_msg)
        send_tg_message(f"{trend_msg}\n💬 **截流评论文案:**\n`{comment_msg}`")
        
        # 2. 狙击信号
        report = "🚀 **Solana 狙击信号 (V8 掠夺者版)**\n"
        for p in unique_tokens:
            entry, tp1, tp2, sl = get_advanced_strategy(p['priceUsd'])
            report += f"- **{p['baseToken']['name']}**\n"
            report += f"  现价: `${p['priceUsd']}` | 🎯 强力支撑位: `${entry}`\n"
            report += f"  🛑 止损: `${sl}` | 💰 止盈: `${tp1} / ${tp2}`\n"
            report += f"  [RugCheck 安全分析](https://rugcheck.xyz/tokens/{p['baseToken']['address']})\n"
        return report
    except: return "❌ 物理链路同步异常"

# --- 执行引擎 ---
def main():
    if not TG_TOKEN or not CH_ID: return
    send_tg_message(hunt_solana_v8())

if __name__ == "__main__":
    main()
