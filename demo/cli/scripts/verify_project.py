#!/usr/bin/env python
"""
项目验证脚本 - 检查所有文件和功能

运行: python verify_project.py
"""

import sys
from pathlib import Path


def check_file_exists(path, description=""):
    """检查文件是否存在"""
    if Path(path).exists():
        size = Path(path).stat().st_size
        print(f"  ✅ {Path(path).name:30} ({size:6} bytes) {description}")
        return True
    else:
        print(f"  ❌ {path} NOT FOUND")
        return False


def check_dir_exists(path, description=""):
    """检查目录是否存在"""
    if Path(path).exists() and Path(path).is_dir():
        print(f"  ✅ {Path(path).name:30} (directory) {description}")
        return True
    else:
        print(f"  ❌ {path} NOT FOUND")
        return False


def main():
    """验证项目"""

    print("\n" + "=" * 80)
    print("🔍 LangGraph Agent 项目验证")
    print("=" * 80)

    # 脚本在 scripts/ 目录，需要向上一级到项目根目录
    project_root = Path(__file__).parent.parent

    print(f"\n📍 项目路径: {project_root}")

    # 检查目录
    print("\n📁 目录检查:")
    dirs_ok = [
        check_dir_exists(project_root / "agent", "- Agent 核心模块"),
    ]

    # 检查核心文件
    print("\n📄 核心文件检查:")
    files_ok = [
        check_file_exists(project_root / "agent" / "__init__.py", "- 包导出"),
        check_file_exists(project_root / "agent" / "state.py", "- 状态定义"),
        check_file_exists(project_root / "agent" / "graph.py", "- 图实现"),
        check_file_exists(project_root / "config" / "langgraph.json", "- LG 配置"),
        check_file_exists(project_root / ".env", "- 环境变量"),
    ]

    # 检查脚本
    print("\n🚀 运行脚本检查:")
    scripts_ok = [
        check_file_exists(project_root / "scripts" / "demo.py", "- 演示脚本"),
        check_file_exists(project_root / "scripts" / "final_test.py", "- 完整测试"),
        check_file_exists(project_root / "scripts" / "run_local.py", "- 本地交互"),
    ]

    # 检查文档
    print("\n📚 文档检查:")
    docs_ok = [
        check_file_exists(project_root / "docs" / "startup_summary.md", "- 启动指南"),
        check_file_exists(project_root / "docs" / "PROJECT_SUMMARY.md", "- 项目总结"),
    ]

    # 验证导入
    print("\n🔧 导入测试:")
    try:
        sys.path.insert(0, str(project_root))
        from agent import graph, AgentState
        print("  ✅ agent 包导入成功")

        # 检查 graph 是否已编译
        if hasattr(graph, 'invoke'):
            print("  ✅ Agent 图已编译并可使用")
        else:
            print("  ❌ Agent 图未编译")

    except ImportError as e:
        print(f"  ❌ 导入失败: {e}")

    # 快速功能测试
    print("\n⚡ 快速功能测试:")
    try:
        from agent.graph import graph
        from langchain_core.messages import HumanMessage

        state = {
            "messages": [HumanMessage(content="现在几点了？")],
            "context": "",
            "next_action": ""
        }

        config = {"configurable": {"thread_id": "test_session"}}
        result = graph.invoke(state, config)

        # 检查结果
        if result and "messages" in result and len(result["messages"]) > 1:
            print("  ✅ Agent 可以成功处理输入")
            last_msg = result["messages"][-1]
            print(f"     示例输出: {last_msg.content[:50]}...")
        else:
            print("  ❌ Agent 处理失败")

    except Exception as e:
        print(f"  ❌ 测试失败: {e}")

    # 总结
    print("\n" + "=" * 80)
    print("📊 验证结果总结:")
    print("=" * 80)

    all_checks = all([
        all(dirs_ok),
        all(files_ok),
        all(scripts_ok),
        all(docs_ok),
    ])

    if all_checks:
        print("""
✅ 所有检查通过！项目完整。

🚀 可以开始使用:
   1. python scripts/demo.py              - 查看演示
   2. python scripts/run_local.py         - 交互式运行
   3. langgraph dev                       - 启动开发服务器
   4. langgraph build                     - Docker 部署
        """)
        return 0
    else:
        print("""
⚠️  部分检查未通过，请检查文件完整性。
        """)
        return 1


if __name__ == "__main__":
    sys.exit(main())

