#!/usr/bin/env python3
"""
最简单的 LangGraph 服务器启动脚本

用法: python simple_start_server.py
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, cwd=None, show_output=True, exit_on_error=True):
    """运行命令并返回结果"""
    if show_output:
        print(f"\n➤ 运行: {' '.join(cmd)}")
        if cwd:
            print(f"  在路径: {cwd}")

    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=not show_output,
        text=True
    )

    if result.returncode != 0:
        if not show_output:
            print(f"❌ 命令失败: {result.stderr}")
        if exit_on_error:
            return False

    return result.returncode == 0


def main():
    print("\n" + "=" * 70)
    print(" " * 15 + "🚀 LangGraph 服务器启动 (Python 方式)")
    print("=" * 70 + "\n")

    # 1. 检查 Python 版本
    print("1️⃣  检查 Python 版本...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print(f"   ❌ Python 版本过低: {version.major}.{version.minor} (需要 >= 3.11)")
        sys.exit(1)
    print(f"   ✓ Python {version.major}.{version.minor}.{version.micro}\n")

    # 2. 安装 LangGraph CLI
    print("2️⃣  安装 LangGraph CLI...")
    if not run_command([sys.executable, "-m", "pip", "install", "-U",
                        "langgraph-cli[inmem]", "python-dotenv"],
                       show_output=False, exit_on_error=False):
        print("   ⚠️  CLI 安装失败，但继续尝试...\n")
    else:
        print("   ✓ 已安装\n")

    # 3. 创建应用
    app_dir = "my_langgraph_app"
    if not Path(app_dir).exists():
        print(f"3️⃣  创建 LangGraph 应用 ({app_dir})...")
        if not run_command(["langgraph", "new", app_dir, "--template", "react-agent-python"],
                          show_output=True, exit_on_error=False):
            print("   ❌ 应用创建失败")
            print("   💡 确保网络连接正常，或手动运行:")
            print(f"      langgraph new {app_dir} --template react-agent-python")
            sys.exit(1)
        print("   ✓ 应用已创建\n")
    else:
        print(f"3️⃣  应用目录已存在 ({app_dir})\n")

    # 4. 安装依赖
    print("4️⃣  安装应用依赖...")
    if not run_command([sys.executable, "-m", "pip", "install", "-e", "."],
                       cwd=app_dir, show_output=False, exit_on_error=False):
        print("   ⚠️  依赖安装失败，但继续尝试启动...\n")
    else:
        print("   ✓ 依赖已安装\n")

    # 5. 启动服务器
    print("5️⃣  启动 LangGraph 服务器...")
    print("\n" + "=" * 70)
    print("   🎯 服务器启动信息:")
    print("   • API:     http://localhost:8123/")
    print("   • 文档:    http://localhost:8123/docs")
    print("   • Studio:  https://smith.langchain.com/studio/")
    print("             ?baseUrl=http://127.0.0.1:8123")
    print("=" * 70 + "\n")

    # 启动服务器
    try:
        run_command(["langgraph", "dev"], cwd=app_dir, show_output=True, exit_on_error=False)
    except FileNotFoundError:
        print("❌ langgraph 命令找不到")
        print("💡 请确保已安装: pip install -U 'langgraph-cli[inmem]'")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✋ 服务器已停止")
        sys.exit(0)

