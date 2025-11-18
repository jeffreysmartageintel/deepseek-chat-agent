"""
简单的API测试脚本
用于测试本地运行的DeepSeek Chat Agent API
"""
import requests
import json

BASE_URL = "http://localhost:8080"

def test_health_check():
    """测试健康检查端点"""
    print("=" * 50)
    print("测试健康检查端点")
    print("=" * 50)
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        print()
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 错误: {e}")
        print("请确保服务正在运行 (uvicorn app.main:app --reload)")
        print()
        return False

def test_simple_chat():
    """测试简化聊天接口"""
    print("=" * 50)
    print("测试简化聊天接口")
    print("=" * 50)
    try:
        user_input = "你好，请介绍一下你自己"
        response = requests.post(
            f"{BASE_URL}/api/chat/simple",
            params={"user_input": user_input}
        )
        print(f"状态码: {response.status_code}")
        print(f"用户输入: {user_input}")
        print(f"AI回复: {response.json().get('ai_response', 'N/A')}")
        print(f"Token使用: {response.json().get('usage', {})}")
        print()
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 错误: {e}")
        print()
        return False

def test_full_chat():
    """测试完整聊天接口"""
    print("=" * 50)
    print("测试完整聊天接口")
    print("=" * 50)
    try:
        payload = {
            "messages": [
                {"role": "user", "content": "什么是人工智能？请用简单的话解释一下。"}
            ],
            "temperature": 0.7,
            "max_tokens": 5000
        }
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json=payload
        )
        print(f"状态码: {response.status_code}")
        print(f"请求: {json.dumps(payload, indent=2, ensure_ascii=False)}")
        print(f"AI回复: {response.json().get('message', 'N/A')}")
        print(f"Token使用: {response.json().get('usage', {})}")
        print()
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 错误: {e}")
        print()
        return False

def test_multi_turn_chat():
    """测试多轮对话"""
    print("=" * 50)
    print("测试多轮对话")
    print("=" * 50)
    try:
        payload = {
            "messages": [
                {"role": "system", "content": "你是一个专业的Python编程助手。"},
                {"role": "user", "content": "如何创建一个Python虚拟环境？"},
                {"role": "assistant", "content": "可以使用 python -m venv venv 命令创建虚拟环境。"},
                {"role": "user", "content": "那如何激活它呢？"}
            ],
            "temperature": 0.7,
            "max_tokens": 5000
        }
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json=payload
        )
        print(f"状态码: {response.status_code}")
        print(f"多轮对话上下文:")
        for msg in payload["messages"]:
            print(f"  {msg['role']}: {msg['content']}")
        print(f"\nAI回复: {response.json().get('message', 'N/A')}")
        print()
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 错误: {e}")
        print()
        return False

def main():
    """运行所有测试"""
    print("\n" + "=" * 50)
    print("DeepSeek Chat Agent API 测试")
    print("=" * 50 + "\n")
    
    results = []
    
    # 测试健康检查
    results.append(("健康检查", test_health_check()))
    
    # 如果健康检查失败，不继续测试
    if not results[0][1]:
        print("❌ 服务未运行，请先启动服务:")
        print("   uvicorn app.main:app --reload")
        return
    
    # 测试简化聊天接口
    results.append(("简化聊天接口", test_simple_chat()))
    
    # 测试完整聊天接口
    results.append(("完整聊天接口", test_full_chat()))
    
    # 测试多轮对话
    results.append(("多轮对话", test_multi_turn_chat()))
    
    # 打印测试结果摘要
    print("=" * 50)
    print("测试结果摘要")
    print("=" * 50)
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")
    print("=" * 50)

if __name__ == "__main__":
    main()

