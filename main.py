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

# --- 模块 A: 社交真伪嗅探 (Scam Detection) ---
def social_authenticity_check(pair_data):
    info = pair_data.get('info', {})
    socials = info.get('socials', [])
    websites = info.get('websites', [])
    
    # 风险对冲逻辑：
    # 1. 无官网 -> 极高风险
    # 2. 无推特 -> 极高风险
    # 3. 只有 Telegram -> 疑似土狗
    has_twitter = any(s.get('type') == 'twitter' for s in socials)
    has_web = len(websites) > 0
    
    if not has_twitter or not has_web:
        return "⚠️ 社交孤儿(无推特/官网)，严禁截流！", False
    return "✅ 社交链路完整", True

# --- 模块 B: 狙击位计算 (V9 策略) ---
def get_v9_strategy(price):
    price = float(price)
    # 逻辑对冲：针对 2026 波动率，回踩 25% 是安全边际
    entry = price * 0.75 
    tp_1 = entry * 1.50 # 50% 止盈
    sl = entry * 0.85    # 15% 止损
    return round(entry, 8), round(tp_1, 8), round(sl, 8)

# --- 模块 C: 闭环复盘与流量文案 ---
def performance_review_v9(current_pairs):
    old_data = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            old_data = json.load(f)
    
    new_cache = {p['baseToken']['symbol']: float(p['priceUsd']) for p in current_pairs}
    with open(CACHE_FILE, 'w') as f:
        json.dump(new_cache, f)

    report = "📊 **实战盈亏复盘 (V9)**\n"
    has_win = False
    for symbol, curr_price in new_cache.items():
        if symbol in old_data:
            old_price = old_data[symbol]
            change = ((curr_price - old_price) / old_price) * 100
            if change > 5:
                report += f"🔥 **{symbol}**: 利润 `{change:.2f}%` \n"
                has_win = True
    return report if has_win else "📝 **行情冷却中...**"

# --- 模块 D: 引擎核心 V9 ---
def hunt_solana_v9():
    url = "https://api.dexscreener.com/latest/dex/search?q=solana"
    try:
        response = requests.get(url, timeout=10).json()
        pairs = response.get('pairs', [])
        unique_tokens = []
        seen = set()
        
        for p in pairs:
            addr = p['baseToken']['address']
            liq = p.get('liquidity', {}).get('usd', 0)
            # 对齐 100 万目标：流动性提升至 10w USD (确保大仓位出入)
            if addr not in seen and liq > 100000:
                unique_tokens.append(p)
                seen.add(addr)
            if len(unique_tokens) >= 3: break
            
        # 1. 复盘
        review_msg = performance_review_v9(unique_tokens)
        send_tg_message(review_msg)
        
        # 2. 狙击报告
        report = "🛡️ **Solana 安全狙击报告 (V9 护城河版)**\n"
        for p in unique_tokens:
            social_status, is_safe = social_authenticity_check(p)
            # 只有社交链路完整的项目才进行策略推送
            if is_safe:
                entry, tp1, sl = get_v9_strategy(p['priceUsd'])
                report += f"- **{p['
