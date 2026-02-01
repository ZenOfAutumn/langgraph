#!/usr/bin/env python
"""
测试 LangGraph API

用于测试通过 LangGraph API 调用 Agent
"""

import json
import uuid

import requests

BASE_URL = "http://127.0.0.1:9000"

def test_agent_invocation():
    """测试 Agent 调用"""

    print("=" * 70)
    print("🧪 测试 LangGraph Agent API")
    print("=" * 70)

    # 1. 创建线程
    print("\n1. 创建新的线程...")
    url_create_thread = f"{BASE_URL}/threads"

    try:
        response_thread = requests.post(url_create_thread, json={}, timeout=10)
        print(f"   状态码: {response_thread.status_code}")

        if response_thread.status_code < 300:
            thread_data = response_thread.json()
            thread_id = thread_data.get("thread_id") or str(uuid.uuid4())
            print(f"✅ 线程已创建")
            print(f"   线程 ID: {thread_id}")
        else:
            print(f"❌ 创建线程失败: {response_thread.status_code}")
            print(f"   响应: {response_thread.text}")
            return
    except Exception as e:
        print(f"❌ 错误: {e}")
        return

    # 2. 创建运行
    print("\n2. 创建新的运行...")
    url_create_run = f"{BASE_URL}/threads/{thread_id}/runs"

    payload = {
        "assistant_id": "agent",
        "input": {
            "messages": [{"type": "human", "content": "现在几点了？"}],
            "context": "",
            "next_action": ""
        }
    }

    print(f"   URL: {url_create_run}")
    print(f"   Payload: {json.dumps(payload, indent=2, ensure_ascii=False)}")

    try:
        response = requests.post(url_create_run, json=payload, timeout=10)
        print(f"   状态码: {response.status_code}")

        if response.status_code < 300:
            print("\n✅ 成功！运行已创建")
            try:
                data = response.json()
                print(f"   运行 ID: {data}")

                # 3. 获取运行结果
                print("\n3. 获取运行结果...")
                run_id = data.get("run_id") if isinstance(data, dict) else str(data).strip('"')
                url_get_run = f"{BASE_URL}/threads/{thread_id}/runs/{run_id}"

                # 等待一下让运行完成
                import time
                time.sleep(2)

                response_result = requests.get(url_get_run, timeout=10)
                if response_result.status_code < 300:
                    result_data = response_result.json()
                    print("✅ 运行结果:")
                    print(json.dumps(result_data, indent=2, ensure_ascii=False))
                else:
                    print(f"❌ 获取结果失败: {response_result.status_code}")

            except Exception as e:
                print(f"❌ 解析响应失败: {e}")
                print(f"   原始响应: {response.text}")
        else:
            print(f"\n❌ 错误: {response.status_code}")
            print(f"   响应: {response.text}")

    except requests.exceptions.ConnectionError as e:
        print(f"\n❌ 连接错误: {e}")
    except Exception as e:
        print(f"\n❌ 错误: {e}")


if __name__ == "__main__":
    test_agent_invocation()

