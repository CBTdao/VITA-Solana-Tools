import requests

def safe_div(n, d):
    return float(n) / float(d) if float(d) > 0 else 0

def analyze_token(addr):
    """核心审计穿透逻辑"""
    try:
        url = f"https://api.dexscreener.com/latest/dex/tokens/{addr}"
        res = requests.get(url, timeout=10).json()
        p = res.get('pairs', [{}])[0] if res.get('pairs') else {}
        
        liq = p.get('liquidity', {}).get('usd', 0)
        fdv = p.get('fdv', 0)
        
        score = 0
        tags = []
        
        # 1. 物理流动性对冲
        if liq > 300000: 
            score += 40
            tags.append("🛡
