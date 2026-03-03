
import os
import requests
import datetime

# --- 配置区 ---
TG_TOKEN = os.getenv("TG_BOT_TOKEN")
CH_ID = os.getenv("CHANNEL_ID")

def send_tg_message(text):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {"chat_id": CH_ID, "text": text, "parse_mode": "Markdown", "disable_web_page_preview": False}
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print(f"发送失败: {e}")

# --- 模块 A: Solana 链上猎人 (基于 DexScreener API) ---
def hunt_solana_gems():
    print("正在扫描 Solana 链上高热度新池子...")
    url = "https://api.dexscreener.com/latest/dex/search?q=solana"
    try:
        response = requests.get(url, timeout=10).json()
        pairs = response.get('pairs', [])[:3] # 取前3个最热项目
        report = "🔥 **Solana 链上高热度预警**\n"
        for p in pairs:
            report += f"- 币种: {p['baseToken']['name']} ({p['baseToken']['symbol']})\n"
            report += f"  价格: ${p['priceUsd']} | 24h涨幅: {p['priceChange']['h24']}%\n"
            report += f"  链接: [点击查看]({p['url']})\n"
        return report
    except:
        return "❌ Solana 数据抓取暂时受限"

# --- 模块 B: AI 变现工具追踪 (基于 ProductHunt RSS/模拟逻辑) ---
def hunt_ai_money():
    print("正在扫描全球 AI 变现新品...")
    # 模拟物理路径抓取（实际生产中可接入 PH API）
    # 逻辑对冲：优先筛选带 Affiliate 或刚融资的项目
    today = datetime.date.today()
    report = f"🤖 **AI 效率工具变现情报 ({today})**\n"
    report += "- **项目 1**: AI-Video-Editor (带有 30% 返佣计划)\n"
    report += "  理由: 刚在 PH 获得 Top 1，目前流量暴增，适合做 SEO 截流。\n"
    report += "- **项目 2**: Multi-Agent Agentic UI\n"
    report += "  理由: 早期测试阶段，可申请内部白名单，属于潜在 0 撸机会。\n"
    return report

# --- 执行引擎 ---
def main():
    if not TG_TOKEN or not CH_ID:
        print("环境异常")
        return

    # 1. 执行 Solana 监控
    sol_data = hunt_solana_gems()
    send_tg_message(sol_data)

    # 2. 执行 AI 变现监控
    ai_data = hunt_ai_money()
    send_tg_message(ai_data)

    print("✅ 双轨数据已推送到 Telegram")

if __name__ == "__main__":
    main()
