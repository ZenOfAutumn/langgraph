# 🐍 Python 方式启动 LangGraph 服务器

基于官方教程: https://www.aidoczh.com/langgraph/tutorials/langgraph-platform/local-server/

## 📁 文件说明

本目录包含以下启动相关的文件：

### 1. `simple_start_server.py` ⭐ **推荐**
最简单的启动脚本，一键启动 LangGraph 服务器。

**特点**:
- ✅ 自动检查 Python 版本
- ✅ 自动安装依赖
- ✅ 自动创建示例应用
- ✅ 直接启动服务器

**使用**:
```bash
python simple_start_server.py
```

### 2. `start_langgraph_server.py`
功能更完整的启动脚本，支持更多自定义选项。

**特点**:
- ✅ 详细的检查和验证
- ✅ 支持自定义应用路径
- ✅ 显示环境变量配置指引
- ✅ 详细的错误提示

**使用**:
```bash
python start_langgraph_server.py
```

### 3. `test_langgraph_server.py`
测试已启动的 LangGraph 服务器的脚本。

**特点**:
- ✅ 同步 SDK 测试
- ✅ 异步 SDK 测试
- ✅ REST API 测试示例

**使用**:
```bash
# 确保服务器正在运行
python test_langgraph_server.py
```

### 4. `LANGGRAPH_STARTUP_GUIDE.md`
完整的启动指南文档，包含所有详细信息。

---

## ⚡ 快速开始 (30 秒)

```bash
# 一键启动
python simple_start_server.py
```

成功后会看到:
```
✓ API:     http://localhost:8123/
✓ 文档:    http://localhost:8123/docs
✓ Studio:  https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8123
```

---

## 🔍 详细步骤

### 方式 1: 使用自动化脚本 (推荐)

```bash
python simple_start_server.py
```

### 方式 2: 手动逐步执行

```bash
# 步骤 1: 安装 CLI
pip install -U "langgraph-cli[inmem]" python-dotenv

# 步骤 2: 创建应用
langgraph new my_app --template react-agent-python

# 步骤 3: 进入应用目录
cd my_app

# 步骤 4: 安装依赖
pip install -e .

# 步骤 5: 启动服务器
langgraph dev
```

---

## 🧪 测试服务器

### Python SDK 测试 (异步)

```python
from langgraph_sdk import get_client
import asyncio

async def test():
    client = get_client(url="http://localhost:8123")

    async for chunk in client.runs.stream(
        None,
        "agent",
        input={
            "messages": [{
                "role": "human",
                "content": "什么是 LangGraph？",
            }],
        },
        stream_mode="updates",
    ):
        print(f"事件: {chunk.event}")
        print(chunk.data)

asyncio.run(test())
```

### Python SDK 测试 (同步)

```python
from langgraph_sdk import get_sync_client

client = get_sync_client(url="http://localhost:8123")

for chunk in client.runs.stream(
    None,
    "agent",
    input={
        "messages": [{
            "role": "human",
            "content": "什么是 LangGraph？",
        }],
    },
    stream_mode="updates",
):
    print(f"事件: {chunk.event}")
    print(chunk.data)
```

### REST API 测试

```bash
curl -s --request POST \
  --url "http://localhost:8123/runs/stream" \
  --header 'Content-Type: application/json' \
  --data '{
    "assistant_id": "agent",
    "input": {
      "messages": [
        {
          "role": "human",
          "content": "什么是 LangGraph？"
        }
      ]
    },
    "stream_mode": "updates"
  }'
```

### JavaScript SDK 测试

```javascript
const { Client } = await import("@langchain/langgraph-sdk");

const client = new Client({ apiUrl: "http://localhost:8123" });

const streamResponse = client.runs.stream(
  null,
  "agent",
  {
    input: {
      "messages": [
        { "role": "user", "content": "什么是 LangGraph？" }
      ]
    },
    streamMode: "messages",
  }
);

for await (const chunk of streamResponse) {
  console.log(`事件: ${chunk.event}`);
  console.log(JSON.stringify(chunk.data));
}
```

---

## 🌐 访问 API

启动服务器后，可以访问以下内容：

| 功能 | URL |
|------|-----|
| **API 端点** | http://localhost:8123/ |
| **Swagger 文档** | http://localhost:8123/docs |
| **ReDoc 文档** | http://localhost:8123/redoc |
| **LangGraph Studio** | https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8123 |

---

## 📋 前置要求

- ✓ Python >= 3.11
- ✓ pip (Python 包管理器)
- ✓ (可选) Docker (如果使用 `langgraph up`)

## 🔐 环境变量配置

如果需要使用 AI 功能，需要配置以下 API 密钥：

创建 `.env` 文件 (在应用目录下):

```env
# LangSmith (可选，用于追踪)
LANGSMITH_API_KEY=lsv2_...

# LLM 提供商 (选一个或多个)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-...

# 工具 API (可选)
TAVILY_API_KEY=tvly-...
```

获取密钥:
- **LANGSMITH_API_KEY**: https://smith.langchain.com/settings
- **OPENAI_API_KEY**: https://openai.com/
- **ANTHROPIC_API_KEY**: https://console.anthropic.com/
- **TAVILY_API_KEY**: https://app.tavily.com/

---

## 🆘 故障排除

### 问题: 命令找不到 `langgraph`

**解决方案**:
```bash
pip install -U "langgraph-cli[inmem]"
```

### 问题: Python 版本过低

**解决方案**:
```bash
# 查看 Python 版本
python --version

# 需要 Python 3.11+，使用 pyenv 或 conda 升级
```

### 问题: 端口 8123 已被占用

**解决方案**:
```bash
# 查找占用端口的进程
lsof -i :8123

# 或者使用不同的端口
LANGGRAPH_PORT=8124 langgraph dev
```

### 问题: 模块导入错误

**解决方案**:
```bash
# 重新安装依赖
pip install --force-reinstall langgraph-sdk
```

---

## 📚 更多资源

- [📖 完整启动指南](./LANGGRAPH_STARTUP_GUIDE.md)
- [🌐 官方文档](https://www.aidoczh.com/langgraph/tutorials/langgraph-platform/local-server/)
- [📚 概念指南](https://www.aidoczh.com/langgraph/concepts/)
- [🛠️ 操作指南](https://www.aidoczh.com/langgraph/how-tos/)
- [🚀 部署到云端](https://www.aidoczh.com/langgraph/cloud/quick_start/)

---

## 💡 提示

### 1. 在后台运行服务器

```bash
# Linux/Mac
python simple_start_server.py &

# 或使用 nohup
nohup python simple_start_server.py > langgraph.log 2>&1 &
```

### 2. 监控日志

```bash
tail -f langgraph.log
```

### 3. 停止服务器

```bash
# 在前台运行时
Ctrl + C

# 在后台运行时
pkill -f "langgraph dev"
```

### 4. 开发模式 vs 生产模式

```bash
# 开发模式 (内存中，重启后数据丢失)
langgraph dev

# 生产模式 (需要 Docker，持久化存储)
langgraph up
```

---

**最后更新**: 2026-01-31
**作者**: LangGraph 文档
**版本**: 1.0

