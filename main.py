import requests
import os
import time
import json

# ================= 物理配置 (GitHub Secrets 需配置) =================
TG_TOKEN = os.getenv('TG_BOT_TOKEN')
TG_CHAT_ID = os.getenv('CHANNEL_ID')

# 模块化对冲：即使库安装失败也能运行基础逻辑
try:
    import feedparser
except ImportError:
    feedparser = None

class GlobalAlphaEngine:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    def fetch_digital_labor_jobs(self):
        """探测源 A：全球 AI 劳务高薪订单 (示例使用公开科技资讯，可替换为私有 RSS)"""
        # 建议洗澡后替换为你自己的 Upwork/Fiverr RSS 链接
        rss_url = "https://news.google.com/rss/search?q=AI+Automation+Jobs+remote&hl=en-US&gl=US&ceid=US:en"
        
        if not feedparser:
            return []
        
        try:
            feed = feedparser.parse(rss_url)
            results = []
            # 过滤高价值关键词
            KEYWORDS = ["AI", "Automation", "Python", "Bot", "Integration"]
            for entry in feed.entries[:3]: 
                if any(kw.lower() in entry.title.lower() for kw in KEYWORDS):
                    results.append({
                        "type": "劳务/商机溢价",
                        "title": entry.title,
                        "link": entry.link
                    })
            return results
        except Exception as e:
            print(f"劳务探测异常: {e}")
            return []

    def fetch_market_anomaly(self):
        """探测源 B：市场物理异常 (稳定币脱钩预警，保护 100 万资产安全)"""
        url = "https://api.binance.com/api/v3/ticker/price?symbol=USDCUSDT"
        try:
            res = self.session.get(url, timeout=10).json()
            price = float(res['price'])
            # 物理逻辑：脱钩超过 0.3% 立即报警
            if price > 1.003 or price < 0.997:
                return [{
                    "type": "资产脱钩预警",
                    "title": f"⚠️ 稳定币风险! 当前价格: {price}",
                    "link": "https://www.binance.com/zh-CN/trade/USDC_USDT"
                }]
        except:
            pass
        return []

    def deliver_signal(self, alpha):
        """物理投递：确保文本结构化，便于 Make.com 识别"""
        report = (
            f"🌐 [GLOBAL_ALPHA_SIGNAL]\n"
            f"TYPE: {alpha['type']}\n"
            f"INFO: {alpha['title']}\n"
            f"PATH: {alpha['link']}\n"
            f"TIME: {time.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
        try:
            resp = self.session.post(url, json={
                "chat_id": TG_CHAT_ID,
                "text": report,
                "disable_web_page_preview": False
            }, timeout=10)
            if resp.status_code == 200:
                print(f"✅ 信号物理发射成功: {alpha['title'][:20]}...")
        except Exception as e:
            print(f"🚨 投递物理崩溃: {e}")

if __name__ == "__main__":
    engine = GlobalAlphaEngine()
    print(f"[{time.strftime('%H:%M:%S')}] 百万资产引擎 2.0 启动审计...")
    
    # 组合探测结果
    all_alphas = engine.fetch_digital_labor_jobs() + engine.fetch_market_anomaly()
    
    # 物理心跳逻辑：如果没有任何信号，也发一个状态，确保你确认链路通畅
    if not all_alphas:
        all_alphas.append({
            "type": "系统心跳",
            "title": "全球机会监控中：暂未发现显著溢价",
            "link": "https://github.com"
        })
    
    for alpha in all_alphas:
        engine.deliver_signal(alpha)
        time.sleep(2)
