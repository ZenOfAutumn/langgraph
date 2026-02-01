#!/bin/bash

# LangGraph 开发服务器启动脚本

set -e

VENV_PATH="/Users/wuliang/Workspace/github/langgraph/venv"
PROJECT_PATH="/Users/wuliang/Workspace/github/langgraph/demo/cli"

# 激活虚拟环境
source "${VENV_PATH}/bin/activate"

# 进入项目目录
cd "${PROJECT_PATH}"

echo "======================================================================="
echo "🚀 启动 LangGraph 开发服务器"
echo "======================================================================="
echo ""
echo "📍 项目路径: ${PROJECT_PATH}"
echo "📝 配置文件: config/langgraph.json"
echo ""
echo "🌐 访问地址:"
echo "   • Web UI: http://localhost:8123"
echo "   • API: http://localhost:8000"
echo ""
echo "💡 功能:"
echo "   • 热重载支持"
echo "   • 实时调试"
echo "   • 图形化界面"
echo ""
echo "按 Ctrl+C 停止服务器"
echo "======================================================================="
echo ""

# 启动开发服务器
langgraph dev

