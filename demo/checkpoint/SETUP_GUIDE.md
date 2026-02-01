# 设置和使用指南

## 📂 文件结构

```
/Users/wuliang/Workspace/github/langgraph/demo/checkpoint/
├── simple_checkpoint_demo.py          # 主演示脚本
├── checkpoint_example.py              # 完整示例
├── init_sqlite_db.py                  # ✨ 数据库初始化脚本
├── README.md                          # 项目说明
├── QUICK_START.md                     # 快速开始
├── INDEX.md                           # 文件索引
├── checkpoint_usage_guide.md          # 使用指南
├── EXECUTION_LOG.md                   # 执行日志
└── DB_INIT_INFO.md                    # 数据库信息
```

## 🚀 快速设置步骤

### 第一步：初始化 SQLite 数据库

```bash
cd /Users/wuliang/Workspace/github/langgraph/demo/checkpoint
python init_sqlite_db.py
```

**输出应该显示：**
```
🗄️  SQLite Checkpoint 数据库初始化
✓ 表创建成功
✓ 数据库正常可用
✅ 数据库初始化完成!
```

### 第二步：运行演示脚本

```bash
python simple_checkpoint_demo.py
```

**演示内容：**
- 🛒 订单处理工作流
- 🔄 Checkpoint 恢复演示
- ⚡ 并行处理多个订单

## 📝 init_sqlite_db.py 脚本说明

### 功能

该脚本自动执行以下操作：

1. **创建目录** - 在 `/tmp/langgraph_demo/` 下创建存储目录
2. **初始化数据库** - 创建 `order_checkpoints.db` SQLite 数据库
3. **创建表** - 建立 `checkpoints` 表及其索引
4. **验证功能** - 测试数据库的读写能力
5. **显示统计** - 输出数据库的详细信息

### 数据库表结构

| 列名 | 类型 | 说明 |
|------|------|------|
| thread_id | TEXT | 流程线程标识 |
| checkpoint_id | TEXT | 检查点ID |
| parent_checkpoint_id | TEXT | 父检查点 |
| values | BLOB | 状态数据 |
| metadata | BLOB | 元数据 |
| created_at | TIMESTAMP | 创建时间 |

### 创建的索引

- `idx_checkpoints_thread_id` - 快速查询特定线程
- `idx_checkpoints_created_at` - 按时间范围查询

## 💾 数据库位置

```
/tmp/langgraph_demo/order_checkpoints.db
```

### 查询数据库

```bash
# 连接到数据库
sqlite3 /tmp/langgraph_demo/order_checkpoints.db

# 查看所有记录
SELECT * FROM checkpoints;

# 按线程查询
SELECT thread_id, checkpoint_id FROM checkpoints WHERE thread_id='ORDER-001';

# 查看最新的检查点
SELECT * FROM checkpoints ORDER BY created_at DESC LIMIT 5;
```

## 📊 使用流程

```
┌─────────────────────┐
│ 运行 init_sqlite_db.py│  初始化数据库
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────┐
│ 运行 simple_checkpoint_demo.py│  演示 checkpoint 功能
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│ 查询 SQLite 数据库        │  验证保存的状态
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────┐
│ 分析 checkpoint 数据 │  学习工作原理
└─────────────────────┘
```

## 🔧 常见操作

### 重新初始化数据库

```bash
python init_sqlite_db.py
```

脚本会自动删除旧数据库并创建新的。

### 备份数据库

```bash
# 导出为 SQL
sqlite3 /tmp/langgraph_demo/order_checkpoints.db ".dump" > backup.sql

# 复制文件
cp /tmp/langgraph_demo/order_checkpoints.db ./order_checkpoints_backup.db
```

### 清理数据库

```bash
# 删除所有记录
sqlite3 /tmp/langgraph_demo/order_checkpoints.db "DELETE FROM checkpoints;"

# 删除数据库文件
rm /tmp/langgraph_demo/order_checkpoints.db
```

## 📖 文档导航

| 文档 | 用途 |
|------|------|
| **README.md** | 项目完整说明 |
| **QUICK_START.md** | 5分钟快速入门 |
| **SETUP_GUIDE.md** | 本文件 - 设置指南 |
| **checkpoint_usage_guide.md** | 详细的概念讲解 |
| **DB_INIT_INFO.md** | 数据库详细信息 |
| **EXECUTION_LOG.md** | 演示执行日志 |

## ✅ 验证安装

运行以下命令验证一切正常：

```bash
# 1. 检查脚本文件
ls -la init_sqlite_db.py

# 2. 运行初始化
python init_sqlite_db.py

# 3. 验证数据库
sqlite3 /tmp/langgraph_demo/order_checkpoints.db ".tables"

# 4. 运行演示
python simple_checkpoint_demo.py
```

所有命令都应该成功执行。

## 🎯 下一步

1. ✅ 初始化数据库 - `python init_sqlite_db.py`
2. ✅ 查看文档 - 阅读 `QUICK_START.md`
3. ✅ 运行演示 - `python simple_checkpoint_demo.py`
4. ✅ 查询数据 - `sqlite3 ...`
5. ✅ 研究代码 - 阅读源代码注释

---

**准备好了吗？开始吧！🚀**

