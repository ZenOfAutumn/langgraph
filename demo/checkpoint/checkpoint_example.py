"""
LangGraph Checkpoint 工作原理演示

这个示例展示了：
1. 如何使用 checkpoint 保存图的执行状态
2. 如何从 checkpoint 恢复并继续执行
3. 为什么 checkpoint 对长流程很重要
"""

import time
from typing import TypedDict

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph, START, END


# 定义状态（State）
class ProcessState(TypedDict):
    """处理流程的状态"""
    step: int                    # 当前步骤
    messages: list               # 消息列表
    result: str                  # 最终结果
    timestamps: list             # 时间戳记录


# 定义节点函数
def step1_data_collection(state: ProcessState) -> ProcessState:
    """步骤1: 数据收集"""
    print("\n📥 [步骤1] 开始数据收集...")
    time.sleep(1)  # 模拟长时间操作

    state["step"] = 1
    state["messages"].append("✓ 数据收集完成")
    state["timestamps"].append(("step1", time.time()))
    print(f"   消息: {state['messages'][-1]}")

    return state


def step2_data_processing(state: ProcessState) -> ProcessState:
    """步骤2: 数据处理"""
    print("\n⚙️  [步骤2] 开始数据处理...")
    time.sleep(1)  # 模拟长时间操作

    state["step"] = 2
    state["messages"].append("✓ 数据处理完成")
    state["timestamps"].append(("step2", time.time()))
    print(f"   消息: {state['messages'][-1]}")

    return state


def step3_data_analysis(state: ProcessState) -> ProcessState:
    """步骤3: 数据分析"""
    print("\n🔍 [步骤3] 开始数据分析...")
    time.sleep(1)  # 模拟长时间操作

    state["step"] = 3
    state["messages"].append("✓ 数据分析完成")
    state["timestamps"].append(("step3", time.time()))
    print(f"   消息: {state['messages'][-1]}")

    return state


def step4_generate_report(state: ProcessState) -> ProcessState:
    """步骤4: 生成报告"""
    print("\n📊 [步骤4] 开始生成报告...")
    time.sleep(1)  # 模拟长时间操作

    state["step"] = 4
    state["messages"].append("✓ 报告生成完成")
    state["timestamps"].append(("step4", time.time()))
    state["result"] = f"报告已生成，包含 {len(state['messages'])} 个处理步骤"
    print(f"   消息: {state['messages'][-1]}")

    return state


def create_graph_with_checkpoint():
    """创建带 checkpoint 的图"""

    # 初始化 SqliteSaver 作为 checkpoint 存储
    checkpoint_dir = "/tmp/langgraph_checkpoints"
    checkpointer = SqliteSaver.from_conn_string(
        f"sqlite:///{checkpoint_dir}/checkpoints.db"
    )

    # 创建状态图
    graph = StateGraph(ProcessState)

    # 添加节点
    graph.add_node("step1", step1_data_collection)
    graph.add_node("step2", step2_data_processing)
    graph.add_node("step3", step3_data_analysis)
    graph.add_node("step4", step4_generate_report)

    # 定义边（流程）
    graph.add_edge(START, "step1")
    graph.add_edge("step1", "step2")
    graph.add_edge("step2", "step3")
    graph.add_edge("step3", "step4")
    graph.add_edge("step4", END)

    # 编译图，启用 checkpoint
    compiled_graph = graph.compile(checkpointer=checkpointer)

    return compiled_graph, checkpointer


def demo_checkpoint_workflow():
    """演示 checkpoint 的工作流程"""

    print("=" * 70)
    print("🚀 LangGraph Checkpoint 工作原理演示")
    print("=" * 70)

    # 创建图
    graph, checkpointer = create_graph_with_checkpoint()

    # 初始状态
    initial_state = {
        "step": 0,
        "messages": [],
        "result": "",
        "timestamps": []
    }

    # 配置：启用 checkpoint，使用 thread_id 作为会话标识
    config = {"configurable": {"thread_id": "workflow_001"}}

    print("\n📌 执行场景1：完整流程执行")
    print("-" * 70)

    try:
        # 第一次执行：完整流程
        result = graph.invoke(initial_state, config)

        print("\n✅ 流程执行完成!")
        print(f"   最终结果: {result['result']}")
        print(f"   处理步骤: {result['messages']}")
        print(f"   总耗时: {len(result['timestamps'])} 个步骤")

    except Exception as e:
        print(f"❌ 执行出错: {e}")
        print(f"   这模拟了长流程中可能出现的故障")
        print(f"   Checkpoint 已自动保存进度")

    # 演示如何查看 checkpoint
    print("\n" + "=" * 70)
    print("💾 Checkpoint 存储信息")
    print("=" * 70)

    try:
        # 查看已保存的 checkpoint
        saved_checkpoints = checkpointer.get_tuple(config)
        if saved_checkpoints:
            print(f"\n✓ 找到已保存的 checkpoint:")
            print(f"  Thread ID: {config['configurable']['thread_id']}")
            print(f"  最后保存状态:")
            checkpoint_data = saved_checkpoints[0]
            print(f"    - 当前步骤: {checkpoint_data.values.get('step', 'N/A')}")
            print(f"    - 消息数: {len(checkpoint_data.values.get('messages', []))}")
    except Exception as e:
        print(f"   (查看 checkpoint 需要数据库访问权限: {type(e).__name__})")

    # 演示从 checkpoint 恢复
    print("\n" + "=" * 70)
    print("🔄 演示：从 Checkpoint 恢复并继续执行")
    print("=" * 70)
    print("\n📌 场景说明：")
    print("  假设第一次执行在步骤2时发生故障，现在从 checkpoint 恢复")
    print("  Checkpoint 会保存已完成的步骤，避免重复执行")

    # 使用相同的 thread_id 再次执行
    # LangGraph 会检查 checkpoint，决定是否恢复状态
    print("\n⏳ 使用相同的 thread_id 重新执行（应该更快）...")

    try:
        result_resumed = graph.invoke(initial_state, config)
        print("\n✅ 恢复执行完成!")
        print(f"   最终结果: {result_resumed['result']}")
    except Exception as e:
        print(f"❌ 恢复执行失败: {e}")

    # 演示使用不同的 thread_id
    print("\n" + "=" * 70)
    print("🆕 演示：使用新的 thread_id（新的独立流程）")
    print("=" * 70)

    new_config = {"configurable": {"thread_id": "workflow_002"}}
    print(f"\n📌 使用新的 thread_id: {new_config['configurable']['thread_id']}")
    print("   这将开始一个全新的流程，不受前面 checkpoint 的影响")

    result_new = graph.invoke(initial_state, new_config)
    print(f"\n✅ 新流程执行完成!")
    print(f"   最终结果: {result_new['result']}")


def demo_checkpoint_benefits():
    """演示 checkpoint 的好处"""

    print("\n" + "=" * 70)
    print("💡 Checkpoint 的主要好处")
    print("=" * 70)

    benefits = [
        ("🛡️  容错恢复",
         "当系统故障时，可以从最后一个 checkpoint 恢复，\n"
         "         无需重新执行整个流程"),

        ("⚡ 性能优化",
         "在分布式系统中，checkpoint 允许不同的工作者\n"
         "         从已保存的状态继续执行"),

        ("📊 可观测性",
         "记录流程的每个阶段状态，便于调试和审计"),

        ("🔄 状态管理",
         "为每个独立的会话维护独立的状态（通过 thread_id），\n"
         "         支持并发处理多个流程"),

        ("💾 持久化",
         "将复杂流程的中间状态持久化到数据库，\n"
         "         支持长期运行的任务"),
    ]

    for title, description in benefits:
        print(f"\n{title}")
        print(f"  {description}")


if __name__ == "__main__":
    # 执行演示
    demo_checkpoint_workflow()

    # 显示 checkpoint 的好处
    demo_checkpoint_benefits()

    print("\n" + "=" * 70)
    print("✨ 演示完成!")
    print("=" * 70)

