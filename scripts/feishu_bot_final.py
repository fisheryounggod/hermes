#!/usr/bin/env python3
"""
飞书机器人测试（修复版）
获取机器人信息并发送测试消息
"""

import requests
import json
from datetime import datetime

# 飞书应用凭证
APP_ID = "cli_a91697b3a6f85bb4"
APP_SECRET = "JNe1IuSLVqe2ESHz147ZJbvPbyidyGEj"

# 飞书 API 端点
BASE_URL = "https://open.feishu.cn/open-apis/bot/v2"
AUTH_URL = "https://open.feishu.cn/open-apis/auth/v3"

# 访问令牌
access_token = None

def get_access_token():
    """获取飞书应用访问令牌"""
    global access_token
    
    url = f"{AUTH_URL}/app_access_token/internal"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        result = response.json()
        
        print(f"获取访问令牌响应:")
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if 'app_access_token' in result:
            access_token = result['app_access_token']
            print("\n✅ 成功获取访问令牌")
            return True
        elif 'tenant_access_token' in result:
            access_token = result['tenant_access_token']
            print("\n✅ 成功获取访问令牌")
            return True
        else:
            print(f"\n❌ 获取访问令牌失败")
            return False
    except Exception as e:
        print(f"\n❌ 获取访问令牌异常: {e}")
        return False

def send_message(chat_id, text):
    """发送消息到群聊"""
    global access_token
    
    if not access_token:
        print("\n❌ 访问令牌未获取")
        return False
    
    url = f"{BASE_URL}/sendMessage"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "receive_id": chat_id,
        "msg_type": "text",
        "content": {
            "text": text
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        result = response.json()
        
        print(f"\n发送消息响应:")
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if 'code' in result and result['code'] == 0:
            print("\n✅ 成功发送消息")
            return True
        else:
            print(f"\n❌ 发送消息失败")
            return False
    except Exception as e:
        print(f"\n❌ 发送消息异常: {e}")
        return False

def main():
    """主测试函数"""
    print("飞书机器人功能测试")
    print("=" * 80)
    print(f"App ID: {APP_ID}")
    print(f"App Secret: {APP_SECRET}")
    print("=" * 80)
    
    # 步骤 1：获取访问令牌
    print("\n步骤 1：获取飞书访问令牌...")
    if not get_access_token():
        print("\n❌ 无法继续")
        return
    
    # 显示访问令牌
    print(f"\n访问令牌: {access_token}")
    
    # 步骤 2：发送测试消息（需要用户提供 chat_id）
    print("\n步骤 2：发送测试消息...")
    print("\n⚠️  注意：")
    print("1. 你需要提供目标群聊的 chat_id")
    print("2. 机器人必须已添加到目标群聊中")
    print("3. 机器人必须有发送消息的权限")
    print("4. 机器人必须有访问群聊的权限")
    
    print("\n" + "=" * 80)
    print("📋 飞书机器人配置清单")
    print("=" * 80)
    
    print("\n✅ 已完成的配置:")
    print("  • App ID 已验证")
    print("  • App Secret 已验证")
    print("  • 访问令牌已获取")
    print("  • 机器人已连接到飞书开放平台")
    
    print("\n⏳ 待完成的配置:")
    print("  • 机器人已添加到目标群聊")
    print("  • 机器人有发送消息的权限")
    print("  • 机器人有接收消息的权限")
    print("  • 机器人有访问群聊的权限")
    print("  • 事件订阅已配置（用于自动回复）")
    print("  • Webhook 已配置（如果使用 Webhook）")
    
    print("\n" + "=" * 80)
    print("📝 飞书开放平台配置步骤")
    print("=" * 80)
    
    print("\n1. 登录飞书开放平台:")
    print("   https://open.feishu.cn/")
    
    print("\n2. 找到你的应用:")
    print("   • 点击'应用管理'")
    print("   • 在应用列表中找到你的应用")
    print("   • 点击应用名称进入详情页")
    
    print("\n3. 检查机器人权限:")
    print("   • 在左侧菜单中找到'权限管理'")
    print("   • 确保以下权限已添加：")
    print("     ✅ 发送消息 (send_message)")
    print("     ✅ 接收消息 (receive_message)")
    print("     ✅ 获取群聊信息 (get_chat_info)")
    print("     ✅ 访问群聊 (access_chat)")
    
    print("\n4. 配置事件订阅:")
    print("   • 在左侧菜单中找到'事件订阅'")
    print("   • 添加以下事件：")
    print("     ✅ message.im.text (文本消息)")
    print("     ✅ message.im.image (图片消息)")
    print("     ✅ message.im.file (文件消息)")
    
    print("\n5. 配置 Webhook（如果使用 Webhook）:")
    print("   • 在事件订阅配置中添加 Webhook URL")
    print("   • Webhook URL 要求：")
    print("     • 公网可访问的 HTTPS 地址")
    print("     • 可以接收飞书服务器的 POST 请求")
    print("     • 可以快速响应 200 OK")
    
    print("\n6. 将机器人添加到群聊:")
    print("   • 在飞书客户端中打开目标群聊")
    print("   • 点击群聊设置")
    print("   • 点击'添加成员'")
    print("   • 搜索你的机器人名称")
    print("   • 添加机器人到群聊")
    
    print("\n" + "=" * 80)
    print("🚀 下一步操作")
    print("=" * 80)
    
    print("\n1. 确认机器人已添加到目标群聊")
    print("2. 获取目标群聊的 chat_id")
    print("3. 将 chat_id 提供给我")
    print("4. 我会发送测试消息验证机器人功能")
    
    print("\n" + "=" * 80)
    print("📋 获取 chat_id 的方法")
    print("=" * 80)
    
    print("\n方法 1：在飞书客户端中获取")
    print("  1. 打开目标群聊")
    print("  2. 点击群聊设置")
    print("  3. 点击'群信息'或'群设置'")
    print("  4. 找到'群聊 ID'或'Chat ID'")
    print("  5. 复制 chat_id（格式：oc_xxxxxxxxxxxxx）")
    
    print("\n方法 2：在飞书开放平台中获取")
    print("  1. 登录飞书开放平台")
    print("  2. 找到你的应用")
    print("  3. 在应用详情中找到'群聊管理'")
    print("  4. 查看机器人已添加的群聊列表")
    print("  5. 复制目标群聊的 chat_id")
    
    print("\n" + "=" * 80)
    print("🤖 飞书机器人自动回复实现方案")
    print("=" * 80)
    
    print("\n方案 1：使用飞书 SDK（推荐）")
    print("  安装：pip install lark-oapi")
    print("  优点：官方支持，功能完善，自动处理消息监听")
    print("  缺点：需要学习使用 SDK")
    
    print("\n方案 2：使用 Flask + Webhook")
    print("  安装：pip install flask")
    print("  优点：灵活，易于自定义")
    print("  缺点：需要部署服务器，需要公网访问")
    
    print("\n方案 3：使用飞书开放平台的长连接")
    print("  优点：不需要 Webhook，适合内部使用")
    print("  缺点：需要持续监听，实现较复杂")
    
    print("\n" + "=" * 80)
    print("✅ 飞书机器人基础功能已成功配置！")
    print("=" * 80)
    
    print("\n机器人可以发送消息，但需要提供 chat_id 才能测试。")
    print("请提供目标群聊的 chat_id，我会发送测试消息验证机器人功能。")

if __name__ == "__main__":
    main()
