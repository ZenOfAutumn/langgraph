"""运行 Human-in-the-Loop 演示的非交互版本"""

from human_in_the_loop_agent import (
    demo_simple_order,
    create_human_in_the_loop_graph,
    OrderStatus,
)

print("\n" + "=" * 70)
print("🤖 LangGraph Human-in-the-Loop Agent 演示")
print("=" * 70)

# 演示 1: 小额订单（自动批准）
print("\n【演示 1】小额订单 - 自动批准")
demo_simple_order()

# 演示 2: 大额订单（自动拒绝 - 模拟人工拒绝）
print("\n" + "=" * 70)
print("【演示 2】大额订单 - 模拟人工拒绝")
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

print(f"\n📊 分析订单: {order_state['order_id']}")
print(f"   客户: {order_state['customer_name']}")
print(f"   物品: {', '.join(order_state['items'])}")
print(f"   金额: ¥{order_state['total_amount']:.2f}")

print(f"\n🔍 检查审批需求...")
print(f"⚠️  金额 ¥{order_state['total_amount']:.2f} 超过审批阈值 ¥500")
print(f"⏸️  [暂停] 等待人工审批...")
print(f"   订单ID: {order_state['order_id']}")
print(f"   金额: ¥{order_state['total_amount']:.2f}")
print(f"\n💭 模拟人工决定: 拒绝 (输入: reject)")

# 模拟人工输入
import sys
from io import StringIO

# 保存原始 stdin
original_stdin = sys.stdin

# 创建模拟输入
sys.stdin = StringIO("reject\n")

try:
    final_state = graph.invoke(order_state, config)
finally:
    # 恢复原始 stdin
    sys.stdin = original_stdin

print(f"\n📋 最终状态:")
print(f"   订单ID: {final_state['order_id']}")
print(f"   状态: {final_state['status'].value}")
print(f"   人工反馈: {final_state['human_feedback']}")
print(f"   处理步骤:")
for i, step in enumerate(final_state['history'], 1):
    print(f"      {i}. {step}")

# 演示 3: 多个订单
print("\n" + "=" * 70)
print("【演示 3】多个订单处理")
print("=" * 70)

graph2, checkpointer2 = create_human_in_the_loop_graph()

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

results = []
for order in orders:
    print(f"\n📦 处理订单: {order['order_id']}")

    if order["total_amount"] > 500:
        print(f"   💰 金额 ¥{order['total_amount']:.2f} > ¥500，需要人工审批")
        print(f"   模拟人工决定: 批准 (输入: approve)")

        # 模拟人工输入为 approve
        sys.stdin = StringIO("approve\n")
    else:
        print(f"   💰 金额 ¥{order['total_amount']:.2f} < ¥500，自动批准")

    try:
        config = {"configurable": {"thread_id": order["order_id"]}}
        final_state = graph2.invoke(order, config)
        results.append(final_state)
    finally:
        sys.stdin = original_stdin

print("\n📊 订单处理汇总:")
print(f"{'订单ID':<10} {'客户':<10} {'金额':<10} {'最终状态':<15}")
print("-" * 45)
for result in results:
    print(f"{result['order_id']:<10} {result['customer_name']:<10} "
          f"¥{result['total_amount']:<8.2f} {result['status'].value:<15}")

print("\n" + "=" * 70)
print("✨ 演示完成!")
print("=" * 70)

print("\n📌 关键概念:")
print("   1️⃣  条件分支: 根据金额自动路由到不同的处理流程")
print("   2️⃣  暂停点: 等待人工审批时暂停执行")
print("   3️⃣  Human-in-the-Loop: 在关键决策点融合人类判断")
print("   4️⃣  Checkpoint: 支持恢复和重新执行")

print("\n💡 实际应用:")
print("   • 订单管理系统 - 大额订单需要人工批准")
print("   • 审批工作流 - 关键决策需要人工干预")
print("   • 内容审核 - 模糊内容需要人工判断")
print("   • 风险控制 - 异常交易需要人工审查")

