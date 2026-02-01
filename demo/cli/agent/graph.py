"""
LangGraph Agent 实现

一个简单但功能完整的 Agent，支持：
- 多轮对话
- 工具调用
- 上下文管理
"""

import sys
from pathlib import Path
from typing import Literal

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver

from langgraph.graph import StateGraph, START, END

# 处理相对导入
try:
    from .state import AgentState
except (ImportError, ValueError):
    # 当作为模块直接导入时，使用绝对导入
    sys.path.insert(0, str(Path(__file__).parent))
    from state import AgentState


# ============================================================================
# 1. 辅助函数
# ============================================================================

def _get_message_content(message):
    """获取消息内容，兼容 dict 和 BaseMessage 格式

    LangGraph API 可能返回字典格式的消息，需要处理多种格式
    """
    # 处理字典格式
    if isinstance(message, dict):
        content = message.get("content", "")
        # 如果 content 是列表，取第一个元素
        if isinstance(content, list) and content:
            return str(content[0])
        return str(content)

    # 处理 BaseMessage 对象
    if hasattr(message, "content"):
        content = message.content
        # 如果 content 是列表，取第一个元素
        if isinstance(content, list) and content:
            return str(content[0])
        return str(content)

    # 其他情况
    return str(message)


# ============================================================================
# 2. 定义工具
# ============================================================================

@tool
def get_current_time() -> str:
    """获取当前时间"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def search_knowledge_base(query: str) -> str:
    """搜索知识库

    Args:
        query: 搜索查询

    Returns:
        搜索结果
    """
    # 模拟知识库搜索
    knowledge_base = {
        "langgraph": "LangGraph 是一个用于构建有状态多 actor 应用的框架",
        "agent": "Agent 是一个能够感知环境并采取行动的智能体",
        "python": "Python 是一种高级编程语言",
        "天气": "今天天气晴朗，温度 25°C",
    }

    query_lower = query.lower()
    for key, value in knowledge_base.items():
        if key in query_lower:
            return value

    return f"未找到关于 '{query}' 的信息"


@tool
def calculate(expression: str) -> str:
    """计算表达式

    Args:
        expression: 数学表达式

    Returns:
        计算结果
    """
    try:
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"计算错误: {str(e)}"


# ============================================================================
# 2. Node 函数
# ============================================================================

def process_input(state: AgentState) -> AgentState:
    """处理用户输入"""
    return state


def think_and_plan(state: AgentState) -> AgentState:
    """思考和规划

    Agent 分析输入并决定下一步操作
    """
    if not state["messages"]:
        state["next_action"] = "respond"
        return state

    last_message = state["messages"][-1]
    user_input = _get_message_content(last_message)
    # 确保 user_input 是字符串，然后转换为小写
    user_input = str(user_input).lower()

    # 决策逻辑
    if any(word in user_input for word in ["时间", "现在", "几点"]):
        state["next_action"] = "use_tool_time"
    elif any(word in user_input for word in ["查询", "搜索", "关于", "什么"]):
        state["next_action"] = "use_tool_search"
    elif any(word in user_input for word in ["计算", "算", "等于"]):
        state["next_action"] = "use_tool_calculate"
    else:
        state["next_action"] = "respond"

    return state


def use_tool_time(state: AgentState) -> AgentState:
    """使用时间工具"""
    from datetime import datetime
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    response = f"当前时间是: {current_time}"
    state["messages"].append(AIMessage(content=response))
    state["context"] = f"已获取时间: {current_time}"
    return state


def use_tool_search(state: AgentState) -> AgentState:
    """使用搜索工具"""
    if not state["messages"]:
        return state

    last_message = state["messages"][-1]
    user_input = _get_message_content(last_message)
    # 确保是字符串
    user_input = str(user_input)

    # 模拟知识库搜索
    knowledge_base = {
        "langgraph": "LangGraph 是一个用于构建有状态多 actor 应用的框架",
        "agent": "Agent 是一个能够感知环境并采取行动的智能体",
        "python": "Python 是一种高级编程语言",
        "天气": "今天天气晴朗，温度 25°C",
    }

    query_lower = user_input.lower()
    result = None
    for key, value in knowledge_base.items():
        if key in query_lower:
            result = value
            break

    if not result:
        result = f"未找到关于 '{user_input}' 的信息"

    state["messages"].append(AIMessage(content=result))
    state["context"] = f"搜索结果: {result}"
    return state


def use_tool_calculate(state: AgentState) -> AgentState:
    """使用计算工具"""
    if not state["messages"]:
        return state

    last_message = state["messages"][-1]
    user_input = _get_message_content(last_message)
    # 确保是字符串
    user_input = str(user_input)

    # 提取表达式
    import re
    match = re.search(r'[\d\+\-\*\/\(\)\.]+', user_input)
    if match:
        expression = match.group()
        try:
            calc_result = eval(expression)
            result = f"{expression} = {calc_result}"
        except Exception as e:
            result = f"计算错误: {str(e)}"
    else:
        result = "未找到有效的数学表达式"

    state["messages"].append(AIMessage(content=result))
    state["context"] = f"计算结果: {result}"
    return state


def respond(state: AgentState) -> AgentState:
    """直接回复

    Agent 直接回复用户
    """
    if not state["messages"]:
        response = "你好！我是一个 LangGraph Agent。我可以帮你：\n" \
                  "1. 查询当前时间\n" \
                  "2. 搜索知识库\n" \
                  "3. 进行数学计算\n\n" \
                  "请告诉我你需要什么帮助！"
    else:
        last_message = state["messages"][-1]
        user_input = _get_message_content(last_message)
        response = f"我收到你的消息: '{user_input}'\n\n" \
                  "我是一个 LangGraph Agent，可以帮助你处理各种任务。" \
                  "请告诉我你需要什么帮助！"

    state["messages"].append(AIMessage(content=response))
    state["context"] = response
    return state


# ============================================================================
# 3. 条件分支函数
# ============================================================================

def route_action(state: AgentState) -> Literal[
    "use_tool_time",
    "use_tool_search",
    "use_tool_calculate",
    "respond"
]:
    """根据下一步操作路由"""
    return state["next_action"]


# ============================================================================
# 4. 创建图
# ============================================================================

def create_agent_graph(with_checkpointer=True):
    """创建 Agent 图

    Args:
        with_checkpointer: 是否添加 checkpointer（本地运行时使用）
    """

    # 创建图
    graph = StateGraph(AgentState)

    # 添加节点
    graph.add_node("process_input", process_input)
    graph.add_node("think_and_plan", think_and_plan)
    graph.add_node("use_tool_time", use_tool_time)
    graph.add_node("use_tool_search", use_tool_search)
    graph.add_node("use_tool_calculate", use_tool_calculate)
    graph.add_node("respond", respond)

    # 添加边
    graph.add_edge(START, "process_input")
    graph.add_edge("process_input", "think_and_plan")

    # 条件分支
    graph.add_conditional_edges(
        "think_and_plan",
        route_action,
        {
            "use_tool_time": "use_tool_time",
            "use_tool_search": "use_tool_search",
            "use_tool_calculate": "use_tool_calculate",
            "respond": "respond",
        }
    )

    # 所有工具路径都回到响应
    graph.add_edge("use_tool_time", "respond")
    graph.add_edge("use_tool_search", "respond")
    graph.add_edge("use_tool_calculate", "respond")

    # 响应结束
    graph.add_edge("respond", END)

    # 编译（带 checkpointer 用于本地运行）
    if with_checkpointer:
        checkpointer = MemorySaver()
        compiled_graph = graph.compile(checkpointer=checkpointer)
    else:
        # LangGraph API/CLI 会自动处理 checkpointer
        compiled_graph = graph.compile()

    return compiled_graph


# ============================================================================
# 5. 导出图
# ============================================================================

# 为 LangGraph CLI 创建不带 checkpointer 的图
graph = create_agent_graph(with_checkpointer=False)

# 为本地运行保存带 checkpointer 的版本
_graph_with_checkpointer = create_agent_graph(with_checkpointer=True)


# ============================================================================
# 6. 本地运行函数
# ============================================================================

def run_agent_locally():
    """本地运行 Agent（开发模式）"""

    print("\n" + "=" * 70)
    print("🤖 LangGraph Agent - 本地开发模式")
    print("=" * 70)

    print("\n💡 功能演示:")
    print("   • 输入 '现在几点' 获取当前时间")
    print("   • 输入 '什么是langgraph' 搜索知识库")
    print("   • 输入 '计算 2+3*4' 进行数学计算")
    print("   • 输入 'quit' 退出\n")

    thread_id = "user_session_1"

    while True:
        user_input = input("👤 你: ").strip()

        if user_input.lower() == "quit":
            print("\n👋 再见!")
            break

        if not user_input:
            continue

        # 调用 Agent（使用带 checkpointer 的版本）
        config = {"configurable": {"thread_id": thread_id}}

        initial_state = {
            "messages": [HumanMessage(content=user_input)],
            "context": user_input,
            "next_action": ""
        }

        result = _graph_with_checkpointer.invoke(initial_state, config)

        # 显示 Agent 的回复
        if result["messages"]:
            last_message = result["messages"][-1]
            content = _get_message_content(last_message)
            print(f"\n🤖 Agent: {content}\n")


if __name__ == "__main__":
    run_agent_locally()

