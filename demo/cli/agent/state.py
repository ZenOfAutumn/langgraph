"""
Agent 状态定义

定义 Agent 的状态结构和数据类型。
"""

from typing import Sequence

from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict, Annotated


class AgentState(TypedDict):
    """Agent 的状态定义

    Attributes:
        messages: 消息历史列表
        context: 上下文信息
        next_action: 下一步操作
    """
    messages: Annotated[Sequence[BaseMessage], "Messages in the conversation"]
    context: str
    next_action: str

