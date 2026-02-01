# 📚 LangGraph 服务器启动总结

根据官方文档创建的 Python 方式启动指南和工具集合。

## 🎯 三种启动方式

### 方式 1️⃣: 一键自动启动 ⭐ **最简单**

```bash
python simple_start_server.py
```

✅ 优点:
- 最少的输入
- 自动化所有步骤
- 适合快速启动

❌ 缺点:
- 自定义选项少

---

### 方式 2️⃣: 完整自动启动脚本

```bash
python start_langgraph_server.py
```

✅ 优点:
- 详细的检查和验证
- 完整的错误提示
- 支持更多定制

❌ 缺点:
- 过程较长

---

### 方式 3️⃣: 手动逐步启动 ⭐ **最灵活**

```bash
# 安装 CLI
pip install -U "langgraph-cli[inmem]" python-dotenv

# 创建应用
langgraph new my_app --template react-agent-python

# 进入应用目录
cd my_app

# 安装依赖
pip install -e .

# 启动服务器
langgraph dev
```

✅ 优点:
- 完全控制每一步
- 理解每个步骤的含义
- 适合学习和调试

❌ 缺点:
- 需要手动执行多个命令

---

## 📂 创建的文件

| 文件 | 用途 | 推荐度 |
|------|------|--------|
| `simple_start_server.py` | 一键启动脚本 | ⭐⭐⭐⭐⭐ |
| `start_langgraph_server.py` | 功能完整的启动脚本 | ⭐⭐⭐⭐ |
| `test_langgraph_server.py` | 测试服务器脚本 | ⭐⭐⭐ |
| `LANGGRAPH_STARTUP_GUIDE.md` | 完整启动指南 | ⭐⭐⭐⭐⭐ |
| `PYTHON_LANGGRAPH_STARTUP_README.md` | 快速参考 | ⭐⭐⭐⭐⭐ |

---

## 🚀 快速启动 (5 秒)

```bash
python simple_start_server.py
```

等待看到:
```
✓ API:     http://localhost:8123/
✓ 文档:    http://localhost:8123/docs
✓ Studio:  https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8123
```

---

## 🔗 API 访问方式

### 1. Web UI (推荐)
- **LangGraph Studio**: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8123
- **Swagger Docs**: http://localhost:8123/docs
- **ReDoc Docs**: http://localhost:8123/redoc

### 2. Python SDK (异步)

```python
from langgraph_sdk import get_client

client = get_client(url="http://localhost:8123")

async for chunk in client.runs.stream(
    None,
    "agent",
    input={"messages": [{"role": "human", "content": "Hello!"}]},
    stream_mode="updates",
):
    print(chunk.event)
    print(chunk.data)
```

### 3. Python SDK (同步)

```python
from langgraph_sdk import get_sync_client

client = get_sync_client(url="http://localhost:8123")

for chunk in client.runs.stream(
    None,
    "agent",
    input={"messages": [{"role": "human", "content": "Hello!"}]},
    stream_mode="updates",
):
    print(chunk.event)
```

### 4. REST API

```bash
curl -X POST "http://localhost:8123/runs/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "assistant_id": "agent",
    "input": {"messages": [{"role": "human", "content": "Hello!"}]},
    "stream_mode": "updates"
  }'
```

### 5. JavaScript SDK

```javascript
const { Client } = await import("@langchain/langgraph-sdk");

const client = new Client({ apiUrl: "http://localhost:8123" });

const streamResponse = client.runs.stream(
  null,
  "agent",
  {
    input: {"messages": [{"role": "user", "content": "Hello!"}]},
    streamMode: "messages",
  }
);

for await (const chunk of streamResponse) {
  console.log(chunk.event);
  console.log(chunk.data);
}
```

---

## ✅ 启动检查清单

### 启动前
- [ ] Python 版本 >= 3.11 (`python --version`)
- [ ] pip 已安装 (`pip --version`)
- [ ] 网络连接正常
- [ ] 端口 8123 未被占用 (`lsof -i :8123`)

### 启动后
- [ ] 看到 "准备好了!" 信息
- [ ] API 可访问: http://localhost:8123/
- [ ] 文档可访问: http://localhost:8123/docs
- [ ] 可以在 Studio 中看到应用

### 测试
- [ ] 能够发送消息到 API
- [ ] 能够接收响应
- [ ] Studio 中可以看到对话历史

---

## 🆘 常见问题

**Q: 端口 8123 被占用了怎么办?**
```bash
# 方式 1: 使用不同端口
LANGGRAPH_PORT=8124 langgraph dev

# 方式 2: 关闭占用端口的进程
lsof -i :8123
kill -9 <PID>
```

**Q: 没有 API 密钥可以运行吗?**
```
部分基础功能可以运行，但完整功能需要配置:
- OPENAI_API_KEY (或 ANTHROPIC_API_KEY)
- TAVILY_API_KEY (用于搜索)
- LANGSMITH_API_KEY (用于追踪)
```

**Q: Safari 无法打开 Studio?**
```
这是已知问题，使用 Chrome 或 Firefox 替代
```

**Q: 如何在后台运行?**
```bash
# Linux/Mac
nohup python simple_start_server.py > langgraph.log 2>&1 &

# 查看日志
tail -f langgraph.log

# 停止
pkill -f "langgraph dev"
```

**Q: 数据会保存吗?**
```
不会。langgraph dev 在内存中运行。
要持久化存储，使用:
langgraph up (需要 Docker)
```

---

## 📚 文档链接

- [📖 官方启动指南](./LANGGRAPH_STARTUP_GUIDE.md)
- [📖 快速参考](./PYTHON_LANGGRAPH_STARTUP_README.md)
- [🌐 官方文档](https://www.aidoczh.com/langgraph/tutorials/langgraph-platform/local-server/)
- [📚 概念指南](https://www.aidoczh.com/langgraph/concepts/)
- [🛠️ 操作指南](https://www.aidoczh.com/langgraph/how-tos/)
- [🚀 云部署](https://www.aidoczh.com/langgraph/cloud/quick_start/)

---

## 📦 系统要求

| 组件 | 要求 | 可选 |
|------|------|------|
| Python | >= 3.11 | ❌ |
| pip | >= 20.0 | ❌ |
| Docker | 任意版本 | ✅ |
| Git | 任意版本 | ✅ |

---

## 💡 最佳实践

### 开发环境
```bash
# 使用虚拟环境隔离依赖
python -m venv venv
source venv/bin/activate  # Mac/Linux
# 或 venv\Scripts\activate  # Windows

# 安装并启动
python simple_start_server.py
```

### 生产环境
```bash
# 使用持久化存储
langgraph up

# 使用 Docker Compose 或 Kubernetes 部署
```

### 调试
```bash
# 启用详细日志
DEBUG=1 langgraph dev

# 使用 Python 调试器
python -m pdb simple_start_server.py
```

---

## 🎓 学习路径

1. **快速开始** (5 分钟)
   - 运行 `python simple_start_server.py`
   - 访问 Studio: https://smith.langchain.com/studio/

2. **理解基础** (15 分钟)
   - 阅读 [LANGGRAPH_STARTUP_GUIDE.md](./LANGGRAPH_STARTUP_GUIDE.md)
   - 测试各种 API 访问方式

3. **构建应用** (1 小时)
   - 学习官方教程
   - 添加自定义工具
   - 实现业务逻辑

4. **部署到生产** (1 小时)
   - 配置持久化存储
   - 部署到云端
   - 设置监控和日志

---

**创建日期**: 2026-01-31
**最后更新**: 2026-01-31
**版本**: 1.0

