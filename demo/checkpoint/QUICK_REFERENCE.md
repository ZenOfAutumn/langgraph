# 快速参考指南

## 环境准备

### 1. 激活虚拟环境
```bash
cd /Users/wuliang/Workspace/github/langgraph
source venv/bin/activate
```

### 2. 安装依赖（仅需一次）
```bash
# 如果还未安装
./venv/bin/python -m pip install -e ./libs/langgraph
./venv/bin/python -m pip install -e ./libs/checkpoint-sqlite
```

---

## 运行演示

### 完整步骤
```bash
cd /Users/wuliang/Workspace/github/langgraph/demo/checkpoint

# Step 1: 初始化数据库（首次运行或需要重置时）
./../../venv/bin/python init_sqlite_db.py

# Step 2: 运行演示脚本
./../../venv/bin/python simple_checkpoint_demo.py
```

### 使用虚拟环境的完整命令
```bash
/Users/wuliang/Workspace/github/langgraph/venv/bin/python init_sqlite_db.py
/Users/wuliang/Workspace/github/langgraph/venv/bin/python simple_checkpoint_demo.py
```

---

## 快速检查

### 验证安装
```bash
/Users/wuliang/Workspace/github/langgraph/venv/bin/python -c \
  "from langgraph.checkpoint.sqlite import SqliteSaver; \
   from langgraph.graph import StateGraph, START, END; \
   print('✓ 环境配置正确')"
```

### 查看数据库内容
```bash
# 查看 checkpoint 记录
sqlite3 /tmp/langgraph_demo/order_checkpoints.db \
  "SELECT thread_id, checkpoint_id FROM checkpoints;"

# 查看表结构
sqlite3 /tmp/langgraph_demo/order_checkpoints.db ".schema"
```

### 清理数据库
```bash
rm -rf /tmp/langgraph_demo
```

---

## 文件说明

| 文件 | 说明 |
|------|------|
| `simple_checkpoint_demo.py` | 核心演示脚本（已修复） |
| `init_sqlite_db.py` | 数据库初始化脚本（已更新） |
| `EXECUTION_RESULT.md` | 最新执行结果记录 |
| `FIXES_APPLIED.md` | 修复过程详细记录 |
| `checkpoint_usage_guide.md` | LangGraph Checkpoint 使用指南 |
| `README.md` | 项目概述 |

---

## 常见问题

### Q: 数据库错误 "no such column"
**A**: 删除旧数据库并重新初始化
```bash
rm -rf /tmp/langgraph_demo
python init_sqlite_db.py
```

### Q: 模块导入错误
**A**: 确保在虚拟环境中运行，并安装了所有依赖
```bash
source /Users/wuliang/Workspace/github/langgraph/venv/bin/activate
pip install -e ./libs/langgraph
pip install -e ./libs/checkpoint-sqlite
```

### Q: 如何验证 checkpoint 是否正确保存？
**A**:
```bash
# 第一次运行（创建 checkpoint）
python simple_checkpoint_demo.py

# 查询数据库
sqlite3 /tmp/langgraph_demo/order_checkpoints.db \
  "SELECT COUNT(*) as total_checkpoints FROM checkpoints;"
```

---

## 演示输出示例

成功运行时会显示：
```
======================================================================
🚀 LangGraph Checkpoint 完整演示
======================================================================

[... 各个演示场景的输出 ...]

======================================================================
✨ 演示完成!
======================================================================
```

---

## 关键概念回顾

- **Checkpoint**: 图执行过程中的状态快照
- **thread_id**: 流程实例的唯一标识
- **SqliteSaver**: 使用 SQLite 存储 checkpoint
- **WAL 模式**: 提高并发性能的数据库模式

---

## 获取帮助

查看详细文档：
- `FIXES_APPLIED.md` - 完整的修复过程说明
- `EXECUTION_RESULT.md` - 详细的执行结果分析
- `checkpoint_usage_guide.md` - LangGraph Checkpoint 深入指南

---

*最后更新: 2026-02-01*

