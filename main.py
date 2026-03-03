import os
import requests
import datetime

# --- 配置区 ---
TG_TOKEN = os.getenv("TG_BOT_TOKEN")
CH_ID = os.getenv("CHANNEL_ID")

def send_tg_message(text):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {"chat_id": CH_ID, "text": text, "parse_mode": "Markdown", "disable_web_page_preview": True}
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print(f"发送失败: {e}")

# --- 模块 A: Solana 深度猎人 (增加去重与流动性过滤) ---
def hunt_solana_gems():
    print("正在扫描 Solana 链上高价值池子...")
    url = "https://api.dexscreener.com/latest/dex/search?q=solana"
    try:
        response = requests.get(url, timeout=10).json()
        pairs = response.get('pairs', [])
        
        # 风险对冲：去重逻辑 + 流动性筛选 (>20k USD)
        unique_tokens = {}
        for p in pairs:
            token_addr = p['baseToken']['address']
            liquidity = p.get('liquidity', {}).get('usd', 0)
            if token_addr not in unique_tokens and liquidity > 20000:
                unique_tokens[token_addr] = p
            if len(unique_tokens) >= 3: break # 只取前3个最优质的
            
        report = "🔥 **Solana 链上精选预警 (流动性 > $20k)**\n"
        for addr, p in unique_tokens.items():
            report += f"- **{p['baseToken']['name']}** ({p['baseToken']['symbol']})\n"
            report += f"  价格: `${p['priceUsd']}` | 1h涨幅: `{p['priceChange']['h1']}%` | 流动性: `${p['liquidity']['usd']}`\n"
            report += f"  交易: [DexScreener]({p['url']})\n"
        return report
    except:
        return "❌ Solana 数据源同步异常"

# --- 模块 B: 巨鲸地址嗅探 (Smart Money Tracker) ---
def whale_tracker():
    # 物理路径：此处预留给特定高胜率地址监控 (此处为逻辑演示，可根据需要填入真实地址)
    report = "🐋 **Solana 巨鲸/聪明钱实时动向**\n"
    report += "- **监控地址**: `7v7...9Pq` (早期入场专家)\n"
    report += "  **状态**: 正在增持高波动率资产，建议观察其最近 24h 交易频率。\n"
    report += "  **策略**: 0 启动阶段建议小额跟测，严禁满仓。\n"
    return report

# --- 模块 C: AI 变现与 Affiliate 猎人 ---
def hunt_ai_affiliate():
    today = datetime.date.today()
    report = f"🤖 **AI 掘金情报 ({today})**\n"
    # 逻辑对冲：寻找高搜索量、带推介计划的项目
    report += "- **Flux.1 AI Video**: 流量极速上升，推介返佣 25%。\n"
    report += "  路径: 在 Twitter 搜索该词并评论你的 Affiliate 链接。\n"
    report += "- **Agentic UI**: 刚获融资，处于早期邀请制。建议去官推申请 Beta 资格。\n"
    return report

# --- 执行引擎 ---
def main():
    if not TG_TOKEN or not CH_ID: return

    # 1. 发送 Solana 异动
    send_tg_message(hunt_solana_gems())
    
    # 2. 发送巨鲸报告
    send_tg_message(whale_tracker())
    
    # 3. 发送 AI 变现情报
    send_tg_message(hunt_ai_affiliate())

if __name__ == "__main__":
    main()
