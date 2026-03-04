import requests
import os
import json
import time

# ================= 物理配置区 =================
# 确保 GitHub Secrets 中已配置 TELEGRAM_TOKEN 和 TELEGRAM_CHAT_ID
TG_TOKEN = os.getenv('TELEGRAM_TOKEN')
TG_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# 为了今天“破冰”验证，阈值降至 3w
MIN_LIQUIDITY = 30000 
# =============================================

def fetch_solana_alpha():
    """
    抓取 Solana 数据并进行阶梯式审计
    """
    url = "https://api.dexscreener.com/latest/dex/search?q=solana"
    print(f"[{time.strftime('%H:%M:%S')}] 物理扫描启动，当前探测门槛: ${MIN_LIQUIDITY}")
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            print(f"❌ API 物理链路故障: HTTP {response.status_code}")
            return []
            
        data = response.json()
        pairs = data.get('pairs', [])
        print(f"📡 成功接入 API，探测到 {len(pairs)} 个待审计对")
        
        results = []
        # 对冲干扰项：物理排除稳定币和原生 SOL
        exclude_list = ['SOL', 'WSOL', 'USDC', 'USDT', 'UXD']
        
        max_seen_liq = 0
        
        for p in pairs:
            if p.get('chainId') != 'solana':
                continue
                
            liq = float(p.get('liquidity', {}).get('usd', 0))
            symbol = p.get('baseToken', {}).get('symbol', 'Unknown')
            
            # 更新探测到的最高流动性（非排除币种）
            if symbol.upper() not in exclude_list:
                max_seen_liq = max(max_seen_liq, liq)

            # 物理审计逻辑
            if liq >= MIN_LIQUIDITY:
                if symbol.upper() not in exclude_list:
                    print(f"✅ 审计通过: {symbol} (Liq: ${liq:,.0f})")
                    results.append({
                        "name": symbol,
                        "liq": liq,
                        "price": p.get('priceUsd', '0'),
                        "vol_24h": p.get('volume', {}).get('h24', 0),
                        "url": p.get('url')
                    })
        
        if not results:
            print(f"ℹ️ 审计未通过。当前市场非 SOL 最高流动性为: ${max_seen_liq:,.0f} (距门槛还差 ${MIN_LIQUIDITY - max_seen_liq:,.0f})")
            
        return results

    except Exception as e:
        print(f"🚨 物理读取崩溃: {str(e)}")
        return []

def deliver_signal(signal):
    """
    物理投递：TG -> Make.com -> Twitter
    """
    if not TG_TOKEN or not TG_CHAT_ID:
        print("❌ 缺失物理密钥：请检查 GitHub Secrets")
        return

    # 针对 Make.com 的数据映射进行文案优化
    report = (
        f"🚨 *Alpha 审计通过 (3w+)*\n\n"
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
            print(f"🚀 物理信号已发射: {signal['name']}")
        else:
            print
