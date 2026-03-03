import os
import requests
import datetime

# --- 1. 配置区 (100万目标唯一路径) ---
TG_TOKEN = os.getenv("TG_BOT_TOKEN")
CH_ID = os.getenv("CHANNEL_ID")
MY_WALLET = "CjBusumcVax2DtzLWVMd6KKXSHDeV7tbNRYdaVHL5SJf"

def send_tg_message(text):
    if not TG_TOKEN or not CH_ID: return
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {"chat_id": CH_ID, "text": text, "parse_mode": "Markdown", "disable_web_page_preview": True}
    try:
        requests.post(url, data=payload, timeout=15)
    except: pass

# --- 2. 变现逻辑引擎 (恢复今日任务) ---
def get_daily_monetization_task():
    tasks = [
        "截图当前高分币，去推特搜索 $SOL 话题进行‘专业审计式’截流回复。",
        "检查钱包地址是否有打赏流入，若无，则手动转发一条盈利复盘到频道。",
        "在 X 上关注 3 个 Solana 链大 V，将 Bot 发现的信号第一时间 @ 他们。",
        "分析今日推送中涨幅最大的币种，总结其‘起飞前’的流动性特征。"
    ]
    # 根据日期轮换任务，确保 0 启动的执行连续性
    day_index = datetime.datetime.now().day % len(tasks)
    return tasks[day_index]

# --- 3. 核心扫描引擎 (V23.1 纯净稳定版) ---
def hunt_solana_v23():
    url = "https://api.dexscreener.com/latest/dex/search?q=solana"
    try:
        response = requests.get(url, timeout=20).json()
        pairs = response.get('pairs', [])
        unique_tokens = []
        seen = set()
        
        for p in pairs:
            liq = float(p.get('liquidity', {}).get('usd', 0))
            addr = p.get('baseToken', {}).get('address', '')
            if addr not in seen and liq > 400000:
                unique_tokens.append(p)
                seen.add(addr)
            if len(unique_tokens) >= 3: break
            
        if not unique_tokens:
            return "⏳ 系统扫描中，暂无符合 40w+ 流动性的高安全信号。"

        # --- 物理拼接变现情报 ---
        report = f"💎 **AI 变现 0 启动系统 (V23.1.3)**\n"
        report += f"📅 日期：2026-03-03 | 状态：收割中\n"
        report += f"---"
        report += f"\n💰 **变现情报**：当前 Solana 链大额池活跃，适合‘安全审计’类引流。"
        report += f"\n📝 **今日任务**：{get_daily_monetization_task()}\n"
        report += f"---\n\n"
        
        for p in unique_tokens:
            sym = p['baseToken']['symbol']
            price = p.get('priceUsd', '0')
            report += f"📍 **{sym}**\n"
            report += f"  💰 流动性: `${int(float(p['liquidity']['usd'])):,}`\n"
            report += f"  🎯 现价: `${price}`\n"
            report += f"  💳 佣金打赏: `{MY_WALLET}`\n"
            report += f"  [查看行情]({p['url']})\n\n"
            
        return report
    except Exception as e:
        return f"❌ 扫描异常: {str(e)[:30]}"

def main():
    content = hunt_solana_v23()
    send_tg_message(content)

if __name__ == "__main__":
    main()
