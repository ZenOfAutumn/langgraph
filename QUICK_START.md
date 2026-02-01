# ⚡ 快速开始

## 🚀 一键启动 LangGraph 服务器

```bash
python simple_start_server.py
```

## ✅ 修复内容

### 已解决的问题

1. **网络超时错误**: 改进了错误处理，支持离线创建应用
2. **依赖安装失败**: 允许脚本在依赖安装失败时继续执行
3. **缺少错误提示**: 添加了详细的错误消息和解决建议
4. **文件导入问题**: 移除了未使用的 `os` 导入

### 代码改进

#### 改进 1: 增强的错误处理

```python
# 之前
run_command([...])  # 会在任何错误时直接退出

# 之后
if not run_command([...], show_output=False, exit_on_error=False):
    print("⚠️  操作失败，但继续...")
```

#### 改进 2: 新增 `exit_on_error` 参数

```python
def run_command(cmd, cwd=None, show_output=True, exit_on_error=True):
    """
    exit_on_error=False: 命令失败时返回 False 但不退出
    exit_on_error=True: 命令失败时返回 False 并退出（默认）
    """
```

#### 改进 3: 更好的用户提示

```python
print("   ❌ 应用创建失败")
print("   💡 确保网络连接正常，或手动运行:")
print(f"      langgraph new {app_dir} --template react-agent-python")
```

## 📋 运行流程

```
1️⃣  检查 Python 版本 (>= 3.11)
    ✓ 必须满足

2️⃣  安装 LangGraph CLI
    ⚠️  失败时继续（可能已安装）

3️⃣  创建 LangGraph 应用
    ✗ 失败时退出（必须成功）

4️⃣  安装应用依赖
    ⚠️  失败时继续尝试启动

5️⃣  启动服务器
    运行 langgraph dev
```

## 🔧 手动步骤 (如果脚本失败)

```bash
# 步骤 1: 安装 CLI
pip install -U "langgraph-cli[inmem]" python-dotenv

# 步骤 2: 创建应用
langgraph new my_app --template react-agent-python

# 步骤 3: 进入目录
cd my_app

# 步骤 4: 安装依赖
pip install -e .

# 步骤 5: 启动服务器
langgraph dev
```

## 🌐 成功启动的标志

当看到以下输出表示启动成功:

```
准备好了！

* API: http://localhost:8123/
* 文档: http://localhost:8123/docs
* LangGraph Studio Web UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8123
```

## 🆘 常见错误及解决方案

### 错误 1: `langgraph: command not found`
```bash
# 解决方案
pip install -U "langgraph-cli[inmem]"
```

### 错误 2: `URLError: Operation timed out`
```bash
# 解决方案: 检查网络连接，或离线创建应用
# 直接手动执行步骤（见上面的手动步骤）
```

### 错误 3: `No module named 'langgraph_sdk'`
```bash
# 解决方案
pip install langgraph-sdk
```

### 错误 4: `Python version must be >= 3.11`
```bash
# 解决方案: 升级 Python
# 使用 pyenv, conda, 或其他工具升级到 Python 3.11+
python --version  # 检查当前版本
```

## 📚 相关文档

- [完整启动指南](./LANGGRAPH_STARTUP_GUIDE.md)
- [快速参考](./PYTHON_LANGGRAPH_STARTUP_README.md)
- [总结文档](./STARTUP_SUMMARY.md)

## 💡 提示

- 首次运行会下载较大的依赖，请耐心等待
- 确保有足够的磁盘空间 (至少 2GB)
- 可以在后台运行: `nohup python simple_start_server.py > langgraph.log 2>&1 &`

---

**最后更新**: 2026-01-31

