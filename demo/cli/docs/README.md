# 🤖 LangGraph Agent 项目

一个完整、可生产的 LangGraph Agent 项目，展示了如何使用 LangGraph 框架构建有状态、多工具的智能代理。

## 🎯 项目概述

本项目提供了一个**开箱即用**的 LangGraph Agent 实现，包括：

- ✨ **完整的 Agent 图** - StateGraph 实现的最佳实践
- 🛠️ **工具系统** - 时间查询、知识库搜索、数学计算
- 🔄 **条件分支路由** - 智能决策和流程控制
- 💾 **状态管理** - Checkpoint 和消息历史
- 🚀 **多种运行方式** - 本地、Web UI、Docker
- 📚 **详细文档** - 启动指南、扩展教程、最佳实践

---

## ⚡ 快速开始 (30 秒)

### 1. 查看演示
```bash
cd /Users/wuliang/Workspace/github/langgraph/demo/cli
python demo.py
```

**输出示例:**
```
【演示 1】获取当前时间
👤 用户: 现在几点了？
🤖 Agent: 当前时间是: 2026-02-01 11:44:29

【演示 2】搜索知识库
👤 用户: 什么是 LangGraph？
🤖 Agent: LangGraph 是一个用于构建有状态多 actor 应用的框架

【演示 3】数学计算
👤 用户: 计算 10+5*2
🤖 Agent: 10+5*2 = 20
```

### 2. 本地交互式运行
```bash
python run_local.py
```

### 3. 启动 Web 开发界面
```bash
langgraph dev --port 8000 --host 127.0.0.1 --no-browser
```

访问: http://localhost:8000

---

## 📁 项目结构

```
demo/cli/
│
├── 📂 agent/                        # Agent 核心模块
│   ├── __init__.py                 # 包导出
│   ├── state.py                    # Agent 状态定义 (18 行)
│   └── graph.py                    # Agent 图实现 (293 行)
│
├── ⚙️  配置文件
│   ├── langgraph.json              # LangGraph 配置
│   └── .env                        # 环境变量
│
├── 🚀 运行脚本
│   ├── demo.py                     # 自动演示脚本 (130 行)
│   ├── run_local.py                # 本地交互运行 (20 行)
│   ├── final_test.py               # 完整测试脚本 (180 行)
│   └── verify_project.py           # 项目验证脚本
│
└── 📚 文档
    ├── README.md                   # 本文件
    ├── QUICKSTART.md               # 5 分钟快速入门
    ├── startup_summary.md          # 详细启动指南
    └── PROJECT_SUMMARY.md          # 完整项目文档
```

---

## 🤖 Agent 功能

### 工具列表

| 工具 | 功能 | 触发词 | 示例 |
|------|------|--------|------|
| **时间** | 获取当前时间 | "时间", "现在", "几点" | "现在几点了？" |
| **搜索** | 知识库搜索 | "查询", "搜索", "关于", "什么" | "什么是 LangGraph?" |
| **计算** | 数学计算 | "计算", "算", "等于" | "计算 10+5*2" |

### 图结构

```
START
  ↓
[process_input] → 处理输入
  ↓
[think_and_plan] → 智能决策
  │
  ├─→ [use_tool_time] → 获取时间
  ├─→ [use_tool_search] → 知识库搜索
  ├─→ [use_tool_calculate] → 数学计算
  └─→ [respond] → 通用回复
  │
  ↓
[respond] → 生成最终响应
  ↓
END
```

---

## 🚀 使用方式

### 方式 1: 快速演示 ⭐⭐⭐
```bash
python demo.py
```
- 自动运行 4 个演示场景
- 无需交互输入
- 快速查看功能效果

### 方式 2: 本地交互式 ⭐⭐
```bash
python run_local.py
```
- 实时输入查询
- 即时获得回复
- 支持多轮对话

### 方式 3: Web 开发界面 ⭐⭐⭐
```bash
langgraph dev --port 8000 --host 127.0.0.1 --no-browser
```
- 访问 http://localhost:8000
- 可视化编辑 Agent
- 热重载和实时调试

### 方式 4: Docker 部署
```bash
langgraph build -t my-agent:latest
docker run -p 8000:8000 my-agent:latest
```

---

## 🔧 核心实现

### 状态定义 (agent/state.py)
```python
class AgentState(TypedDict):
    messages: Sequence[BaseMessage]  # 消息历史
    context: str                     # 上下文信息
    next_action: str                 # 下一步操作
```

### Agent 图 (agent/graph.py)
```python
# 6 个计算节点
1. process_input       # 输入处理
2. think_and_plan      # 智能决策
3. use_tool_time       # 时间工具
4. use_tool_search     # 搜索工具
5. use_tool_calculate  # 计算工具
6. respond             # 最终响应

# 条件分支路由
if "时间" in input → use_tool_time
elif "搜索" in input → use_tool_search
elif "计算" in input → use_tool_calculate
else → respond
```

### Checkpoint 支持
```python
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()
graph = StateGraph(AgentState)
compiled_graph = graph.compile(checkpointer=checkpointer)
```

---

## 📚 文档导航

| 文档 | 用途 | 阅读时间 |
|------|------|---------|
| **QUICKSTART.md** | 5 分钟入门 | 5 分钟 |
| **startup_summary.md** | 详细启动和扩展指南 | 15 分钟 |
| **PROJECT_SUMMARY.md** | 完整项目文档 | 30 分钟 |

---

## 🎓 学习路径

### 初级 (入门阶段)
1. 📖 阅读 QUICKSTART.md
2. 🏃 运行 `python demo.py`
3. 🎮 尝试 `python run_local.py`

### 中级 (深入学习)
1. 📚 阅读 startup_summary.md
2. 🔍 研究 agent/graph.py 源码
3. ✏️ 修改路由逻辑和工具函数

### 高级 (扩展应用)
1. 🛠️ 添加自定义工具
2. 🧠 集成 LLM (ChatOpenAI)
3. 💾 实现 SQLite 持久化
4. 🚀 Docker 部署

---

## 🔨 扩展指南

### 添加新工具 (3 步)

**步骤 1: 定义工具函数**
```python
def my_tool(input: str) -> str:
    """工具描述"""
    return "结果"
```

**步骤 2: 添加路由条件**
```python
if "关键词" in user_input:
    state["next_action"] = "use_tool_my"
```

**步骤 3: 实现 Node 函数**
```python
def use_tool_my(state: AgentState) -> AgentState:
    result = my_tool(user_input)
    state["messages"].append(AIMessage(content=result))
    return state
```

更多详情，参考 startup_summary.md

---

## 📊 项目特性

### ✅ 完整性
- [x] StateGraph 完整实现
- [x] 6 个计算节点
- [x] 条件分支路由
- [x] 消息历史管理
- [x] Checkpoint 支持

### ✅ 生产就绪
- [x] 模块化设计
- [x] 清晰的代码注释
- [x] 错误处理
- [x] 标准配置文件
- [x] Docker 支持

### ✅ 开发友好
- [x] 多种运行方式
- [x] 详细的文档
- [x] 演示脚本
- [x] 验证工具
- [x] CLI 集成

### ✅ 教学价值
- [x] 代码注释详细
- [x] 架构清晰
- [x] 逐步教程
- [x] 最佳实践示例

---

## 💡 技术栈

- **LangGraph** (1.0.6+) - 有状态 Agent 框架
- **Langchain Core** - 核心库
- **Python** (3.11+) - 运行环境
- **FastAPI/Uvicorn** - Dev 服务器
- **SQLite** (可选) - 数据持久化

---

## 📋 检查清单

项目完成度：
- [x] 项目结构搭建
- [x] Agent 核心实现 (293 行)
- [x] 状态管理系统
- [x] 工具系统集成
- [x] 条件分支路由
- [x] LangGraph.json 配置
- [x] 演示脚本完成
- [x] 验证脚本实现
- [x] 文档编写
  - [x] 快速入门 (QUICKSTART.md)
  - [x] 详细指南 (startup_summary.md)
  - [x] 项目总结 (PROJECT_SUMMARY.md)
  - [x] README (本文件)

---

## 🚀 后续步骤

### 立即可做
```bash
python demo.py                    # 查看演示
python run_local.py               # 交互式运行
langgraph dev --port 8000         # Web UI
```

### 短期计划
- 添加自定义工具
- 集成 OpenAI GPT
- 实现 SQLite 持久化

### 长期计划
- 多 Agent 协作
- 完整应用系统
- 生产环境部署

---

## ❓ FAQ

**Q: 如何修改 Agent 行为?**
> 编辑 `agent/graph.py` 中的 `think_and_plan()` 和 `use_tool_*()` 函数

**Q: 如何添加新工具?**
> 参考 startup_summary.md 中的扩展指南

**Q: 如何集成 LLM?**
> 使用 `langchain_openai.ChatOpenAI`

**Q: 如何部署到生产?**
> 使用 `langgraph build` 创建 Docker 镜像

**Q: 支持哪些数据库?**
> MemorySaver (内存), SqliteSaver (SQLite), PostgresSaver (Postgres)

---

## 🔗 相关资源

### 官方文档
- [LangGraph 官方文档](https://langchain-ai.github.io/langgraph/)
- [LangChain Python](https://python.langchain.com/)

### 项目示例
- `demo/checkpoint/` - Checkpoint 示例
- `demo/interrupt/` - Human-in-the-Loop 示例
- `examples/` - 各种应用场景

---

## 📞 支持

- 📖 查看 QUICKSTART.md 快速入门
- 📚 查看 startup_summary.md 详细指南
- 🔍 运行 `python verify_project.py` 验证项目
- 📊 查看 PROJECT_SUMMARY.md 完整文档

---

## 📈 项目统计

| 指标 | 数值 |
|------|------|
| 代码行数 | ~900+ |
| 文档大小 | ~1000+ 行 |
| 脚本数量 | 5 个 |
| 文档数量 | 4 个 |
| 完成度 | 100% |

---

## 🎉 总结

这是一个**完整、可生产、开箱即用**的 LangGraph Agent 项目。无论是学习 LangGraph 框架，还是构建实际应用，都能从中获得价值。

**推荐开始:**
```bash
python demo.py
```

**祝你使用愉快！** 🚀

---

*项目完成日期: 2026-02-01*
*LangGraph 版本: 1.0.6*
*Python 版本: 3.11+*

