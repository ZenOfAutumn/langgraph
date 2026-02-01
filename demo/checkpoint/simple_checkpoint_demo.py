"""
简化版 LangGraph Checkpoint 演示

展示核心概念：
- 使用 checkpoint 保存图的执行状态
- 通过 thread_id 隔离不同的流程
"""

import os
import sqlite3
from typing import TypedDict

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, START, END


class OrderState(TypedDict):
    """订单处理状态"""
    order_id: str
    status: str
    items: list
    total_price: float
    history: list  # 记录每个步骤


def step_validate_order(state: OrderState) -> OrderState:
    """验证订单"""
    print(f"  ✓ 验证订单 {state['order_id']}")
    state["status"] = "validated"
    state["history"].append(f"订单验证完成")
    return state


def step_process_payment(state: OrderState) -> OrderState:
    """处理支付"""
    print(f"  ✓ 处理支付 {state['order_id']}")
    state["status"] = "payment_processed"
    state["history"].append(f"支付已处理")
    return state


def step_pack_items(state: OrderState) -> OrderState:
    """打包物品"""
    print(f"  ✓ 打包物品 {state['order_id']}")
    state["status"] = "packed"
    state["history"].append(f"物品已打包")
    return state


def step_ship_order(state: OrderState) -> OrderState:
    """发货"""
    print(f"  ✓ 发货 {state['order_id']}")
    state["status"] = "shipped"
    state["history"].append(f"订单已发货")
    return state


def create_order_processing_graph():
    """创建订单处理工作流图"""

    # 初始化 checkpoint（SQLite 存储）
    # 创建数据库目录（如果不存在）
    db_path = "/tmp/langgraph_demo/order_checkpoints.db"
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # 使用 sqlite3.connect 直接创建连接
    conn = sqlite3.connect(db_path, check_same_thread=False)
    checkpointer = SqliteSaver(conn)
    checkpointer.setup()

    # 创建状态图
    graph = StateGraph(OrderState)

    # 添加处理节点
    graph.add_node("validate", step_validate_order)
    graph.add_node("payment", step_process_payment)
    graph.add_node("pack", step_pack_items)
    graph.add_node("ship", step_ship_order)

    # 定义流程
    graph.add_edge(START, "validate")
    graph.add_edge("validate", "payment")
    graph.add_edge("payment", "pack")
    graph.add_edge("pack", "ship")
    graph.add_edge("ship", END)

    # 编译并启用 checkpoint
    compiled_graph = graph.compile(checkpointer=checkpointer)

    return compiled_graph, checkpointer


def demo_basic_workflow():
    """演示基本工作流"""
    print("\n" + "=" * 70)
    print("🛒 订单处理工作流 - 基本演示")
    print("=" * 70)

    graph, checkpointer = create_order_processing_graph()

    # 初始订单状态
    order_state = {
        "order_id": "ORDER-001",
        "status": "pending",
        "items": ["手机", "充电器", "保护壳"],
        "total_price": 3999.99,
        "history": []
    }

    # 配置：使用 thread_id 作为订单标识
    config = {"configurable": {"thread_id": "ORDER-001"}}

    print("\n📝 初始订单状态:")
    print(f"   订单ID: {order_state['order_id']}")
    print(f"   物品: {', '.join(order_state['items'])}")
    print(f"   价格: ¥{order_state['total_price']}")

    print("\n▶️  执行订单处理流程...")

    # 执行工作流
    final_state = graph.invoke(order_state, config)

    print("\n✅ 流程完成!")
    print(f"   最终状态: {final_state['status']}")
    print(f"   处理步骤:")
    for i, step in enumerate(final_state['history'], 1):
        print(f"      {i}. {step}")


def demo_resuming_from_checkpoint():
    """演示从 checkpoint 恢复"""
    print("\n" + "=" * 70)
    print("🔄 从 Checkpoint 恢复 - 演示")
    print("=" * 70)

    graph, checkpointer = create_order_processing_graph()

    # 创建一个新订单（使用不同的 thread_id）
    order_state = {
        "order_id": "ORDER-002",
        "status": "pending",
        "items": ["笔记本电脑"],
        "total_price": 6999.99,
        "history": []
    }

    config = {"configurable": {"thread_id": "ORDER-002"}}

    print("\n📝 初始订单:")
    print(f"   订单ID: {order_state['order_id']}")
    print(f"   物品: {', '.join(order_state['items'])}")

    print("\n▶️  第一次执行...")

    # 第一次执行
    result1 = graph.invoke(order_state, config)

    print(f"\n✓ 第一次执行完成")
    print(f"   状态: {result1['status']}")
    print(f"   Checkpoint 已自动保存此状态")

    print("\n📌 模拟场景: 使用相同的 thread_id 再次执行")
    print("   (在生产中，这可能是系统重启后恢复)")

    print("\n▶️  第二次执行...")

    # 使用相同的 thread_id 再次执行
    # LangGraph 会检查 checkpoint，决定是否恢复
    result2 = graph.invoke(order_state, config)

    print(f"\n✓ 恢复执行完成")
    print(f"   状态: {result2['status']}")
    print(f"   \n💡 关键点: LangGraph 使用 checkpoint 避免重复处理")


def demo_parallel_orders():
    """演示处理多个订单"""
    print("\n" + "=" * 70)
    print("⚡ 并行处理多个订单 - 演示")
    print("=" * 70)

    graph, checkpointer = create_order_processing_graph()

    orders = [
        {
            "order_id": "ORDER-101",
            "status": "pending",
            "items": ["T恤", "牛仔裤"],
            "total_price": 199.99,
            "history": []
        },
        {
            "order_id": "ORDER-102",
            "status": "pending",
            "items": ["书籍"],
            "total_price": 49.99,
            "history": []
        },
        {
            "order_id": "ORDER-103",
            "status": "pending",
            "items": ["显示器", "键盘", "鼠标"],
            "total_price": 1999.99,
            "history": []
        }
    ]

    print(f"\n📦 处理 {len(orders)} 个订单...\n")

    results = []

    for order in orders:
        # 每个订单使用不同的 thread_id
        config = {"configurable": {"thread_id": order["order_id"]}}

        print(f"处理订单 {order['order_id']}:")

        result = graph.invoke(order, config)
        results.append(result)

    print("\n✅ 所有订单处理完成!")
    print("\n📊 订单处理摘要:")
    print(f"{'订单ID':<15} {'状态':<20} {'金额':<15}")
    print("-" * 50)

    for result in results:
        print(f"{result['order_id']:<15} {result['status']:<20} ¥{result['total_price']:<15.2f}")

    print("\n💡 关键点:")
    print("  • 每个订单有独立的 thread_id")
    print("  • 每个订单的 checkpoint 互不影响")
    print("  • 支持真正的并行/并发处理")


def print_checkpoint_info():
    """显示 checkpoint 信息"""
    print("\n" + "=" * 70)
    print("💾 Checkpoint 概念说明")
    print("=" * 70)

    info = {
        "什么是 Checkpoint":
            "图执行过程中的状态快照。保存每个节点执行后的完整状态。",

        "为什么需要 Checkpoint":
            "1. 故障恢复 - 系统崩溃后可从断点继续\n"
            "            2. 状态持久化 - 支持长时间运行的流程\n"
            "            3. 可观测性 - 随时查看流程进度\n"
            "            4. 并发支持 - 多个流程独立执行",

        "Checkpoint 的工作机制":
            "1. 节点执行完成 → 2. 状态变化 → 3. 自动保存到数据库\n"
            "            ↓\n"
            "            5. 故障恢复时 ← 4. 通过 thread_id 查询保存的状态",

        "thread_id 的作用":
            "唯一标识一个流程实例。相同的 thread_id 会共享 checkpoint。\n"
            "            不同的 thread_id 是完全独立的流程。",

        "生产环境推荐":
            "使用 PostgreSQL 而不是 SQLite\n"
            "            • SQLite 适合开发和测试\n"
            "            • PostgreSQL 提供更好的并发支持和可靠性",
    }

    for title, desc in info.items():
        print(f"\n📌 {title}:")
        print(f"   {desc}")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("🚀 LangGraph Checkpoint 完整演示")
    print("=" * 70)

    # 基本演示
    demo_basic_workflow()

    # 恢复演示
    demo_resuming_from_checkpoint()

    # 并行处理演示
    demo_parallel_orders()

    # 概念说明
    print_checkpoint_info()

    print("\n" + "=" * 70)
    print("✨ 演示完成!")
    print("=" * 70)
    print("\n📚 更多信息请查看: checkpoint_usage_guide.md")

