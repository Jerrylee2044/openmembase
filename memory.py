"""
OpenMemBase 会话记忆模块 - 简化 API
"""

import asyncio
from typing import Optional, Dict, List

from .core import get_openmembase


async def memory_add(
    content: str,
    memory_type: str = "session",
    metadata: Optional[Dict] = None
) -> str:
    """
    添加会话记忆
    
    Args:
        content: 记忆内容
        memory_type: 记忆类型 (session/user_preference/...)
        metadata: 元数据
        
    Returns:
        记忆ID
        
    Example:
        >>> memory_id = await memory_add(
        ...     content="用户喜欢蓝色主题",
        ...     memory_type="user_preference",
        ...     metadata={"user_id": "user_001"}
        ... )
    """
    omb = get_openmembase()
    return await omb.memory_add(content, memory_type, metadata)


async def memory_search(
    query: str,
    top_k: int = 5,
    scope: str = "all"
) -> List[Dict]:
    """
    搜索会话记忆
    
    Args:
        query: 查询文本
        top_k: 返回数量
        scope: 搜索范围 (all/session/user_preference/...)
        
    Returns:
        记忆列表
        
    Example:
        >>> results = await memory_search("用户喜欢什么颜色", top_k=3)
        >>> for r in results:
        ...     print(r['content'])
    """
    omb = get_openmembase()
    return await omb.memory_search(query, top_k, scope)


async def memory_get(memory_id: str) -> Optional[Dict]:
    """
    获取单个记忆
    
    Args:
        memory_id: 记忆ID
        
    Returns:
        记忆内容，不存在返回 None
    """
    omb = get_openmembase()
    return await omb.memory_get(memory_id)


async def memory_delete(memory_id: str) -> bool:
    """
    删除记忆
    
    Args:
        memory_id: 记忆ID
        
    Returns:
        是否成功
    """
    omb = get_openmembase()
    return await omb.memory_delete(memory_id)


async def memory_stats() -> Dict:
    """
    获取记忆统计
    
    Returns:
        {
            "total_memories": 100,
            "type_distribution": {"session": 80, "user_preference": 20}
        }
    """
    omb = get_openmembase()
    return await omb.memory_stats()
