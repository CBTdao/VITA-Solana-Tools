
import os
import requests

def fire_test():
    # 从系统获取变量
    token = os.getenv("TG_BOT_TOKEN")
    chat_id = os.getenv("CHANNEL_ID")
    
    print(f"--- 诊断开始 ---")
    print(f"Token 是否读取: {'已读取' if token else '未读取 (检查 Secrets)'}")
    print(f"Channel ID: {chat_id}")
    
    if not token or not chat_id:
        print("❌ 错误：环境变量缺失！请检查 GitHub Secrets 设置。")
        return

    # 尝试发送请求
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": "🔥 100M_Asset_Engine 物理路径测试成功！\n状态：通道已打通。\n下一步：开启 Solana 监控模式。"
    }
    
    try:
        response = requests.post(url, data=payload)
        data = response.json()
        if data.get("ok"):
            print("✅ 恭喜！消息已成功送达 Telegram。")
        else:
            print(f"❌ Telegram 返回错误: {data.get('description')}")
            print(f"错误码: {data.get('error_code')}")
    except Exception as e:
        print(f"🔥 系统崩溃: {str(e)}")

if __name__ == "__main__":
    fire_test()
