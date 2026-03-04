import requests
import os
import json
import time

# ================= 物理配置区 =================
# 建议：GitHub Secrets 中必须包含 TELEGRAM_TOKEN 和 TELEGRAM_CHAT_ID
TG_TOKEN = os.getenv('TELEGRAM_TOKEN')
TG_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# 门槛对冲：下调至 10w，既能抓到新币，又能过滤极端垃圾
MIN_LIQUIDITY = 100000 
# =============================================

def fetch_solana_alpha():
    """
    通过物理链路抓取 Solana 实时数据
    """
    url = "https://api.dexscreener.com/latest/dex/search?q=solana"
    print(f"[{time.strftime('%H:%M:%S')}] 物理扫描启动，阈值: ${MIN_LIQUIDITY}")
    
    try:
        # 设置 15 秒物理超时，对冲网络波动
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            print(f"❌ API 链路异常: HTTP {response.status_code}")
            return []
            
        data = response.json()
        pairs = data.get('pairs', [])
        print(f"📡 API 返回了 {len(pairs)} 个待审计交易对")
        
        results = []
        for p in pairs:
            # 1. 物理层过滤：必须是 Solana 链
            if p.get('chainId') != 'solana':
                continue
                
            # 2. 数据层过滤：流动性审计
            liq = float(p.get('liquidity', {}).get('usd', 0))
            symbol = p.get('baseToken', {}).get('symbol', 'Unknown')
            
            # 调试日志：在 Actions 中可以看到每个接近门槛的币
            if liq > 50000:
                print(f"🔍 审计中: {symbol} | 流动性: ${liq:,.0f}")

            if liq >= MIN_LIQUIDITY:
                # 3. 策略层过滤：排除原生 SOL，只抓取潜在 Alpha
                if symbol not in ['SOL', 'WSOL']:
                    results.append({
                        "name": symbol,
                        "liq": liq,
                        "price": p.get('priceUsd', '0'),
                        "vol_24h": p.get('volume', {}).get('h24', 0),
                        "url": p.get('url')
                    })
        return results

    except Exception as e:
        print(f"🚨 物理读取崩溃: {str(e)}")
        return []

def deliver_signal(signal):
    """
    物理投递：将审计结果推送到 TG -> Make.com -> X
    """
    if not TG_TOKEN or not TG_CHAT_ID:
        print("❌ 缺失物理密钥：请检查 GitHub Secrets 配置")
        return

    # 构造 Markdown 格式报告
    report = (
        f"🚨 *Solana Alpha 审计通过*\n\n"
        f"💎 代币: #{signal['name']}\n"
        f"💰 流动性: ${signal['liq']:,.0f}\n"
        f"📊 24h成交: ${signal['vol_24h']:,.0f}\n"
        f"💵 价格: ${signal['price']}\n\n"
        f"🔗 [在 DexScreener 查看]({signal['url']})"
    )

    tg_url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    try:
        res = requests.post(tg_url, json={
            "chat_id": TG_CHAT_ID,
            "text": report,
            "parse_mode": "Markdown",
            "disable_web_page_preview": False
        }, timeout=10)
        
        if res.status_code == 200:
            print(f"✅ 成功投递信号: {signal['name']}")
        else:
            print(f"⚠️ 投递失败: {res.text}")
    except Exception as e:
        print(f"🚨 投递物理报错: {e}")

if __name__ == "__main__":
    found_signals = fetch_solana_alpha()
    print(f"--- 审计结束，最终过滤出 {len(found_signals)} 个高价值信号 ---")
    
    for sig in found_signals:
        deliver_signal(sig)
        # 物理间隔，防止 TG 频率限制
        time.sleep(1)
