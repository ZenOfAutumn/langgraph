# 🚀 LangGraph 服务器启动指南 (Python 方式)

基于官方文档: https://www.aidoczh.com/langgraph/tutorials/langgraph-platform/local-server/

## 📋 前置要求

- **Python >= 3.11**
- **LangGraph CLI >= 0.1.58**

## ⚡ 快速启动（5 分钟）

### 步骤 1️⃣: 安装 LangGraph CLI

```bash
pip install -U "langgraph-cli[inmem]" python-dotenv
```

### 步骤 2️⃣: 创建 LangGraph 应用

```bash
# 使用 react-agent-python 模板
langgraph new my_langgraph_app --template react-agent-python

# 或者使用交互式菜单选择其他模板
langgraph new my_langgraph_app
```

### 步骤 3️⃣: 安装依赖

```bash
cd my_langgraph_app
pip install -e .
```

### 步骤 4️⃣: 配置环境变量

```bash
# 复制示例文件
cp .env.example .env

# 编辑 .env 文件，填写必要的 API 密钥
```

需要设置的 API 密钥：
- **LANGSMITH_API_KEY**: 从 [LangSmith 设置页面](https://smith.langchain.com/settings) 获取
- **ANTHROPIC_API_KEY**: 从 [Anthropic 控制台](https://console.anthropic.com/) 获取
- **OPENAI_API_KEY**: 从 [OpenAI 官网](https://openai.com/) 获取
- **TAVILY_API_KEY**: 从 [Tavily 网站](https://app.tavily.com/) 获取

### 步骤 5️⃣: 启动服务器

```bash
langgraph dev
```

✅ 如果成功，你会看到：

```
准备好了！

* API: http://localhost:8123/
* 文档: http://localhost:8123/docs
* LangGraph Studio Web UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8123
```

---

## 🔗 测试 API

### 使用 Python SDK (异步)

```python
from langgraph_sdk import get_client

client = get_client(url="http://localhost:8123")

async for chunk in client.runs.stream(
    None,  # 无线程运行
    "agent",  # 助手名称
    input={
        "messages": [{
            "role": "human",
            "content": "什么是 LangGraph？",
        }],
    },
    stream_mode="updates",
):
    print(f"接收新事件类型: {chunk.event}...")
    print(chunk.data)
    print("\n\n")
```

### 使用 Python SDK (同步)

```python
from langgraph_sdk import get_sync_client

client = get_sync_client(url="http://localhost:8123")

for chunk in client.runs.stream(
    None,  # 无线程运行
    "agent",  # 助手名称
    input={
        "messages": [{
            "role": "human",
            "content": "什么是 LangGraph？",
        }],
    },
    stream_mode="updates",
):
    print(f"接收新事件类型: {chunk.event}...")
    print(chunk.data)
    print("\n\n")
```

### 使用 REST API (curl)

```bash
curl -s --request POST \
  --url "http://localhost:8123/runs/stream" \
  --header 'Content-Type: application/json' \
  --data "{
    \"assistant_id\": \"agent\",
    \"input\": {
      \"messages\": [
        {
          \"role\": \"human\",
          \"content\": \"什么是 LangGraph？\"
        }
      ]
    },
    \"stream_mode\": \"updates\"
  }"
```

### 使用 Javascript SDK

```javascript
const { Client } = await import("@langchain/langgraph-sdk");

const client = new Client({ apiUrl: "http://localhost:8123" });

const streamResponse = client.runs.stream(
  null, // 无线程运行
  "agent", // 助手 ID
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
  console.log(`接收新事件类型: ${chunk.event}...`);
  console.log(JSON.stringify(chunk.data));
  console.log("\n\n");
}
```

---

## 📚 访问 API 文档

启动服务器后，可以访问以下资源：

| 资源 | URL |
|------|-----|
| API 端点 | http://localhost:8123/ |
| Swagger 文档 | http://localhost:8123/docs |
| ReDoc 文档 | http://localhost:8123/redoc |
| LangGraph Studio | https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8123 |

---

## 🔧 高级选项

### 使用持久化存储 (PostgreSQL/SQLite)

如果想要生产级别的持久存储，使用 `langgraph up` 而不是 `langgraph dev`：

```bash
# 需要先安装 Docker
langgraph up
```

### 更改服务器端口

```bash
# 默认端口是 8123，可以通过环境变量修改
LANGGRAPH_PORT=8000 langgraph dev
```

### 调试模式

```bash
# 启用详细日志
DEBUG=1 langgraph dev
```

---

## 🆘 常见问题

### Q: 服务器无法启动？
A: 检查以下几点：
- Python 版本 >= 3.11
- LangGraph CLI 已正确安装
- 端口 8123 未被占用
- `.env` 文件已正确配置

### Q: 可以不设置 API 密钥吗？
A: 部分功能不需要 API 密钥，但为了完整功能体验，建议配置所有密钥。

### Q: 内存模式有数据持久化吗？
A: 不，`langgraph dev` 在内存模式下运行，重启后数据会丢失。使用 `langgraph up` 以获得持久存储。

### Q: Safari 不支持 LangGraph Studio？
A: 正确，目前 LangGraph Studio Web 在本地运行时不支持 Safari，请使用 Chrome 或 Firefox。

---

## 📖 自动化启动脚本

项目中提供了两个自动化脚本：

### 自动启动脚本
```bash
python start_langgraph_server.py
```

这个脚本会自动完成以下操作：
1. 检查 Python 版本和依赖
2. 创建示例应用
3. 配置环境变量
4. 安装依赖
5. 启动服务器

### 测试脚本
```bash
python test_langgraph_server.py
```

这个脚本会测试：
1. 同步 Python SDK 连接
2. 异步 Python SDK 连接
3. REST API 调用示例

---

## 🚀 后续步骤

1. **在 LangGraph Studio 中测试**: 访问 Web UI 测试你的应用
2. **构建自定义工具**: 查看官方文档学习如何添加自定义工具
3. **部署到云端**: 参考 [LangGraph Cloud 快速开始](https://www.aidoczh.com/langgraph/cloud/quick_start/)
4. **学习更多**: 查看 [概念指南](https://www.aidoczh.com/langgraph/concepts/) 和 [操作指南](https://www.aidoczh.com/langgraph/how-tos/)

---

## 📚 官方资源

- [官方文档](https://www.aidoczh.com/langgraph/tutorials/langgraph-platform/local-server/)
- [Python SDK 参考](https://www.aidoczh.com/langgraph/cloud/reference/sdk/python_sdk_ref/)
- [JS/TS SDK 参考](https://www.aidoczh.com/langgraph/tutorials/cloud/reference/sdk/js_ts_sdk_ref.md)
- [LangGraph 服务器 API 参考](https://www.aidoczh.com/langgraph/cloud/reference/api/api_ref.html)

---

**最后更新**: 2026-01-31
**文档版本**: 1.0

