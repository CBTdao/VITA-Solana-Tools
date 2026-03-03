
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

# --- 模块 A: 自动化复盘与胜率统计 ---
def performance_review(current_pairs):
    old_data = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            old_data = json.load(f)
    
    new_cache = {p['baseToken']['symbol']: float(p['priceUsd']) for p in current_pairs}
    with open(CACHE_FILE, 'w') as f:
        json.dump(new_cache, f)

    report = "📊 **上轮信号复盘报告**\n"
    twitter_content = "🧵 **今日 Solana 链上实战复盘**\n\n"
    
    if not old_data:
        return "📝 **首轮运行：已锁定初始价，下一轮生成复盘推文。**", ""

    has_profit = False
    for symbol, curr_price in new_cache.items():
        if symbol in old_data:
            old_price = old_data[symbol]
            change = ((curr_price - old_price) / old_price) * 100
            status = "🚀" if change > 0 else "📉"
            report += f"- **{symbol}**: `{status} {change:.2f}%` \n"
            if change > 3: # 涨幅超过3%才发推
                twitter_content += f"{status} ${symbol} 提示后最高涨幅 {change:.2f}%\n"
                has_profit = True
    
    twitter_content += "\n🎯 更多聪明钱监控点位：加入我的 TG 频道获取 \n#Solana #AIAgent #Crypto"
    return report, twitter_content if has_profit else ""

# --- 模块 B: 精准策略计算 ---
def get_strategy(price):
    entry = float(price) * 0.82 # 建议买入位
    tp = entry * 1.5            # 止盈位
    sl = entry * 0.88           # 止损位
    return round(entry, 8), round(tp, 8), round(sl, 8)

# --- 模块 C: 资产引擎核心 V7 ---
def hunt_solana_v7():
    url = "https://api.dexscreener.com/latest/dex/search?q=solana"
    try:
        response = requests.get(url, timeout=10).json()
        pairs = response.get('pairs', [])
        unique_tokens = []
        seen = set()
        for p in pairs:
            addr = p['baseToken']['address']
            liq = p.get('liquidity', {}).get('usd', 0)
            if addr not in seen and liq > 50000:
                unique_tokens.append(p)
                seen.add(addr)
            if len(unique_tokens) >= 3: break
            
        # 1. 执行复盘并生成推文内容
        review_msg, tw_msg = performance_review(unique_tokens)
        send_tg_message(review_msg)
        
        if tw_msg:
            send_tg_message(f"📢 **推特自动营销文案已生成 (请手动/自动分发):**\n\n{tw_msg}")
        
        # 2. 发送新信号
        report = "🚀 **Solana 狙击信号 (V7 流量版)**\n"
        for p in unique_tokens:
            entry, tp, sl = get_strategy(p['priceUsd'])
            report += f"- **{p['baseToken']['name']}**\n"
            report += f"  现价: `${p['priceUsd']}` | 🎯 建议入场: `${entry}`\n"
            report += f"  🛑 止损: `${sl}` | 💰 止盈: `${tp}`\n"
            report += f"  [安全性检测](https://rugcheck.xyz/tokens/{p['baseToken']['address']})\n"
        return report
    except: return "❌ 数据链路异常"

# --- 执行引擎 ---
def main():
    if not TG_TOKEN or not CH_ID: return
    send_tg_message(hunt_solana_v7())

if __name__ == "__main__":
    main()
