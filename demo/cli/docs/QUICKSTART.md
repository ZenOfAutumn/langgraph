# 🚀 快速入门指南

## 项目位置

```
/Users/wuliang/Workspace/github/langgraph/demo/cli
```

---

## ⚡ 5 秒快速开始

### 1️⃣ 查看演示（推荐）
```bash
cd /Users/wuliang/Workspace/github/langgraph/demo/cli
python demo.py
```

输出示例：
```
🤖 Agent: 当前时间是: 2026-02-01 11:44:29
🤖 Agent: LangGraph 是一个用于构建有状态多 actor 应用的框架
🤖 Agent: 10+5*2 = 20
```

✅ 完成！看到了 Agent 的工作。

---

## 🎮 互动式运行

```bash
python run_local.py
```

然后输入：
```
👤 你: 现在几点了？
🤖 Agent: 当前时间是: 2026-02-01 11:44:29

👤 你: 什么是 LangGraph？
🤖 Agent: LangGraph 是一个用于构建有状态多 actor 应用的框架

👤 你: quit
👋 再见!
```

---

## 🌐 开发服务器 (Web UI)

```bash
langgraph dev --port 8000 --host 127.0.0.1 --no-browser
```

访问: **http://localhost:8000**

功能：
- 📊 可视化 Agent 图
- 🔄 热重载
- 🐛 实时调试
- 📝 配置编辑

---

## 📊 项目验证

检查所有文件是否完整：
```bash
python verify_project.py
```

输出：
```
✅ agent/__init__.py (100 bytes)
✅ agent/state.py (500 bytes)
✅ agent/graph.py (12000 bytes)
✅ langgraph.json (300 bytes)
✅ .env (200 bytes)
✅ demo.py (5000 bytes)
...
```

---

## 📁 项目结构一览

```
demo/cli/
├── agent/
│   ├── __init__.py        # 包导出
│   ├── state.py           # 状态定义
│   └── graph.py           # Agent 核心
├── langgraph.json         # LG 配置
├── .env                   # 环境变量
├── demo.py                # 演示脚本 ⭐
├── run_local.py           # 本地运行 ⭐
├── final_test.py          # 完整测试
├── verify_project.py      # 项目验证
└── 📚 文档
    ├── QUICKSTART.md      # 本文件
    ├── startup_summary.md # 详细指南
    └── PROJECT_SUMMARY.md # 完整总结
```

---

## 🤖 Agent 能做什么？

| 功能 | 示例 | 工具 |
|------|------|------|
| ⏰ 时间 | "现在几点了？" | GetTime |
| 🔍 搜索 | "什么是 LangGraph?" | SearchKB |
| 🧮 计算 | "计算 10+5*2" | Calculate |
| 💬 聊天 | "你好" | Respond |

---

## 🔧 常用命令速查

```bash
# 查看演示
python demo.py

# 交互式运行
python run_local.py

# 启动 Web UI
langgraph dev --port 8000 --no-browser

# 构建 Docker 镜像
langgraph build -t my-agent:latest

# 验证项目
python verify_project.py

# 查看配置
cat langgraph.json

# 编辑环境变量
nano .env  # 或 vim / open
```

---

## 📚 文档导航

| 文档 | 内容 |
|------|------|
| **QUICKSTART.md** | 👈 你在这里 (5分钟入门) |
| **startup_summary.md** | 详细启动指南和扩展 |
| **PROJECT_SUMMARY.md** | 完整项目文档 |

---

## 💡 使用技巧

### 🎯 快速体验
```bash
python demo.py && echo "✨ 演示完成！"
```

### 🔄 循环测试
```bash
while true; do python demo.py; sleep 2; done
```

### 📊 监控输出
```bash
python run_local.py | tee session.log
```

---

## ❓ 常见问题

**Q: 如何修改 Agent 的行为？**
- 编辑 `agent/graph.py` 中的 `think_and_plan()` 函数

**Q: 如何添加新工具？**
- 在 `agent/graph.py` 中添加新函数和路由逻辑

**Q: 如何集成 LLM？**
- 使用 `langchain_openai.ChatOpenAI` (参考 startup_summary.md)

**Q: 如何保存对话历史？**
- 使用 `SqliteSaver` 替代 `MemorySaver`

---

## 🚀 下一步

1. ✅ 已完成: 本地开发环境建立
2. 📝 推荐: 修改 Agent 逻辑，添加自己的工具
3. 🌐 生产: 使用 `langgraph build` 部署

---

## 📞 获取帮助

- 📖 [LangGraph 官方文档](https://langchain-ai.github.io/langgraph/)
- 🔍 查看 `startup_summary.md` 了解详细信息
- 📊 运行 `python verify_project.py` 检查项目状态

---

**祝你使用愉快！** 🎉

开始: `python demo.py`

