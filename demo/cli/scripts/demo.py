"""
LangGraph Agent 演示脚本

演示 Agent 的各种功能
"""

import sys
from pathlib import Path

# 添加项目路径（脚本在 scripts/ 目录，需要向上一级到项目根目录）
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from langchain_core.messages import HumanMessage

from agent.graph import graph, _get_message_content


def get_content(msg):
    """获取消息内容，兼容多种格式"""
    try:
        return _get_message_content(msg)
    except:
        if hasattr(msg, "content"):
            return msg.content
        elif isinstance(msg, dict):
            return msg.get("content", "")
        return str(msg)


def demo_get_time():
    """演示获取时间"""
    print("\n【演示 1】获取当前时间")
    print("-" * 70)
    print("👤 用户: 现在几点了？")

    state = {
        "messages": [HumanMessage(content="现在几点了？")],
        "context": "",
        "next_action": ""
    }

    config = {"configurable": {"thread_id": "demo_session"}}
    result = graph.invoke(state, config)

    for msg in result["messages"]:
        content = get_content(msg)
        if content.startswith("当前时间"):
            print(f"🤖 Agent: {content}")


def demo_search_knowledge():
    """演示搜索知识库"""
    print("\n【演示 2】搜索知识库")
    print("-" * 70)
    print("👤 用户: 什么是 LangGraph？")

    state = {
        "messages": [HumanMessage(content="什么是 LangGraph？")],
        "context": "",
        "next_action": ""
    }

    config = {"configurable": {"thread_id": "demo_session_2"}}
    result = graph.invoke(state, config)

    # 显示搜索结果
    if len(result["messages"]) > 1:
        for msg in result["messages"][1:]:
            content = get_content(msg)
            print(f"🤖 Agent: {content}")


def demo_calculate():
    """演示计算"""
    print("\n【演示 3】数学计算")
    print("-" * 70)
    print("👤 用户: 计算 10+5*2")

    state = {
        "messages": [HumanMessage(content="计算 10+5*2")],
        "context": "",
        "next_action": ""
    }

    config = {"configurable": {"thread_id": "demo_session_3"}}
    result = graph.invoke(state, config)

    # 显示计算结果
    if len(result["messages"]) > 1:
        for msg in result["messages"][1:]:
            content = get_content(msg)
            print(f"🤖 Agent: {content}")


def demo_general_query():
    """演示通用查询"""
    print("\n【演示 4】通用查询")
    print("-" * 70)
    print("👤 用户: 你好，你能做什么？")

    state = {
        "messages": [HumanMessage(content="你好，你能做什么？")],
        "context": "",
        "next_action": ""
    }

    config = {"configurable": {"thread_id": "demo_session_4"}}
    result = graph.invoke(state, config)

    # 显示响应
    if len(result["messages"]) > 1:
        for msg in result["messages"][1:]:
            content = get_content(msg)
            print(f"🤖 Agent: {content}")


def main():
    """运行演示"""
    print("\n" + "=" * 70)
    print("🤖 LangGraph Agent 本地演示")
    print("=" * 70)

    print("\n📌 这是一个完整的 LangGraph Agent 示例，展示了：")
    print("   1. 多轮对话处理")
    print("   2. 条件分支路由")
    print("   3. 工具调用（时间、搜索、计算）")
    print("   4. 状态管理")
    print("   5. Checkpoint 支持\n")

    # 运行演示
    demo_get_time()
    demo_search_knowledge()
    demo_calculate()
    demo_general_query()

    print("\n" + "=" * 70)
    print("✨ 演示完成!")
    print("=" * 70)

    print("\n🚀 下一步:")
    print("   1. 运行本地服务器: python run_local.py")
    print("   2. 使用 LangGraph CLI: langgraph dev")
    print("   3. 启动 Docker: langgraph up\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()

