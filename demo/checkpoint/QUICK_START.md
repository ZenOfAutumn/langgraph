# 快速开始 - Checkpoint 演示

## 5 分钟快速理解

### 什么是 Checkpoint？

想象你在做一个多步骤的任务：

```
步骤1 (收集数据) ✓ 完成 → 保存快照1
    ↓
步骤2 (处理数据) ✓ 完成 → 保存快照2
    ↓
步骤3 (分析数据) ✓ 完成 → 保存快照3
    ↓
步骤4 (生成报告) ✗ 失败 → 可从快照3恢复!
```

**Checkpoint 就是这些快照**。当系统故障时，不需要从头开始，可以从最后一个成功点继续。

## 核心代码

### 1️⃣ 创建 Checkpoint 存储

```python
from langgraph.checkpoint.sqlite import SqliteSaver

# 使用 SQLite（开发环境）
checkpointer = SqliteSaver.from_conn_string(
    "sqlite:////tmp/langgraph_checkpoints/checkpoints.db"
)

# 生产环境使用 PostgreSQL
# checkpointer = PostgresSaver.from_conn_string(
#     "postgresql://user:password@localhost/db"
# )
```

### 2️⃣ 启用 Checkpoint

```python
# 编译图时启用 checkpoint
compiled_graph = graph.compile(checkpointer=checkpointer)
```

### 3️⃣ 执行流程

```python
# 定义配置（thread_id 是关键）
config = {"configurable": {"thread_id": "order_001"}}

# 执行工作流
result = compiled_graph.invoke(initial_state, config)

# 再次执行相同 thread_id 时
# LangGraph 会检查 checkpoint，决定是否恢复
result = compiled_graph.invoke(initial_state, config)  # 自动恢复!
```

## 关键概念

| 概念 | 说明 | 示例 |
|------|------|------|
| **thread_id** | 流程的唯一标识 | `"order_001"`, `"user_123"` |
| **Checkpoint** | 执行阶段的状态快照 | 完整的变量、计算结果 |
| **恢复** | 从上次保存点继续执行 | 系统重启后自动继续 |

## 运行演示

### 方式1: 简化版 (推荐)

```bash
cd /Users/wuliang/Workspace/github/langgraph/demo
python simple_checkpoint_demo.py
```

输出示例：
```
🛒 订单处理工作流 - 基本演示
   ✓ 验证订单 ORDER-001
   ✓ 处理支付 ORDER-001
   ✓ 打包物品 ORDER-001
   ✓ 发货 ORDER-001

⚡ 并行处理多个订单 - 演示
   每个订单独立执行，互不干扰
```

### 方式2: 完整版

```bash
python checkpoint_example.py
```

更详细的说明和高级用法。

## 三个核心场景

### 场景1: 基本流程

```python
# 第一次执行
config = {"configurable": {"thread_id": "flow_001"}}
result = graph.invoke(state, config)  # 完整执行，自动保存

# 如果系统故障...
# 重启系统后，使用相同的 thread_id
result = graph.invoke(state, config)  # 自动恢复!
```

### 场景2: 长流程处理

```python
# 支持运行很长时间的流程
# 中途可以暂停/恢复
# Checkpoint 会保存中间状态

for step in long_process:
    result = graph.invoke(state, config)
    # 每个步骤都有 checkpoint，支持中断恢复
```

### 场景3: 并发处理多个任务

```python
tasks = ["task_001", "task_002", "task_003"]

for task_id in tasks:
    config = {"configurable": {"thread_id": task_id}}
    # 每个任务有独立的 checkpoint
    # 完全并发，互不干扰
    graph.invoke(state, config)
```

## 常见问题

**Q: 为什么需要 checkpoint？**

A:
- 🛡️ **故障恢复** - 不用重新开始
- ⚡ **效率** - 避免重复处理
- 📊 **可见性** - 清楚地看到进度
- 🔄 **并发** - 支持多个独立流程

**Q: thread_id 有什么作用？**

A: 它是流程的**唯一标识**。相同 thread_id 的执行会共享 checkpoint，不同 thread_id 是完全独立的流程。

**Q: Checkpoint 存在哪里？**

A: 默认使用 SQLite（开发）或 PostgreSQL（生产）。可自定义存储位置。

**Q: 会影响性能吗？**

A: 有轻微影响（IO操作），但对大多数应用可以忽略。好处远大于成本。

## 数据库查看

### 查看 SQLite 中的 Checkpoint

```bash
# 打开数据库
sqlite3 /tmp/langgraph_checkpoints/checkpoints.db

# 查看 checkpoints 表
sqlite> .tables
sqlite> SELECT * FROM checkpoints;

# 查看特定 thread 的数据
sqlite> SELECT thread_id, checkpoint_id, timestamp FROM checkpoints
        WHERE thread_id = 'ORDER-001';
```

## 文件结构

```
demo/
├── README.md                    # 详细说明
├── QUICK_START.md              # 本文件（快速入门）
├── simple_checkpoint_demo.py   # ⭐ 推荐首先运行
├── checkpoint_example.py       # 完整版本
└── checkpoint_usage_guide.md   # 概念深入讲解
```

## 学习步骤

1. **5分钟** - 读这个文件，理解基本概念
2. **10分钟** - 运行 `simple_checkpoint_demo.py`
3. **20分钟** - 研究代码，理解实现细节
4. **∞分钟** - 在自己项目中应用

## 下一步

✅ 基本理解完成

现在你可以：
- 在自己的 LangGraph 项目中启用 checkpoint
- 使用 thread_id 隔离不同的流程
- 支持长时间运行的复杂工作流

## 生产建议

```python
# ❌ 开发环境可以这样
checkpointer = SqliteSaver.from_conn_string(
    "sqlite:////tmp/checkpoints.db"
)

# ✅ 生产环境应该这样
from langgraph.checkpoint.postgres import PostgresSaver

checkpointer = PostgresSaver.from_conn_string(
    "postgresql://user:password@prod-host/langgraph_db"
)

# 配置数据库连接池
checkpointer.setup()
```

## 需要帮助？

📖 查看 `checkpoint_usage_guide.md` 了解更多细节

💻 查看 `simple_checkpoint_demo.py` 中的代码注释

🔬 查看 `checkpoint_example.py` 了解高级用法

---

**现在开始吧！** 🚀

```bash
python simple_checkpoint_demo.py

