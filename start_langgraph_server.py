#!/usr/bin/env python3
"""
启动 LangGraph 服务器的示例脚本

根据文档 https://www.aidoczh.com/langgraph/tutorials/langgraph-platform/local-server/
使用 Python 方式启动 LangGraph 服务器
"""

import subprocess
import sys
from pathlib import Path

def check_prerequisites():
    """检查必要的环境和工具"""
    print("=" * 60)
    print("📋 检查启动前置条件")
    print("=" * 60)

    # 检查 Python 版本
    version_info = sys.version_info
    if version_info.major < 3 or (version_info.major == 3 and version_info.minor < 11):
        print(f"❌ Python 版本过低: {version_info.major}.{version_info.minor}")
        print("   需要 Python >= 3.11")
        sys.exit(1)
    print(f"✓ Python 版本: {version_info.major}.{version_info.minor}.{version_info.micro}")

    # 检查 langgraph CLI
    try:
        result = subprocess.run(["langgraph", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ LangGraph CLI: {result.stdout.strip()}")
        else:
            print("❌ LangGraph CLI 未安装或无法运行")
            sys.exit(1)
    except FileNotFoundError:
        print("❌ LangGraph CLI 未安装")
        print("   运行: pip install -U 'langgraph-cli[inmem]' python-dotenv")
        sys.exit(1)

    print()

def create_sample_app(app_path):
    """创建一个示例 LangGraph 应用"""
    print("=" * 60)
    print("🌱 创建 LangGraph 应用示例")
    print("=" * 60)

    app_path = Path(app_path)

    if app_path.exists():
        print(f"⚠️  应用目录已存在: {app_path}")
        return

    # 使用 langgraph CLI 创建应用
    print(f"📦 从 react-agent-python 模板创建应用...")
    result = subprocess.run(
        ["langgraph", "new", str(app_path), "--template", "react-agent-python"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(f"✓ 应用已创建: {app_path}")
    else:
        print(f"❌ 创建应用失败: {result.stderr}")
        sys.exit(1)

    print()

def create_env_file(app_path):
    """创建 .env 文件"""
    print("=" * 60)
    print("🔑 配置环境变量")
    print("=" * 60)

    app_path = Path(app_path)
    env_file = app_path / ".env"
    env_example = app_path / ".env.example"

    if env_file.exists():
        print(f"⚠️  .env 文件已存在: {env_file}")
        return

    if env_example.exists():
        print(f"📄 复制 .env.example 到 .env...")
        with open(env_example, 'r') as f:
            content = f.read()
        with open(env_file, 'w') as f:
            f.write(content)
        print(f"✓ .env 文件已创建")
        print(f"  📝 请编辑 {env_file} 并填写必要的 API 密钥:")
        print("     - LANGSMITH_API_KEY (LangSmith 设置页面)")
        print("     - ANTHROPIC_API_KEY (从 Anthropic 获取)")
        print("     - OPENAI_API_KEY (从 OpenAI 获取)")
        print("     - TAVILY_API_KEY (从 Tavily 网站获取)")
    else:
        print(f"⚠️  .env.example 不存在，请手动创建 .env 文件")

    print()

def install_dependencies(app_path):
    """安装应用依赖"""
    print("=" * 60)
    print("📦 安装依赖")
    print("=" * 60)

    app_path = Path(app_path)

    print(f"🔧 在编辑模式下安装依赖...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-e", "."],
        cwd=str(app_path),
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(f"✓ 依赖已安装")
    else:
        print(f"⚠️  安装过程中出现警告或错误:")
        print(result.stderr[-500:] if len(result.stderr) > 500 else result.stderr)

    print()

def start_server(app_path):
    """启动 LangGraph 服务器"""
    print("=" * 60)
    print("🚀 启动 LangGraph 服务器")
    print("=" * 60)

    app_path = Path(app_path)

    print(f"📍 应用路径: {app_path}")
    print(f"")
    print(f"运行命令: langgraph dev")
    print(f"")
    print(f"服务器启动后，你将看到:")
    print(f"  • API: http://localhost:8123/")
    print(f"  • 文档: http://localhost:8123/docs")
    print(f"  • LangGraph Studio: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8123")
    print(f"")
    print("=" * 60)
    print()

    # 启动服务器
    try:
        result = subprocess.run(
            ["langgraph", "dev"],
            cwd=str(app_path)
        )
    except KeyboardInterrupt:
        print("\n\n✋ 服务器已停止")
        sys.exit(0)

def main():
    """主函数"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "   🚀 LangGraph 服务器启动指南 (Python 方式)".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    print()

    # 应用路径
    app_path = "./my_langgraph_app"

    # 执行步骤
    check_prerequisites()
    create_sample_app(app_path)
    create_env_file(app_path)
    install_dependencies(app_path)

    print("=" * 60)
    print("✅ 所有准备工作完成！")
    print("=" * 60)
    print()

    # 启动服务器
    start_server(app_path)

if __name__ == "__main__":
    main()

