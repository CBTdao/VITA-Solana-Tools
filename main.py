import os
import requests

# 100万目标自动化引擎 - 诊断版
def run_diagnostic():
    token = os.getenv("TG_BOT_TOKEN")
    chat_id = os.getenv("CHANNEL_ID")
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": "🚨 自动化引擎测试：通道已激活。若收到此消息，请确认下一步指令。",
    }
    
    print(f"--- 正在执行物理路径测试 ---")
    try:
        response = requests.post(url, data=payload)
        result = response.json()
        
        if result.get("ok"):
            print("✅ 成功！消息已发出。请检查频道。")
        else:
            # 这里的输出将直接告诉你为什么“只读不回”
            print(f"❌ 失败原因: {result.get('description')}")
            print(f"错误码: {result.get('error_code')}")
    except Exception as e:
        print(f"🔥 系统崩溃风险：{str(e)}")

if __name__ == "__main__":
    run_diagnostic()
