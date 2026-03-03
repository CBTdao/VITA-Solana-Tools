import os
import requests
import json

# --- 配置区 (从 GitHub Secrets 获取) ---
TG_TOKEN = os.getenv("TG_BOT_TOKEN")
CH_ID = os.getenv("CHANNEL_ID")

def get_high_value_data():
    """
    物理路径：监控 ProductHunt 或特定聚合器
    目标：寻找具有 Affiliate 计划或 0 成本套利潜力的项目
    """
    # 示例：抓取具有高增长潜力的 AI 变现工具数据接口
    # 实际应用中可替换为特定的 RSS 或 API
    target_url = "https://api.producthunt.com/v2/posts" # 需申请免费 Developer Token
    
    # 演示用的简化路径：抓取 GitHub 上的 Earn-related 热门仓库
    search_url = "https://api.github.com/search/repositories?q=make+money+automation+stars:>50&sort=updated"
    
    try:
        resp = requests.get(search_url, timeout=10)
        items = resp.json().get('items', [])
        return items[:3] # 每次只推最精选的 3 个
    except Exception as e:
        print(f"数据源风险对冲：主接口异常，切换备用源... {e}")
        return []

def refine_content(item):
    """
    逻辑加工：将原始数据转化为“盈利指南”格式
    """
    name = item.get('name')
    desc = item.get('description', '无描述')
    url = item.get('html_url')
    
    # 自动化改写模板
    report = (
        f"🚀 **发现潜在变现机会**\n\n"
        f"项目名称：{name}\n"
        f"核心逻辑：{desc}\n"
        f"物理路径：{url}\n"
        f"⚠️ 风险对冲：建议先进行 0 成本测试，切勿投入本金。"
    )
    return report

def send_to_tg(text):
    """
    分发终端：确保信息触达
    """
    if not TG_TOKEN: return
    api_url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {"chat_id": CH_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(api_url, data=payload)

if __name__ == "__main__":
    data = get_high_value_data()
    for entry in data:
        content = refine_content(entry)
        send_to_tg(content)
