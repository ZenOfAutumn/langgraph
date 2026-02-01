# SQLite 数据库初始化信息

## ✅ 初始化状态

SQLite 数据库已成功初始化！

### 📊 数据库位置
```
/tmp/langgraph_demo/order_checkpoints.db
```

### 💾 数据库大小
- 20 KB

### 🗂️ SQLite 版本
- 3.41.2

## 📋 表结构详情

### checkpoints 表

| 列名 | 类型 | 说明 | 约束 |
|------|------|------|------|
| `thread_id` | TEXT | 流程线程ID（分片键） | PRIMARY KEY, NOT NULL |
| `checkpoint_id` | TEXT | 检查点唯一标识 | PRIMARY KEY, NOT NULL |
| `parent_checkpoint_id` | TEXT | 父检查点ID | - |
| `values` | BLOB | 存储的状态数据 | NOT NULL |
| `metadata` | BLOB | 检查点元数据 | - |
| `created_at` | TIMESTAMP | 创建时间 | DEFAULT CURRENT_TIMESTAMP |

### 索引

```sql
CREATE INDEX idx_checkpoints_thread_id ON checkpoints(thread_id);
CREATE INDEX idx_checkpoints_created_at ON checkpoints(created_at);
```

## 🔧 使用方式

### 1. 在 simple_checkpoint_demo.py 中使用

脚本会自动连接到这个数据库：

```python
from langgraph.checkpoint.sqlite import SqliteSaver

checkpointer = SqliteSaver.from_conn_string(
    "sqlite:////tmp/langgraph_demo/order_checkpoints.db"
)
```

### 2. 直接创建连接

```python
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

conn = sqlite3.connect('/tmp/langgraph_demo/order_checkpoints.db')
checkpointer = SqliteSaver(conn)
graph.compile(checkpointer=checkpointer)
```

### 3. 命令行查询

```bash
# 查看所有表
sqlite3 /tmp/langgraph_demo/order_checkpoints.db ".tables"

# 查询检查点
sqlite3 /tmp/langgraph_demo/order_checkpoints.db "SELECT * FROM checkpoints;"

# 查询特定线程的检查点
sqlite3 /tmp/langgraph_demo/order_checkpoints.db \
  "SELECT thread_id, checkpoint_id, created_at FROM checkpoints WHERE thread_id='ORDER-001';"
```

## 📊 功能特性

### ✅ 已启用的功能

- ✓ 完整的 checkpoint 保存
- ✓ 多线程隔离（通过 thread_id）
- ✓ 检查点恢复
- ✓ 元数据存储
- ✓ 时间戳追踪
- ✓ 查询优化（索引）

### 🎯 支持的操作

1. **保存状态**
   - 自动保存每个节点执行后的状态
   - 支持完整的状态数据序列化

2. **恢复流程**
   - 从特定 checkpoint 恢复
   - 支持增量恢复

3. **并发处理**
   - 多个线程独立存储
   - 线程间完全隔离

4. **查询和分析**
   - 按 thread_id 查询
   - 按时间戳查询
   - 支持复杂的 SQL 查询

## 🚀 现在可以做什么

### 1. 运行演示脚本

```bash
cd /Users/wuliang/Workspace/github/langgraph/demo/checkpoint
python simple_checkpoint_demo.py
```

### 2. 查看保存的数据

演示运行后，可以查看保存的 checkpoint：

```bash
sqlite3 /tmp/langgraph_demo/order_checkpoints.db
SELECT thread_id, checkpoint_id, created_at FROM checkpoints ORDER BY created_at DESC;
```

### 3. 扩展应用

可以基于这个数据库实现：
- 流程状态监控
- Checkpoint 恢复测试
- 性能分析
- 审计日志

## ⚙️ 维护

### 清理数据库

```bash
# 删除所有 checkpoint
sqlite3 /tmp/langgraph_demo/order_checkpoints.db "DELETE FROM checkpoints;"

# 删除整个数据库
rm /tmp/langgraph_demo/order_checkpoints.db
```

### 备份数据库

```bash
# 导出为 SQL
sqlite3 /tmp/langgraph_demo/order_checkpoints.db ".dump" > checkpoint_backup.sql

# 复制文件
cp /tmp/langgraph_demo/order_checkpoints.db ./order_checkpoints_backup.db
```

### 检查数据库完整性

```bash
sqlite3 /tmp/langgraph_demo/order_checkpoints.db "PRAGMA integrity_check;"
```

## 📈 性能指标

- **数据库大小**: 20 KB (初始)
- **主键查询**: O(log n) 通过索引
- **范围查询**: 支持通过 created_at 索引
- **并发支持**: SQLite WAL 模式（如需更新）

## 🔗 相关文件

- 演示脚本: `simple_checkpoint_demo.py`
- 使用指南: `checkpoint_usage_guide.md`
- 快速开始: `QUICK_START.md`
- 执行日志: `EXECUTION_LOG.md`

## ✨ 初始化完成

数据库已准备就绪，可以开始使用 LangGraph 的 checkpoint 功能了！

---

*数据库初始化于: 2026-02-01*

