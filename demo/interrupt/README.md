# Human-in-the-Loop Agent 示例

这是一个展示 LangGraph 中 Human-in-the-Loop（人工干预）机制的完整示例。

## 📋 项目说明

### 场景：订单处理系统

一个 Agent 处理客户订单，根据订单金额自动决定是否需要人工审批：
- **小额订单** (≤ ¥500): 自动批准
- **大额订单** (> ¥500): 暂停并等待人工审批

## 🏗️ 文件说明

| 文件 | 说明 |
|------|------|
| `human_in_the_loop_agent.py` | 核心 Agent 实现 |
| `run_demo.py` | 自动化演示（无需交互） |
| `interactive_demo.py` | 交互式演示（支持用户输入） |
| `README.md` | 本文件 |

## 🚀 快速开始

### 运行自动化演示

```bash
cd /Users/wuliang/Workspace/github/langgraph/demo/interrupt
/Users/wuliang/Workspace/github/langgraph/venv/bin/python run_demo.py
```

**特点**:
- ✅ 无需用户交互
- ✅ 自动演示 3 个场景
- ✅ 显示完整的处理流程

### 运行交互式演示

```bash
cd /Users/wuliang/Workspace/github/langgraph/demo/interrupt
/Users/wuliang/Workspace/github/langgraph/venv/bin/python interactive_demo.py
```

**特点**:
- 🎯 支持自定义订单信息
- 👤 等待真实用户输入
- 💡 完整的菜单系统

## 🏗️ Agent 架构

### 流程图

```
START
  ↓
[analyze] → 分析订单信息
  ↓
[check_approval] → 检查是否需要人工审批
  ├─→ (金额 > 500) → [wait_approval] → 等待人工输入
  └─→ (金额 ≤ 500) → [auto_approve] → 自动批准
  ↓
[process] → 处理订单
  ↓
[complete] → 完成订单
  ↓
END
```

### 关键节点

#### 1. analyze (分析订单)
```python
def analyze_order(state: OrderState) -> OrderState:
    """分析订单信息"""
    # 输出订单详情
    # 更新订单状态
```

#### 2. check_approval (检查审批需求)
- **条件**: 金额 > 500 ?
- **true**: 路由到 `wait_approval`
- **false**: 路由到 `auto_approve`

#### 3. wait_approval (等待人工审批)
```python
def wait_human_approval(state: OrderState) -> OrderState:
    """等待人工审批（暂停点）"""
    user_input = input("请输入审批结果 (approve/reject): ")
    # 根据用户输入更新订单状态
```

#### 4. auto_approve (自动批准)
```python
def auto_approve(state: OrderState) -> OrderState:
    """自动批准小额订单"""
    # 直接批准，无需等待
```

#### 5. process & complete (处理和完成)
- 处理批准的订单
- 完成订单流程

## 💡 关键概念

### 1. 条件分支 (Conditional Edges)

```python
graph.add_conditional_edges(
    "check_approval",
    check_approval_needed,  # 条件函数
    {
        "wait_approval": "wait_approval",  # 结果 1 → 节点 1
        "auto_approve": "auto_approve",    # 结果 2 → 节点 2
    },
)
```

### 2. 暂停点 (Interrupt Point)

在 `wait_approval` 节点中，Agent 暂停执行并等待人工输入：

```python
user_input = input("请输入审批结果: ")
# Agent 在这里暂停，直到用户输入
```

### 3. 状态更新

根据人工反馈更新订单状态：

```python
if user_input == "approve":
    state["status"] = OrderStatus.APPROVED
else:
    state["status"] = OrderStatus.REJECTED
```

## 📊 演示场景

### 演示 1: 小额订单 (自动批准)
- 订单金额: ¥299.99
- 流程: 分析 → 检查 → 自动批准 → 处理 → 完成
- 特点: 无需人工干预

### 演示 2: 大额订单 (人工审批)
- 订单金额: ¥8999.99
- 流程: 分析 → 检查 → **等待人工批准** → 处理 → 完成
- 特点: 在暂停点等待用户输入

### 演示 3: 批量订单处理
- 多个订单，混合自动/人工审批
- 显示批量处理的统计信息

## 🔄 状态管理

### OrderState 定义

```python
class OrderState(TypedDict):
    order_id: str              # 订单ID
    customer_name: str         # 客户名称
    items: list                # 物品列表
    total_amount: float        # 订单金额
    status: OrderStatus        # 订单状态
    history: list              # 处理历史
    human_feedback: str        # 人工反馈
```

### OrderStatus 枚举

```python
class OrderStatus(str, Enum):
    PENDING = "pending"              # 待处理
    ANALYZING = "analyzing"          # 分析中
    WAITING_APPROVAL = "waiting_approval"  # 等待审批
    APPROVED = "approved"            # 已批准
    REJECTED = "rejected"            # 已拒绝
    PROCESSING = "processing"        # 处理中
    COMPLETED = "completed"          # 已完成
```

## 🔧 配置选项

### 审批阈值

在 `check_approval_needed` 函数中修改：

```python
approval_threshold = 500  # 修改这个值
```

### 自动路由规则

根据不同的业务规则修改条件函数：

```python
def check_approval_needed(state: OrderState) -> str:
    # 可以添加多个条件
    if state["total_amount"] > 500:
        return "wait_approval"
    # ... 其他条件
```

## 📈 扩展示例

### 1. 多级审批

```python
def create_multi_level_approval_graph():
    """创建多级审批流程"""
    # Manager 审批 (¥500-¥5000)
    # Director 审批 (¥5000-¥50000)
    # CFO 审批 (> ¥50000)
```

### 2. 并行审批

```python
# 多个审批人同时审批
for approver in approvers:
    create_parallel_approval_task(approver)
```

### 3. 条件分支增强

```python
def advanced_routing(state: OrderState) -> str:
    if is_vip_customer(state):
        return "vip_auto_approve"
    elif state["total_amount"] > 5000:
        return "director_approval"
    elif state["total_amount"] > 500:
        return "manager_approval"
    else:
        return "auto_approve"
```

## 🎯 实际应用场景

### 1. 订单管理系统
- 大额订单需要人工审批
- 特殊客户自动通过
- 风险客户需要加强审核

### 2. 审批工作流
- 请假申请
- 采购申请
- 合同审签

### 3. 内容审核
- 用户生成的内容审核
- 模糊内容需要人工判断
- 自动通过低风险内容

### 4. 风险控制
- 异常交易检测
- 大额支付审批
- 合规性检查

## 📝 代码示例

### 最简单的 Human-in-the-Loop

```python
def simple_human_approval(state: OrderState) -> OrderState:
    """最简单的人工审批实现"""
    print(f"订单 {state['order_id']}: ¥{state['total_amount']}")
    user_input = input("审批 (y/n): ")

    if user_input.lower() == "y":
        state["status"] = OrderStatus.APPROVED
    else:
        state["status"] = OrderStatus.REJECTED

    return state
```

### 完整的 Human-in-the-Loop

```python
def complete_human_approval(state: OrderState) -> OrderState:
    """完整的人工审批实现"""
    # 显示详细的订单信息
    # 提示用户做决定
    # 记录审批理由
    # 更新状态
    # 返回更新后的状态
```

## 🧪 测试

运行单个演示：

```bash
# 演示 1: 小额订单
python run_demo.py

# 交互式演示
python interactive_demo.py
```

## 🔍 调试技巧

### 1. 打印状态

```python
print(json.dumps(state, indent=2, default=str))
```

### 2. 检查流程路径

```python
print(f"当前节点: {node_name}")
print(f"订单状态: {state['status']}")
```

### 3. 查看处理历史

```python
for i, step in enumerate(state['history'], 1):
    print(f"{i}. {step}")
```

## 📚 相关文档

- [LangGraph 官方文档](https://langchain-ai.github.io/langgraph/)
- [Conditional Edges](https://langchain-ai.github.io/langgraph/concepts/low_level_concepts/#conditional-edges)
- [Human-in-the-Loop](https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/)

## 🎓 学习路径

1. ✅ 理解基本的 StateGraph
2. ✅ 学习条件分支（conditional edges）
3. ✅ 实现人工干预点
4. ✅ 管理复杂状态
5. ✅ 扩展为多级审批流程

## 💬 常见问题

### Q: 如何在多个节点中实现人工干预？
**A**: 在需要的每个节点中添加 `input()` 调用，或者创建专门的审批节点。

### Q: 如何保存审批历史？
**A**: 将所有操作添加到 `state['history']` 列表中。

### Q: 如何实现审批超时？
**A**: 使用带超时的输入（需要额外的库支持）。

### Q: 如何并行处理多个审批？
**A**: 使用 LangGraph 的并行处理功能（参考高级示例）。

## 📞 支持

如有问题，请查看：
- 本项目的 README.md（本文件）
- 代码中的详细注释
- LangGraph 官方文档

---

**版本**: 1.0
**最后更新**: 2026-02-01
**作者**: CatPaw AI Assistant

