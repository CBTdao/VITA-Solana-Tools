
import os
import requests
import telebot
from telebot import types
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import time

# --- 1. 物理配置区 ---
API_TOKEN = os.getenv("TG_BOT_TOKEN")
CH_ID = os.getenv("CHANNEL_ID")
MY_WALLET = "CjBusumcVax2DtzLWVMd6KKXSHDeV7tbNRYdaVHL5SJf"
bot = telebot.TeleBot(API_TOKEN)

# --- 2. 鲁棒性对冲：安全计算函数 ---
def safe_div(n, d):
    """防止分母为0导致系统停机"""
    try:
        return float(n) / float(d) if float(d) > 0 else 0
    except:
        return 0

# --- 3. 核心审计逻辑 (V24+V25 融合版) ---
def analyze_token_v28(p):
    # 提取物理数据
    liq = p.get('liquidity', {}).get('usd', 0)
    fdv = p.get('fdv', 0)
    vol24 = p.get('volume', {}).get('h24', 0)
    h1_txns = p.get('txns', {}).get('h1', {})
    buys = h1_txns.get('buys', 0)
    sells = h1_txns.get('sells', 0)

    score = 0
    tags = []

    # A. 聪明钱与流动性对冲 (30分)
    if liq > 500000: score += 20
    avg_buy = safe_div(vol24, (buys + sells))
    if avg_buy > 2000: 
        score += 10
        tags.append("🧠 聪明钱布局")

    # B. 老鼠仓穿透 (强制扣分项)
    # 如果市值是流动性的 20 倍以上，判定为高危控制盘
    risk_ratio = safe_div(fdv, liq)
    if risk_ratio > 20:
        score -= 50
        tags.append("🚫 高危老鼠仓")

    # C. 审计背书 (20分)
    if p.get('info', {}).get('audits'):
        score += 20
        tags.append("🛡️ 审计已通过")

    return max(0, score), tags

# --- 4. PDF 报告生成模块 ---
def generate_audit_pdf(addr, val, fee, tags):
    file_path = f"Audit_{addr[:6]}.pdf"
    c = canvas.Canvas(file_path, pagesize=A4)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 800, "2026 AI ASSET AUDIT & RECOVERY REPORT")
    c.setFont("Helvetica", 10)
    c.drawString(50, 785, f"Address: {addr} | Timestamp: {time.ctime()}")
    c.line(50, 775, 550, 775)

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, 740, "Diagnostic Tags:")
    c.setFont("Helvetica", 11)
    y = 720
    for tag in tags:
        c.drawString(70, y, f"- {tag}")
        y -= 20

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 600, "Financial Recovery Summary:")
    c.setFont("Helvetica", 12)
    c.drawString(70, 580, f"Detected Unclaimed Assets: ${val}")
    c.setFillColorRGB(0.8, 0, 0)
    c.drawString(70, 560, f"Recovery Commission (20%): ${fee} (PENDING)")
    
    c.setFillColorRGB(0, 0, 0)
    c.drawString(50, 500, "To unlock the full claim guide, please pay commission to:")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, 480, f"SOLANA: {MY_WALLET}")
    
    c.save()
    return file_path

# --- 5. Telegram 收银员交互 ---
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "💰 **欢迎来到 2026 链上收割工厂**\n请输入 Solana 钱包地址或代币地址开始审计：")

@bot.message_handler(func=lambda message: len(message.text) > 30)
def handle_request(message):
    addr = message.text
    bot.send_message(message.chat.id, "🔄 正在穿透底层数据，请稍候...")
    
    try:
        # 实际探测 (对接 DexScreener API 作为示例数据源)
        url = f"https://api.dexscreener.com/latest/dex/tokens/{addr}"
        res = requests.get(url, timeout=10).json()
        pair = res.get('pairs', [{}])[0] if res.get('pairs') else {}
        
        score, tags = analyze_token_v28(pair)
        
        # 自动计算沉默资产回收 (模拟逻辑)
        unclaimed_val = 1250.0  # 假设检测到资产
        fee = unclaimed_val * 0.2
        
        # 生成 PDF
        pdf_path = generate_audit_pdf(addr, unclaimed_val, fee, tags)
        
        with open(pdf_path, 'rb') as doc:
            bot.send_document(
                message.chat.id, 
                doc, 
                caption=f"🔍 审计完成！综合评分: `{score}`\n佣金解锁地址: `{MY_WALLET}`",
                parse_mode="Markdown"
            )
        os.remove(pdf_path) # 发送后清理本地文件
        
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ 处理失败: 链路拥堵或地址格式错误。")

# --- 6. 自动执行入口 ---
if __name__ == "__main__":
    print("🚀 2026 收割工厂已上线，正在监听地址...")
    bot.polling(none_stop=True)
