"""
测试 LangGraph 开发服务器启动

这个脚本会启动 langgraph dev 服务器并检查是否能正常启动。
"""

import subprocess
import sys
import time
from pathlib import Path


def main():
    """启动开发服务器并测试"""

    print("\n" + "=" * 70)
    print("🚀 启动 LangGraph 开发服务器")
    print("=" * 70)

    project_dir = Path(__file__).parent

    # 启动服务器
    print("\n📍 项目目录:", project_dir)
    print("⏳ 启动服务器中...\n")

    try:
        # 启动 langgraph dev
        process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "langgraph_cli.cli",
                "dev",
                "--port", "8000",
                "--host", "127.0.0.1",
                "--no-browser"
            ],
            cwd=str(project_dir),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # 等待 3 秒并读取输出
        print("⏱️  等待服务器启动...")
        time.sleep(3)

        # 检查进程是否还在运行
        if process.poll() is None:
            print("✅ 服务器启动成功！")
            print("\n📋 服务器信息:")
            print("   • Web UI: http://localhost:8000")
            print("   • API: http://localhost:8000/api")
            print("   • 项目配置: langgraph.json")
            print("\n💡 功能:")
            print("   • 热重载支持")
            print("   • 实时调试")
            print("   • 图形化界面")
            print("\n⏹️  按 Ctrl+C 停止服务器\n")

            # 读取一些初始输出
            try:
                # 使用 communicate 与短超时来获取一些输出
                stdout, stderr = process.communicate(timeout=2)
                if stdout:
                    print("📝 服务器输出:")
                    print(stdout[:500])  # 显示前500字符
                if stderr:
                    print("⚠️  错误输出:")
                    print(stderr[:500])
            except subprocess.TimeoutExpired:
                print("（服务器仍在运行...）")

            # 停止进程
            process.terminate()

        else:
            # 进程已经结束，读取输出
            stdout, stderr = process.communicate()
            print("❌ 服务器启动失败：")
            if stderr:
                print("\n📝 错误信息:")
                print(stderr)
            if stdout:
                print("\n📝 输出信息:")
                print(stdout)
            return 1

    except KeyboardInterrupt:
        print("\n\n👋 服务器已停止")
        if 'process' in locals():
            process.terminate()
    except Exception as e:
        print(f"❌ 错误: {e}")
        return 1

    print("\n" + "=" * 70)
    print("✨ 测试完成！")
    print("=" * 70)
    print("\n💡 下一步:")
    print("   1. 在生产环境使用: langgraph dev")
    print("   2. Docker 部署: langgraph up")
    print("   3. 查看所有选项: langgraph dev --help\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())

