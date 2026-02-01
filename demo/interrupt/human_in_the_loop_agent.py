"""
Human-in-the-Loop Agent 示例

演示如何在 LangGraph 中实现人工干预（Human-in-the-Loop）机制。
Agent 在关键决策点暂停，等待用户输入后继续执行。

场景：订单处理 Agent
- 用户提交订单信息
- Agent 分析订单
- 当金额超过阈值时，Agent 暂停并等待人工审批
- 获得人工批准后继续处理
"""

from enum import Enum
from typing import TypedDict

from langgraph.checkpoint.memory import MemorySaver

from langgraph.graph import StateGraph, START, END


class OrderStatus(str, Enum):
    """订单状态"""
    PENDING = "pending"
    ANALYZING = "analyzing"
    WAITING_APPROVAL = "waiting_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    PROCESSING = "processing"
    COMPLETED = "completed"


class OrderState(TypedDict):
    """订单处理状态"""
    order_id: str
    customer_name: str
    items: list
    total_amount: float
    status: OrderStatus
    history: list
    human_feedback: str  # 人工反馈信息


# ============================================================================
# 1. 分析订单节点
# ============================================================================

def analyze_order(state: OrderState) -> OrderState:
    """分析订单信息"""
    print(f"\n📊 分析订单: {state['order_id']}")
    print(f"   客户: {state['customer_name']}")
    print(f"   物品: {', '.join(state['items'])}")
    print(f"   金额: ¥{state['total_amount']:.2f}")

    state["status"] = OrderStatus.ANALYZING
    state["history"].append(f"订单分析完成，金额: ¥{state['total_amount']:.2f}")

    return state


# ============================================================================
# 2. 检查是否需要人工审批（关键决策点）
# ============================================================================

def check_approval_needed(state: OrderState) -> str:
    """检查是否需要人工审批（金额 > 500 需要审批）"""
    print(f"\n🔍 检查审批需求...")

    approval_threshold = 500  # 审批阈值

    if state["total_amount"] > approval_threshold:
        print(f"⚠️  金额 ¥{state['total_amount']:.2f} 超过审批阈值 ¥{approval_threshold}")
        state["status"] = OrderStatus.WAITING_APPROVAL
        state["history"].append("订单金额超过审批阈值，等待人工审批")
        return "wait_approval"
    else:
        print(f"✓ 金额 ¥{state['total_amount']:.2f} 在审批阈值以内")
        return "auto_approve"


# ============================================================================
# 3. 等待人工审批节点（暂停点）
# ============================================================================

def wait_human_approval(state: OrderState) -> OrderState:
    """等待人工审批（节点暂停）"""
    print(f"\n⏸️  [暂停] 等待人工审批...")
    print(f"   订单ID: {state['order_id']}")
    print(f"   金额: ¥{state['total_amount']:.2f}")
    print(f"   请输入审批结果 (approve/reject): ", end="", flush=True)

    # 从标准输入读取用户决定
    user_input = input().strip().lower()

    if user_input in ["approve", "a", "yes", "y"]:
        state["human_feedback"] = "人工批准订单"
        state["status"] = OrderStatus.APPROVED
        state["history"].append("人工审批: 批准")
        print(f"✅ 订单已批准")
    else:
        state["human_feedback"] = "人工拒绝订单"
        state["status"] = OrderStatus.REJECTED
        state["history"].append("人工审批: 拒绝")
        print(f"❌ 订单已拒绝")

    return state


# ============================================================================
# 4. 自动审批节点
# ============================================================================

def auto_approve(state: OrderState) -> OrderState:
    """自动批准小额订单"""
    print(f"\n✅ 自动批准订单")
    state["status"] = OrderStatus.APPROVED
    state["human_feedback"] = "自动批准（金额在阈值以内）"
    state["history"].append("自动审批: 批准")
    return state


# ============================================================================
# 5. 处理订单节点
# ============================================================================

def process_order(state: OrderState) -> OrderState:
    """处理批准的订单"""
    if state["status"] == OrderStatus.REJECTED:
        print(f"\n⛔ 订单被拒绝，跳过处理")
        state["history"].append("订单被拒绝，处理中止")
        return state

    print(f"\n⚙️  处理订单: {state['order_id']}")
    state["status"] = OrderStatus.PROCESSING
    state["history"].append("订单处理中...")
    return state


# ============================================================================
# 6. 完成订单节点
# ============================================================================

def complete_order(state: OrderState) -> OrderState:
    """完成订单"""
    if state["status"] in [OrderStatus.REJECTED, OrderStatus.PENDING]:
        print(f"\n✗ 订单处理失败")
        return state

    print(f"\n🎉 订单完成!")
    print(f"   订单ID: {state['order_id']}")
    print(f"   最终状态: {state['status'].value}")
    state["status"] = OrderStatus.COMPLETED
    state["history"].append("订单完成")

    return state


# ============================================================================
# 创建图
# ============================================================================

def create_human_in_the_loop_graph():
    """创建具有人工干预的订单处理图"""

    # 初始化 checkpoint（使用内存存储）
    checkpointer = MemorySaver()

    # 创建状态图
    graph = StateGraph(OrderState)

    # 添加节点
    graph.add_node("analyze", analyze_order)
    graph.add_node("check_approval", lambda state: state)  # 虚拟节点用于条件判断
    graph.add_node("wait_approval", wait_human_approval)
    graph.add_node("auto_approve", auto_approve)
    graph.add_node("process", process_order)
    graph.add_node("complete", complete_order)

    # 添加边
    graph.add_edge(START, "analyze")
    graph.add_edge("analyze", "check_approval")

    # 条件分支
    graph.add_conditional_edges(
        "check_approval",
        check_approval_needed,
        {
            "wait_approval": "wait_approval",
            "auto_approve": "auto_approve",
        },
    )

    # 两条路径都汇聚到处理
    graph.add_edge("wait_approval", "process")
    graph.add_edge("auto_approve", "process")

    # 完成
    graph.add_edge("process", "complete")
    graph.add_edge("complete", END)

    # 编译图
    compiled_graph = graph.compile(checkpointer=checkpointer)

    return compiled_graph, checkpointer


# ============================================================================
# 演示函数
# ============================================================================

def demo_simple_order():
    """演示 1: 小额订单（无需人工审批）"""
    print("\n" + "=" * 70)
    print("演示 1: 小额订单（自动批准）")
    print("=" * 70)

    graph, checkpointer = create_human_in_the_loop_graph()

    order_state = {
        "order_id": "ORD-001",
        "customer_name": "张三",
        "items": ["笔记本", "鼠标"],
        "total_amount": 299.99,
        "status": OrderStatus.PENDING,
        "history": [],
        "human_feedback": "",
    }

    config = {"configurable": {"thread_id": "ORD-001"}}

    final_state = graph.invoke(order_state, config)

    print(f"\n📋 最终状态:")
    print(f"   订单ID: {final_state['order_id']}")
    print(f"   状态: {final_state['status'].value}")
    print(f"   处理步骤: {len(final_state['history'])}")
    for i, step in enumerate(final_state['history'], 1):
        print(f"      {i}. {step}")


def demo_large_order():
    """演示 2: 大额订单（需要人工审批）"""
    print("\n" + "=" * 70)
    print("演示 2: 大额订单（需要人工审批）")
    print("=" * 70)

    graph, checkpointer = create_human_in_the_loop_graph()

    order_state = {
        "order_id": "ORD-002",
        "customer_name": "李四",
        "items": ["高端笔记本电脑", "显示器", "键盘"],
        "total_amount": 8999.99,
        "status": OrderStatus.PENDING,
        "history": [],
        "human_feedback": "",
    }

    config = {"configurable": {"thread_id": "ORD-002"}}

    print("\n💡 提示: 此订单金额超过审批阈值，需要人工批准")
    print("   请在提示时输入 'approve' 或 'reject'")

    final_state = graph.invoke(order_state, config)

    print(f"\n📋 最终状态:")
    print(f"   订单ID: {final_state['order_id']}")
    print(f"   状态: {final_state['status'].value}")
    print(f"   人工反馈: {final_state['human_feedback']}")
    print(f"   处理步骤: {len(final_state['history'])}")
    for i, step in enumerate(final_state['history'], 1):
        print(f"      {i}. {step}")


def demo_multiple_orders():
    """演示 3: 处理多个订单"""
    print("\n" + "=" * 70)
    print("演示 3: 处理多个订单")
    print("=" * 70)

    graph, checkpointer = create_human_in_the_loop_graph()

    orders = [
        {
            "order_id": "ORD-003",
            "customer_name": "王五",
            "items": ["打印机"],
            "total_amount": 1200.00,
            "status": OrderStatus.PENDING,
            "history": [],
            "human_feedback": "",
        },
        {
            "order_id": "ORD-004",
            "customer_name": "赵六",
            "items": ["书籍"],
            "total_amount": 99.99,
            "status": OrderStatus.PENDING,
            "history": [],
            "human_feedback": "",
        },
    ]

    print("\n💡 提示: 第一个订单需要人工批准（¥1200 > ¥500）")
    print("   第二个订单将自动批准（¥99.99 < ¥500）")

    for order in orders:
        print(f"\n📦 处理订单: {order['order_id']}")

        config = {"configurable": {"thread_id": order["order_id"]}}
        final_state = graph.invoke(order, config)

        print(f"   最终状态: {final_state['status'].value}")
        print(f"   反馈信息: {final_state['human_feedback']}")


# ============================================================================
# 主程序
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("🤖 LangGraph Human-in-the-Loop Agent 示例")
    print("=" * 70)

    # 演示 1: 小额订单
    demo_simple_order()

    # 演示 2: 大额订单（需要人工交互）
    demo_large_order()

    # 演示 3: 多个订单
    demo_multiple_orders()

    print("\n" + "=" * 70)
    print("✨ 演示完成!")
    print("=" * 70)
    print("\n💡 关键概念:")
    print("   1. 条件分支: 根据金额自动路由到不同的处理流程")
    print("   2. 暂停点: 等待人工审批时暂停执行")
    print("   3. Human-in-the-Loop: 在关键决策点融合人类判断")
    print("   4. Checkpoint: 支持恢复和重新执行")
    print("\n📚 更多信息请查看代码注释")

