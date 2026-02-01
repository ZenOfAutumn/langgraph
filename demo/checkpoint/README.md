# LangGraph Demo - Checkpoint 演示

本目录包含 LangGraph 的 checkpoint 机制演示。

## 📁 文件说明

### 1. `simple_checkpoint_demo.py` ⭐ (推荐首先运行)

简化版 checkpoint 演示，包含三个场景：

- **基本工作流** - 展示订单处理的完整流程
- **从 Checkpoint 恢复** - 演示故障恢复机制
- **并行处理多个订单** - 演示 thread_id 隔离

```bash
python simple_checkpoint_demo.py
```

### 2. `checkpoint_example.py`

完整版本，包含更详细的说明和高级用法。

```bash
python checkpoint_example.py
```

### 3. `checkpoint_usage_guide.md`

详细的 checkpoint 概念说明和使用指南。

## 🎯 核心概念

### Checkpoint 是什么？

Checkpoint 是图执行过程中的**状态快照**。

```
执行流程:
节点1 完成 → [保存 Checkpoint 1]
    ↓
节点2 完成 → [保存 Checkpoint 2]
    ↓
节点3 完成 → [保存 Checkpoint 3]
    ↓
若中途故障，可从最后的 Checkpoint 恢复
```

### 为什么重要？

| 特性 | 说明 |
|------|------|
| **容错恢复** | 系统故障时从最后状态继续，无需重新处理 |
| **效率** | 避免重复执行已完成的步骤 |
| **可观测** | 清晰追踪流程的每一步 |
| **并发** | 多个独立流程同时运行，互不干扰 |

### thread_id 的作用

`thread_id` 是流程的唯一标识：

```python
config = {"configurable": {"thread_id": "ORDER-001"}}

# 相同 thread_id 会共享 checkpoint
graph.invoke(state, config)  # 第一次执行
graph.invoke(state, config)  # 可从 checkpoint 恢复

# 不同 thread_id 是独立流程
config2 = {"configurable": {"thread_id": "ORDER-002"}}
graph.invoke(state, config2)  # 完全独立的流程
```

## 🚀 快速开始

### 前置要求

```bash
pip install langgraph
```

### 运行演示

```bash
# 简化版演示（推荐）
python simple_checkpoint_demo.py

# 完整版演示
python checkpoint_example.py
```

### 预期输出

```
======================================================================
🚀 LangGraph Checkpoint 完整演示
======================================================================

▶️ 订单处理工作流 - 基本演示
   ✓ 验证订单 ORDER-001
   ✓ 处理支付 ORDER-001
   ✓ 打包物品 ORDER-001
   ✓ 发货 ORDER-001

✅ 流程完成!
```

## 📊 Checkpoint 数据存储

演示使用 SQLite 存储（开发友好）：

```
/tmp/langgraph_demo/order_checkpoints.db
```

数据库结构：
```sql
-- Checkpoint 表
CREATE TABLE checkpoints (
    thread_id TEXT,           -- 流程标识
    checkpoint_id TEXT,       -- checkpoint 序号
    parent_checkpoint_id TEXT, -- 父 checkpoint
    values BLOB,             -- 状态数据
    metadata BLOB,           -- 元数据
    timestamp DATETIME       -- 时间戳
);
```

## 🔄 工作流程

```
用户创建流程
    ↓
指定 thread_id
    ↓
执行第一个节点 → 保存 Checkpoint 1
    ↓
执行第二个节点 → 保存 Checkpoint 2
    ↓
... (循环) ...
    ↓
流程完成

[若中途故障]
系统重启
    ↓
使用相同 thread_id 再次执行
    ↓
LangGraph 检查 checkpoint
    ↓
从最后一个成功的 checkpoint 继续
    ↓
完成流程
```

## 💡 实际应用

### 场景1: 电商订单处理

```
订单验证 → 支付处理 → 库存扣减 → 打包 → 发货

Checkpoint 优势：
✓ 支付失败后可立即重试
✓ 发货前任何环节失败都能恢复
✓ 不会重复扣库存或重复收费
```

### 场景2: 数据处理管道

```
数据导入 → 数据清洗 → 数据转换 → 数据验证 → 数据导出

Checkpoint 优势：
✓ 长时间运行不怕中断
✓ 可暂停和恢复
✓ 支持部分重新处理
```

### 场景3: 多步骤审批流程

```
申请 → 部门审核 → 总监审核 → 财务审核 → 执行

Checkpoint 优势：
✓ 每个审批步骤的状态都清晰可见
✓ 支持在任何环节查询进度
✓ 支持人工介入和修改
```

## ⚙️ 高级配置

### 使用 PostgreSQL（生产推荐）

```python
from langgraph.checkpoint.postgres import PostgresSaver

checkpointer = PostgresSaver.from_conn_string(
    "postgresql://user:password@localhost/langgraph_db"
)

graph.compile(checkpointer=checkpointer)
```

### 自定义 Checkpoint 存储

```python
from langgraph.checkpoint.base import BaseSaver

class CustomCheckpointer(BaseSaver):
    def put(self, config, values, metadata):
        # 自定义保存逻辑
        pass

    def get_tuple(self, config, checkpoint_id=None):
        # 自定义加载逻辑
        pass
```

## 📚 学习路径

1. 📖 **先读** `checkpoint_usage_guide.md` 理解概念
2. ▶️ **运行** `simple_checkpoint_demo.py` 看效果
3. 🔬 **研究** `checkpoint_example.py` 了解细节
4. 💻 **实践** 在自己的项目中应用

## 🎓 核心要点

✅ Checkpoint 自动保存每个节点执行后的状态

✅ 通过 `thread_id` 隔离不同流程

✅ 故障自动恢复，无需手动干预

✅ 支持长时间运行的复杂流程

✅ 生产环境推荐使用 PostgreSQL

## 📞 问题排查

**Q: 为什么 checkpoint 文件很大？**
A: Checkpoint 保存完整状态，包括所有中间结果。可考虑定期清理旧 checkpoint。

**Q: 多个流程并发执行会冲突吗？**
A: 不会，因为每个流程有独立的 thread_id，checkpoint 数据完全隔离。

**Q: Checkpoint 会影响性能吗？**
A: 会有小的延迟（IO操作），但在大多数情况下可以忽略。

## 📝 参考资源

- [LangGraph 官方文档](https://langchain-ai.github.io/langgraph/)
- [Checkpoint 完整 API](https://langchain-ai.github.io/langgraph/concepts/checkpoint/)

