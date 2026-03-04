import requests
import os
import time
import json

# ================= 物理配置 (必须在 GitHub Secrets 配置) =================
TG_TOKEN = os.getenv('TG_BOT_TOKEN')
TG_CHAT_ID = os.getenv('CHANNEL_ID')

# 风险对冲：即使 RSS 库安装失败，脚本也能通过 API 运行
try:
    import feedparser
except ImportError:
    feedparser = None

class GlobalAlphaEngine:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    def fetch_digital_labor_jobs(self):
        """探测源 A：全球 AI 劳务高薪订单 (Upwork 示例)"""
        # 这里使用一个公开的 RSS 聚合，你可以替换为你的定制 RSS
        rss_url = "https://www.upwork.com/ab/feed/jobs/rss?q=python+ai+automation&sort=recency"
        if not feedparser:
            return [{"title": "系统提醒", "link": "请在 requirements.txt 加入 feedparser"}]
        
        try:
            feed = feedparser.parse(rss_url)
            results = []
            for entry in feed.entries[:5]: # 仅取最新的 5 条
                results.append({
                    "type": "劳务溢价",
                    "title": entry.title,
                    "link": entry.link
                })
            return results
        except:
            return []

    def fetch_market_anomaly(self):
        """探测源 B：市场异常波动 (如法币/稳定币脱钩报警)"""
        # 物理路径：通过 Binance API 监控汇率异常
        url = "https://api.binance.com/api/v3/ticker/price?symbol=USDCUSDT"
        try:
            res = self.session.get(url, timeout=10).json()
            price = float(res['price'])
            # 风险对冲逻辑：如果 USDC/USDT 脱钩超过 0.5%，立即报警
            if price > 1.005 or price < 0.995:
                return [{
                    "type": "资产脱钩",
                    "title": f"⚠️ 稳定币异常: {price}",
                    "link": "https://www.binance.com/zh-CN/trade/USDC_USDT"
                }]
        except:
            pass
        return []

    def deliver_signal(self, alpha):
        """物理投递：确保 Make.com 能 100% 识别的格式"""
        report = (
            f"🌐 [GLOBAL_ALPHA_SIGNAL]\n"
            f"类型: {alpha['type']}\n"
            f"描述: {alpha['title']}\n"
            f"路径: {alpha['link']}\n"
            f"时间: {time.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
        try:
            self.session.post(url, json={
                "chat_id": TG_CHAT_ID,
                "text": report,
                "disable_web_page_preview": False
            }, timeout=10)
            print(f"✅ 已成功发射信号: {alpha['title']}")
        except Exception as e:
            print(f"🚨 投递物理崩溃: {e}")

if __name__ == "__main__":
    engine = GlobalAlphaEngine()
    print(f"[{time.strftime('%H:%M:%S')}] 百万资产引擎 2.0 启动...")
    
    # 执行多维扫描
    all_alphas = engine.fetch_digital_labor_jobs() + engine.fetch_market_anomaly()
    
    if not all_alphas:
        print("--- 物理审计结束：未发现显著套利机会 ---")
    else:
        for alpha in all_alphas:
            engine.deliver_signal(alpha)
            time.sleep(2) # 物理对冲 TG 频率限制
