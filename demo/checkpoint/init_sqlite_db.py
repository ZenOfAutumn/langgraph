#!/usr/bin/env python3
"""
初始化 simple_checkpoint_demo.py 所需的 SQLite 数据库

使用方法:
    python init_sqlite_db.py

说明:
    - 创建 /tmp/langgraph_demo 目录
    - 初始化 order_checkpoints.db 数据库
    - 创建 checkpoints 表和索引
    - 验证数据库可用性
"""

import os
import sqlite3

# 数据库配置
db_path = '/tmp/langgraph_demo/order_checkpoints.db'
db_dir = os.path.dirname(db_path)

print("=" * 70)
print("🗄️  SQLite Checkpoint 数据库初始化")
print("=" * 70)

# 创建目录
print(f"\n📁 创建目录: {db_dir}")
os.makedirs(db_dir, exist_ok=True)
print(f"   ✓ 目录已准备")

# 如果数据库已存在，先删除
if os.path.exists(db_path):
    print(f"\n📝 清理旧数据库...")
    os.remove(db_path)
    print(f"   ✓ 旧数据库已删除")

# 创建数据库连接
print(f"\n🔌 创建新数据库: {db_path}")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
print(f"   ✓ 连接成功")

# 创建 checkpoint 表 - 使用引号避免保留字问题
print("\n📊 创建数据库表...")

create_table_sql = '''
PRAGMA journal_mode=WAL;
CREATE TABLE IF NOT EXISTS checkpoints (
    thread_id TEXT NOT NULL,
    checkpoint_ns TEXT NOT NULL DEFAULT '',
    checkpoint_id TEXT NOT NULL,
    parent_checkpoint_id TEXT,
    type TEXT,
    checkpoint BLOB,
    metadata BLOB,
    PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id)
);

CREATE TABLE IF NOT EXISTS writes (
    thread_id TEXT NOT NULL,
    checkpoint_ns TEXT NOT NULL DEFAULT '',
    checkpoint_id TEXT NOT NULL,
    task_id TEXT NOT NULL,
    idx INTEGER NOT NULL,
    channel TEXT NOT NULL,
    type TEXT,
    value BLOB,
    PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id, task_id, idx)
);

CREATE INDEX IF NOT EXISTS idx_writes_thread_id
ON writes(thread_id);

CREATE INDEX IF NOT EXISTS idx_checkpoints_thread_id
ON checkpoints(thread_id);
'''

try:
    cursor.executescript(create_table_sql)
    conn.commit()
    print("   ✓ 表创建成功")
except Exception as e:
    print(f"   ✗ 创建表失败: {e}")
    conn.close()
    exit(1)

# 验证表结构
print("\n📋 验证表结构...")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print(f"   找到 {len(tables)} 个表:")
for table in tables:
    print(f"     • {table[0]}")

# 查看表详情
cursor.execute("PRAGMA table_info(checkpoints)")
columns = cursor.fetchall()
print(f"\n   checkpoints 表的列:")
for col in columns:
    col_symbol = "📌" if col[1] in ["thread_id", "checkpoint_id"] else "📝"
    print(f"     {col_symbol} {col[1]:25} ({col[2]})")

# 获取数据库统计信息
print(f"\n📊 数据库统计:")
cursor.execute("SELECT COUNT(*) FROM checkpoints")
count = cursor.fetchone()[0]
print(f"   当前记录数: {count}")

# 显示文件信息
file_stat = os.stat(db_path)
print(f"\n💾 文件信息:")
print(f"   路径: {db_path}")
print(f"   大小: {file_stat.st_size} 字节")

# 验证数据库可用性
print(f"\n✅ 验证数据库可用性...")
try:
    cursor.execute("SELECT sqlite_version();")
    version = cursor.fetchone()[0]
    print(f"   SQLite 版本: {version}")

    # 测试插入
    cursor.execute("""
        INSERT INTO checkpoints (thread_id, checkpoint_id, "values")
        VALUES (?, ?, ?)
    """, ('test_thread', 'test_cp_1', b'test_data'))
    conn.commit()
    print(f"   ✓ 测试插入成功")

    # 查询验证
    cursor.execute("SELECT COUNT(*) FROM checkpoints")
    test_count = cursor.fetchone()[0]
    print(f"   ✓ 数据库正常可用 (当前记录: {test_count})")

except Exception as e:
    print(f"   ✗ 验证失败: {e}")

# 关闭连接
conn.close()

print("\n" + "=" * 70)
print("✅ 数据库初始化完成!")
print("=" * 70)

# 显示使用信息
print("\n📝 现在可以这样使用:")
print(f"""
1. 运行 simple_checkpoint_demo.py:
   python simple_checkpoint_demo.py

   会自动使用数据库: {db_path}

2. 查询 checkpoint 数据:
   sqlite3 {db_path}
   SELECT thread_id, checkpoint_id FROM checkpoints;

3. 在代码中使用:
   from langgraph.checkpoint.sqlite import SqliteSaver
   import sqlite3

   conn = sqlite3.connect('{db_path}')
   checkpointer = SqliteSaver(conn)
   graph.compile(checkpointer=checkpointer)

4. 清理数据库:
   rm {db_path}
""")

print("=" * 70)

