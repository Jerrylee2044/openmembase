"""
OpenMemBase 项目知识模块 - 简化 API
"""

import asyncio
from typing import Optional, Dict, List

from .core import get_openmembase


async def project_create(
    name: str,
    description: str = "",
    path: str = ""
) -> str:
    """
    创建项目
    
    Args:
        name: 项目名称
        description: 项目描述
        path: 项目路径
        
    Returns:
        项目ID
        
    Example:
        >>> project_id = await project_create(
        ...     name="DC-AMS",
        ...     description="数据中心资产管理系统"
        ... )
    """
    omb = get_openmembase()
    return await omb.project_create(name, description, path)


async def project_delete(name: str) -> bool:
    """
    删除项目
    
    Args:
        name: 项目名称
        
    Returns:
        是否成功
    """
    omb = get_openmembase()
    return await omb.project_delete(name)


async def project_list() -> List[Dict]:
    """
    列出所有项目
    
    Returns:
        项目列表
    """
    omb = get_openmembase()
    return await omb.project_list()


async def project_get(name: str) -> Optional[Dict]:
    """
    获取项目详情
    
    Args:
        name: 项目名称
        
    Returns:
        项目信息
    """
    from project_kb.project_manager import get_project_manager
    pm = get_project_manager()
    return await pm.get_by_name(name)


async def project_stats(name: str) -> Dict:
    """
    获取项目统计
    
    Args:
        name: 项目名称
        
    Returns:
        {
            "total_resources": 100,
            "doc_count": 30,
            "code_count": 70
        }
    """
    omb = get_openmembase()
    return await omb.project_stats(name)


async def project_add_resource(
    project_name: str,
    source_path: str,
    content: str,
    resource_type: Optional[str] = None
) -> str:
    """
    添加资源到项目
    
    Args:
        project_name: 项目名称
        source_path: 资源路径
        content: 资源内容
        resource_type: 资源类型 (doc/code/web/session)
        
    Returns:
        资源ID
    """
    omb = get_openmembase()
    return await omb.project_add_resource(
        project_name, source_path, content, resource_type
    )


async def project_search(
    query: str,
    project_name: Optional[str] = None,
    top_k: int = 5
) -> List[Dict]:
    """
    搜索项目知识
    
    Args:
        query: 查询文本
        project_name: 限定项目（None搜索所有）
        top_k: 返回数量
        
    Returns:
        资源列表
        
    Example:
        >>> results = await project_search(
        ...     query="调拨功能",
        ...     project_name="DC-AMS"
        ... )
    """
    omb = get_openmembase()
    return await omb.project_search(query, project_name, top_k)


async def project_sync_files(
    project_name: str,
    paths: List[str]
) -> Dict:
    """
    同步项目文件
    
    Args:
        project_name: 项目名称
        paths: 要同步的路径列表
        
    Returns:
        同步结果
    """
    omb = get_openmembase()
    return await omb.project_sync_files(project_name, paths)


async def project_import_directory(
    project_name: str,
    directory: str,
    dry_run: bool = False
) -> Dict:
    """
    导入整个目录到项目
    
    Args:
        project_name: 项目名称
        directory: 目录路径
        dry_run: 仅预览不导入
        
    Returns:
        导入结果
    """
    from project_kb import batch_import_directory
    return await batch_import_directory(project_name, directory, dry_run)
