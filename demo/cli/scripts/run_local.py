"""
本地运行 LangGraph Agent

这个脚本可以在不使用 LangGraph CLI 的情况下本地运行 Agent。
"""

import sys
from pathlib import Path

# 添加项目路径（脚本在 scripts/ 目录，需要向上一级到项目根目录）
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agent.graph import run_agent_locally


if __name__ == "__main__":
    try:
        run_agent_locally()
    except KeyboardInterrupt:
        print("\n\n👋 Agent 已停止")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        sys.exit(1)

