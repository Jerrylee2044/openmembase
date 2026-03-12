"""
OpenMemBase 智能查询模块 - 统一查询接口
"""

import asyncio
from typing import Optional, Dict, List

from .core import get_openmembase
from .types import QueryType


class QueryRouter:
    """查询路由器"""
    
    # 项目关键词
    PROJECT_KEYWORDS = [
        "项目", "代码", "功能", "实现", "设计", "架构",
        "project", "code", "function", "implement", "design",
        "app", "module", "class", "api", "database",
        "bug", "fix", "优化", "重构", "feature",
        "文件", "目录", "配置", "部署"
    ]
    
    # 个人关键词
    PERSONAL_KEYWORDS = [
        "我", "我的", "喜欢", "偏好", "习惯", "记得",
        "i ", "my ", "me ", "preference", "like", "favorite",
        "want", "need", "think", "feel"
    ]
    
    @classmethod
    def classify(cls, query: str) -> QueryType:
        """
        分类查询类型
        
        Args:
            query: 查询文本
            
        Returns:
            QueryType
        """
        query_lower = query.lower()
        
        # 计算项目分数
        project_score = sum(
            1 for kw in cls.PROJECT_KEYWORDS
            if kw.lower() in query_lower
        )
        
        # 计算个人分数
        personal_score = sum(
            1 for kw in cls.PERSONAL_KEYWORDS
            if kw.lower() in query_lower
        )
        
        # 判断类型
        if project_score > 0 and personal_score > 0:
            return QueryType.MIXED
        elif project_score > personal_score:
            return QueryType.PROJECT
        elif personal_score > project_score:
            return QueryType.PERSONAL
        else:
            return QueryType.UNKNOWN


async def smart_query(
    query: str,
    top_k: int = 5,
    context: Optional[Dict] = None
) -> Dict:
    """
    智能查询 - 自动路由到最佳记忆源
    
    Args:
        query: 查询文本
        top_k: 返回数量
        context: 上下文信息
            - current_project: 当前项目
            - user_id: 用户ID
            
    Returns:
        {
            "query": "原始查询",
            "query_type": "personal|project|mixed",
            "results": [...],
            "sources": {
                "memory": [...],
                "projects": [...]
            },
            "metadata": {
                "total_results": 10,
                "search_time_ms": 1500
            }
        }
        
    Example:
        >>> result = await smart_query("DC-AMS调拨功能怎么实现")
        >>> print(result['query_type'])  # 'project'
        >>> for r in result['results']:
        ...     print(r['name'], r['score'])
    """
    import time
    start_time = time.time()
    
    omb = get_openmembase()
    
    # 分类查询
    query_type = QueryRouter.classify(query)
    
    # 如果有明确的项目上下文，强制使用项目搜索
    if context and context.get('current_project'):
        query_type = QueryType.PROJECT
    
    results = []
    memory_results = []
    project_results = []
    
    # 根据类型查询
    if query_type == QueryType.PERSONAL:
        # 只查会话记忆
        memory_results = omb.memory_search(query, top_k=top_k)
        results = memory_results
        
    elif query_type == QueryType.PROJECT:
        # 只查项目知识
        project_name = context.get('current_project') if context else None
        project_results = await omb.project_search(query, project_name, top_k)
        results = project_results
        
    else:  # MIXED or UNKNOWN
        # 两者都查
        memory_results = omb.memory_search(query, top_k=top_k)
        project_results = await omb.project_search(query, None, top_k)
        
        # 合并结果（简单合并，后续可优化排序）
        results = memory_results + project_results
    
    search_time = (time.time() - start_time) * 1000
    
    return {
        "query": query,
        "query_type": query_type.value,
        "results": results[:top_k],
        "sources": {
            "memory": memory_results,
            "projects": project_results
        },
        "metadata": {
            "total_results": len(results),
            "memory_count": len(memory_results),
            "project_count": len(project_results),
            "search_time_ms": round(search_time, 2)
        }
    }


async def unified_search(
    query: str,
    search_type: str = "auto",
    top_k: int = 5,
    project_name: Optional[str] = None
) -> Dict:
    """
    统一搜索接口
    
    Args:
        query: 查询文本
        search_type: 搜索类型 (auto/memory/project/all)
        top_k: 返回数量
        project_name: 限定项目
        
    Returns:
        搜索结果
    """
    omb = get_openmembase()
    
    if search_type == "auto":
        return await smart_query(query, top_k)
    elif search_type == "memory":
        results = omb.memory_search(query, top_k)
        return {
            "query": query,
            "query_type": "memory",
            "results": results,
            "sources": {"memory": results, "projects": []}
        }
    elif search_type == "project":
        results = await omb.project_search(query, project_name, top_k)
        return {
            "query": query,
            "query_type": "project",
            "results": results,
            "sources": {"memory": [], "projects": results}
        }
    else:  # all
        memory_results = omb.memory_search(query, top_k)
        project_results = await omb.project_search(query, project_name, top_k)
        return {
            "query": query,
            "query_type": "all",
            "results": (memory_results + project_results)[:top_k],
            "sources": {"memory": memory_results, "projects": project_results}
        }
