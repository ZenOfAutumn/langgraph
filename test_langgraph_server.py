#!/usr/bin/env python3
"""
测试 LangGraph 服务器的示例脚本

此脚本演示如何使用 Python SDK 连接到已运行的 LangGraph 服务器
需要先运行: langgraph dev
"""

import asyncio

from langgraph_sdk import get_client, get_sync_client


async def test_async():
    """使用异步 Python SDK 测试"""
    print("=" * 60)
    print("🔗 异步测试：连接到 LangGraph 服务器")
    print("=" * 60)

    try:
        # 创建客户端
        client = get_client(url="http://localhost:8123")

        print("✓ 成功连接到服务器")
        print()

        # 发送消息给助手（无线程运行）
        print("📝 发送消息: '什么是 LangGraph？'")
        print()

        chunk_count = 0
        async for chunk in client.runs.stream(
            None,  # 无线程运行
            "agent",  # 助手名称，定义在 langgraph.json 中
            input={
                "messages": [{
                    "role": "human",
                    "content": "什么是 LangGraph？",
                }],
            },
            stream_mode="updates",
        ):
            chunk_count += 1
            print(f"接收事件 #{chunk_count}: {chunk.event}")
            if hasattr(chunk, 'data') and chunk.data:
                # 只显示前 200 个字符
                data_str = str(chunk.data)[:200]
                print(f"  数据: {data_str}...")
            print()

        print(f"✓ 成功接收 {chunk_count} 个事件")

    except Exception as e:
        print(f"❌ 错误: {e}")
        print()
        print("💡 确保 LangGraph 服务器正在运行:")
        print("   cd my_langgraph_app && langgraph dev")


def test_sync():
    """使用同步 Python SDK 测试"""
    print("=" * 60)
    print("🔗 同步测试：连接到 LangGraph 服务器")
    print("=" * 60)

    try:
        # 创建客户端
        client = get_sync_client(url="http://localhost:8123")

        print("✓ 成功连接到服务器")
        print()

        # 发送消息给助手（无线程运行）
        print("📝 发送消息: '什么是 LangGraph？'")
        print()

        chunk_count = 0
        for chunk in client.runs.stream(
            None,  # 无线程运行
            "agent",  # 助手名称，定义在 langgraph.json 中
            input={
                "messages": [{
                    "role": "human",
                    "content": "什么是 LangGraph？",
                }],
            },
            stream_mode="updates",
        ):
            chunk_count += 1
            print(f"接收事件 #{chunk_count}: {chunk.event}")
            if hasattr(chunk, 'data') and chunk.data:
                # 只显示前 200 个字符
                data_str = str(chunk.data)[:200]
                print(f"  数据: {data_str}...")
            print()

        print(f"✓ 成功接收 {chunk_count} 个事件")

    except Exception as e:
        print(f"❌ 错误: {e}")
        print()
        print("💡 确保 LangGraph 服务器正在运行:")
        print("   cd my_langgraph_app && langgraph dev")


def test_curl():
    """显示如何使用 REST API 测试"""
    print("=" * 60)
    print("🌐 REST API 测试示例 (使用 curl)")
    print("=" * 60)
    print()
    print("运行以下命令来测试 REST API:")
    print()
    print('curl -s --request POST \\')
    print('  --url "http://localhost:8123/runs/stream" \\')
    print("  --header 'Content-Type: application/json' \\")
    print('  --data "{')
    print('    \\"assistant_id\\": \\"agent\\",')
    print('    \\"input\\": {')
    print('      \\"messages\\": [')
    print('        {')
    print('          \\"role\\": \\"human\\",')
    print('          \\"content\\": \\"什么是 LangGraph?\\"')
    print('        }')
    print('      ]')
    print('    },')
    print('    \\"stream_mode\\": \\"updates\\"')
    print('  }"')
    print()


def main():
    """主函数"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "   ✅ 测试 LangGraph 服务器".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    print()

    print("📌 前置条件:")
    print("   1. 确保 LangGraph 服务器正在运行")
    print("   2. 运行: cd my_langgraph_app && langgraph dev")
    print()

    # 测试同步客户端
    test_sync()
    print()

    # 测试异步客户端
    print("按 Enter 继续异步测试...")
    input()
    asyncio.run(test_async())
    print()

    # 显示 REST API 示例
    test_curl()

    print("=" * 60)
    print("✅ 测试完成")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()

