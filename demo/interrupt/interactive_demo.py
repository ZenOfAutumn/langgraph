"""
交互式 Human-in-the-Loop Agent 演示

支持实时用户输入，体验完整的人工干预工作流。
"""

from human_in_the_loop_agent import (
    create_human_in_the_loop_graph,
    OrderStatus,
)


def print_header(text):
    """打印标题"""
    print(f"\n{'=' * 70}")
    print(f"  {text}")
    print(f"{'=' * 70}")


def get_user_decision():
    """获取用户审批决定"""
    while True:
        decision = input("\n👤 请输入审批决定 (approve/reject): ").strip().lower()
        if decision in ["approve", "a", "yes", "y", "reject", "r", "no", "n"]:
            return decision
        print("❌ 无效输入，请输入 'approve' 或 'reject'")


def interactive_order_processing():
    """交互式订单处理"""
    print_header("🤖 LangGraph Human-in-the-Loop Agent - 交互式演示")

    graph, checkpointer = create_human_in_the_loop_graph()

    print("\n📝 请输入订单信息:")

    # 获取订单基本信息
    order_id = input("   订单ID (默认: ORD-001): ").strip() or "ORD-001"
    customer_name = input("   客户名称 (默认: 张三): ").strip() or "张三"

    items_input = input("   物品列表，用逗号分隔 (默认: 笔记本,鼠标): ").strip()
    if items_input:
        items = [item.strip() for item in items_input.split(",")]
    else:
        items = ["笔记本", "鼠标"]

    while True:
        try:
            amount = float(input("   订单金额 (默认: 299.99): ").strip() or "299.99")
            break
        except ValueError:
            print("❌ 无效金额，请输入数字")

    # 创建订单状态
    order_state = {
        "order_id": order_id,
        "customer_name": customer_name,
        "items": items,
        "total_amount": amount,
        "status": OrderStatus.PENDING,
        "history": [],
        "human_feedback": "",
    }

    config = {"configurable": {"thread_id": order_id}}

    # 处理订单
    print_header("处理订单")
    print(f"\n📦 订单详情:")
    print(f"   订单ID: {order_state['order_id']}")
    print(f"   客户: {order_state['customer_name']}")
    print(f"   物品: {', '.join(order_state['items'])}")
    print(f"   金额: ¥{order_state['total_amount']:.2f}")

    print(f"\n⚠️  检查: 审批阈值为 ¥500")
    if order_state["total_amount"] > 500:
        print(f"   该订单需要人工审批 (¥{order_state['total_amount']:.2f} > ¥500)")
        print("\n💭 系统已准备好接收你的审批决定...")

        # 运行图（会在 wait_human_approval 节点暂停）
        final_state = graph.invoke(order_state, config)
    else:
        print(f"   该订单符合自动批准条件 (¥{order_state['total_amount']:.2f} ≤ ¥500)")
        final_state = graph.invoke(order_state, config)

    # 显示最终结果
    print_header("订单处理结果")
    print(f"\n✅ 处理完成!")
    print(f"\n📊 最终状态:")
    print(f"   订单ID: {final_state['order_id']}")
    print(f"   客户: {final_state['customer_name']}")
    print(f"   金额: ¥{final_state['total_amount']:.2f}")
    print(f"   最终状态: {final_state['status'].value.upper()}")
    print(f"   反馈: {final_state['human_feedback']}")

    print(f"\n📋 处理历史:")
    for i, step in enumerate(final_state["history"], 1):
        print(f"   {i}. {step}")

    # 显示统计信息
    print(f"\n📈 统计信息:")
    print(f"   总处理步骤: {len(final_state['history'])}")
    print(f"   订单最终状态: {final_state['status'].value}")


def batch_processing():
    """批量处理订单（演示多个订单的场景）"""
    print_header("📦 批量订单处理")

    graph, checkpointer = create_human_in_the_loop_graph()

    # 预定义的订单集
    orders = [
        {
            "order_id": "ORD-1001",
            "customer_name": "企业A",
            "items": ["服务器", "网络设备"],
            "total_amount": 15000.00,
        },
        {
            "order_id": "ORD-1002",
            "customer_name": "企业B",
            "items": ["办公用品"],
            "total_amount": 250.50,
        },
        {
            "order_id": "ORD-1003",
            "customer_name": "企业C",
            "items": ["软件许可证"],
            "total_amount": 2500.00,
        },
    ]

    print(f"\n📥 将处理 {len(orders)} 个订单...")
    results = []

    for idx, order_info in enumerate(orders, 1):
        print(f"\n[{idx}/{len(orders)}] 处理订单: {order_info['order_id']}")

        order_state = {
            "order_id": order_info["order_id"],
            "customer_name": order_info["customer_name"],
            "items": order_info["items"],
            "total_amount": order_info["total_amount"],
            "status": OrderStatus.PENDING,
            "history": [],
            "human_feedback": "",
        }

        config = {"configurable": {"thread_id": order_info["order_id"]}}

        print(f"   客户: {order_state['customer_name']}")
        print(f"   金额: ¥{order_state['total_amount']:.2f}")

        if order_state["total_amount"] > 500:
            print(f"   ⚠️  需要人工审批...")
            print(f"\n   👤 请审批此订单 (approve/reject): ", end="", flush=True)
            decision = get_user_decision()

            # 模拟用户输入
            import sys
            from io import StringIO

            original_stdin = sys.stdin
            sys.stdin = StringIO(f"{decision}\n")

            try:
                final_state = graph.invoke(order_state, config)
            finally:
                sys.stdin = original_stdin
        else:
            print(f"   ✅ 自动批准...")
            final_state = graph.invoke(order_state, config)

        print(f"   ✓ 最终状态: {final_state['status'].value}")
        results.append(final_state)

    # 显示汇总
    print_header("批量处理结果汇总")

    approved = [r for r in results if r["status"] == OrderStatus.COMPLETED]
    rejected = [r for r in results if r["status"] == OrderStatus.REJECTED]

    print(f"\n📊 统计结果:")
    print(f"   总订单数: {len(results)}")
    print(f"   批准订单: {len(approved)} 个")
    print(f"   拒绝订单: {len(rejected)} 个")

    print(f"\n📋 订单列表:")
    print(f"{'订单ID':<12} {'客户':<12} {'金额':<12} {'状态':<15}")
    print("-" * 51)

    for result in results:
        status_display = "✅ 已完成" if result["status"] == OrderStatus.COMPLETED else "❌ 已拒绝"
        print(f"{result['order_id']:<12} {result['customer_name']:<12} "
              f"¥{result['total_amount']:<10.2f} {status_display:<15}")

    # 总金额统计
    total_approved = sum(r["total_amount"] for r in approved)
    total_rejected = sum(r["total_amount"] for r in rejected)

    print(f"\n💰 金额统计:")
    print(f"   批准订单总额: ¥{total_approved:.2f}")
    print(f"   拒绝订单总额: ¥{total_rejected:.2f}")
    print(f"   全部订单总额: ¥{total_approved + total_rejected:.2f}")


def main():
    """主菜单"""
    while True:
        print_header("Human-in-the-Loop Agent 演示菜单")

        print("\n请选择演示模式:")
        print("  1. 📝 交互式单个订单处理")
        print("  2. 📦 批量订单处理")
        print("  3. ❌ 退出")

        choice = input("\n请输入选择 (1/2/3): ").strip()

        if choice == "1":
            try:
                interactive_order_processing()
            except KeyboardInterrupt:
                print("\n\n⚠️  已取消操作")
            except Exception as e:
                print(f"\n❌ 出错: {e}")

        elif choice == "2":
            try:
                batch_processing()
            except KeyboardInterrupt:
                print("\n\n⚠️  已取消操作")
            except Exception as e:
                print(f"\n❌ 出错: {e}")

        elif choice == "3":
            print("\n👋 再见!")
            break

        else:
            print("\n❌ 无效选择，请输入 1、2 或 3")

        input("\n按 Enter 继续...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 程序已退出")

