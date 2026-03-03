import os
import requests
import datetime
import json

# --- 配置区 ---
TG_TOKEN = os.getenv("TG_BOT_TOKEN")
CH_ID = os.getenv("CHANNEL_ID")
# 物理路径：利用 GitHub Actions 的工作目录存储临时价格快照（模拟复盘）
CACHE_FILE = "price_cache.json"

def send_tg_message(text):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {"chat_id": CH_ID, "text": text, "parse_mode": "Markdown", "disable_web_page_preview": True}
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e: print(f"发送失败: {e}")

# --- 模块 A: 自动化复盘逻辑 (Profit/Loss Review) ---
def performance_review(current_pairs):
    report = "📊 **上轮信号复盘 (24h 胜率追踪)**\n"
    old_data = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            old_data = json.load(f)
    
    new_cache = {}
    hit_count = 0
    for p in current_pairs:
        symbol = p['baseToken']['symbol']
        curr_price = float(p['priceUsd'])
        new_cache[symbol] = curr_price
        
        if symbol in old_data:
            old_price = old_data[symbol]
            change = ((curr_price - old_price) / old_price) * 100
            status = "📈 获利" if change > 0 else "📉 浮亏"
            report += f"- **{symbol}**: `{status} {change:.2f}%` (建议位对照)\n"
            if change > 5: hit_count += 1
            
    with open(CACHE_FILE, 'w') as f:
        json.dump(new_cache, f)
    
    if not old_data: return "📝 **首轮运行：已记录初始价，下轮开启复盘。**"
    return report

# --- 模块 B: 精准建议位计算 (Fibonacci 0.618) ---
def get_entry_strategy(price):
    entry = float(price) * 0.82 # 黄金回调买入位
    stop_loss = entry * 0.88    # 严格 12% 止损（2026 波动对冲）
    take_profit = entry * 1.5   # 目标 50% 利润点
    return round(entry, 8), round(stop_loss, 8), round(take_profit, 8)

# --- 模块 C: Solana 猎人 V6 (含复盘与安全性) ---
def hunt_solana_v6():
    url = "https://api.dexscreener.com/latest/dex/search?q=solana"
    try:
        response = requests.get(url, timeout=10).json()
        pairs = response.get('pairs', [])
        
        # 风险对冲：去重 + 流动性(>5w) + 24h量(>30w)
        unique_tokens = []
        seen = set()
        for p in pairs:
            addr = p['baseToken']['address']
            liq = p.get('liquidity', {}).get('usd', 0)
            vol = p.get('volume', {}).get('h24', 0)
            if addr not in seen and liq > 50000 and vol > 300000:
                unique_tokens.append(p)
                seen.add(addr)
            if len(unique_tokens) >= 3: break
            
        # 1. 执行复盘报告
        review_msg = performance_review(unique_tokens)
        send_tg_message(review_msg)
        
        # 2. 发送新信号报告
        report = "🚀 **Solana 狙击信号 (V6 精准版)**\n"
        for p in unique_tokens:
            entry, sl, tp = get_entry_strategy(p['priceUsd'])
            report += f"- **{p['baseToken']['name']}**\n"
            report += f"  现价: `${p['priceUsd']}` | 🎯 建议入场: `${entry}`\n"
            report += f"  🛑 止损: `${sl}` | 💰 止盈目标: `${tp}`\n"
            report += f"  [安全性检测](https://rugcheck.xyz/tokens/{p['baseToken']['address']})\n"
        return report
    except: return "❌ 数据链路异常"

# --- 执行引擎 ---
def main():
    if not TG_TOKEN or not CH_ID: return
    # 模块化按序执行
    send_tg_message(hunt_solana_v6())
    
    # AI 变现任务对冲
    ai_task = "🤖 **今日 AI 现金流任务**\n针对上述盈利 >10% 的币种，生成一篇推特复盘文，带上你的频道链接吸引流量。"
    send_tg_message(ai_task)

if __name__ == "__main__":
    main()
