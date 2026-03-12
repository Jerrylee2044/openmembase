"""
OpenMemBase 核心 - 统一记忆管理器
"""

import os
import asyncio
from typing import Optional, Dict, Any
from pathlib import Path

# 导入底层实现
import sys
sys.path.insert(0, '/root/.copaw/customized_skills')

from memory_lancedb import (
    memory_store as _mem_add,
    memory_search as _mem_search,
    get_memory_stats as _mem_stats,
)

from memory_lancedb.manager import (
    delete_memory as _mem_delete,
    list_all_memories as _mem_list,
)

from project_kb import (
    project_kb_create as _proj_create,
    project_kb_delete_project as _proj_delete,
    project_kb_list as _proj_list,
    project_kb_search as _proj_search,
    project_kb_add_resource as _proj_add_resource,
    project_kb_stats as _proj_stats,
    sync_project as _proj_sync,
    smart_search as _smart_search,
)


class OpenMemBase:
    """
    OpenMemBase 统一记忆管理器
    
    整合 Memory-LanceDB 和 Project KB 的能力
    提供统一的 API 接口
    """
    
    def __init__(self, db_path: Optional[str] = None):
        """
        初始化 OpenMemBase
        
        Args:
            db_path: 数据库路径，默认使用 ~/.copaw/lancedb_memory
        """
        self.db_path = db_path or os.path.expanduser("~/.copaw/lancedb_memory")
        self._initialized = False
        
    def initialize(self):
        """初始化数据库连接"""
        if self._initialized:
            return
        
        # 确保目录存在
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        # 初始化底层表
        from memory_lancedb.store import init_table as _init_mem
        from project_kb.models import init_tables as _init_proj
        
        _init_mem()
        _init_proj()
        
        self._initialized = True
        print(f"✅ OpenMemBase initialized at {self.db_path}")
    
    # ========== 会话记忆 API (异步) ==========
    
    async def memory_add(
        self,
        content: str,
        memory_type: str = "session",
        metadata: Optional[Dict] = None
    ) -> str:
        """
        添加会话记忆
        
        Args:
            content: 记忆内容
            memory_type: 记忆类型
            metadata: 元数据
            
        Returns:
            记忆ID
        """
        self.initialize()
        return await _mem_add(content, memory_type, metadata or {})
    
    async def memory_search(
        self,
        query: str,
        top_k: int = 5,
        scope: str = "all"
    ) -> list:
        """
        搜索会话记忆
        
        Args:
            query: 查询文本
            top_k: 返回数量
            scope: 搜索范围
            
        Returns:
            记忆列表
        """
        self.initialize()
        return await _mem_search(query, top_k, scope)
    
    async def memory_get(self, memory_id: str) -> Optional[Dict]:
        """获取单个记忆"""
        self.initialize()
        # 从列表中查找
        memories = await _mem_list(limit=10000)
        for mem in memories:
            if mem.get('id') == memory_id:
                return mem
        return None
    
    async def memory_delete(self, memory_id: str) -> bool:
        """删除记忆"""
        self.initialize()
        return await _mem_delete(memory_id)
    
    async def memory_stats(self) -> Dict:
        """获取记忆统计"""
        self.initialize()
        return await _mem_stats()
    
    # ========== 项目知识 API (异步) ==========
    
    async def project_create(
        self,
        name: str,
        description: str = "",
        path: str = ""
    ) -> str:
        """创建项目"""
        self.initialize()
        return await _proj_create(name, description, path)
    
    async def project_delete(self, name: str) -> bool:
        """删除项目"""
        self.initialize()
        return await _proj_delete(name)
    
    async def project_list(self) -> list:
        """列出所有项目"""
        self.initialize()
        return await _proj_list()
    
    async def project_search(
        self,
        query: str,
        project_name: Optional[str] = None,
        top_k: int = 5
    ) -> list:
        """
        搜索项目知识
        
        Args:
            query: 查询文本
            project_name: 限定项目
            top_k: 返回数量
            
        Returns:
            资源列表
        """
        self.initialize()
        return await _proj_search(query, project_name, top_k=top_k)
    
    async def project_add_resource(
        self,
        project_name: str,
        source_path: str,
        content: str,
        resource_type: Optional[str] = None
    ) -> str:
        """添加资源到项目"""
        self.initialize()
        return await _proj_add_resource(
            project_name, source_path, content, resource_type
        )
    
    async def project_stats(self, project_name: str) -> Dict:
        """获取项目统计"""
        self.initialize()
        return await _proj_stats(project_name)
    
    async def project_sync_files(
        self,
        project_name: str,
        paths: list
    ):
        """同步项目文件"""
        self.initialize()
        return await _proj_sync(project_name, paths)
    
    # ========== 智能查询 API ==========
    
    async def smart_query(
        self,
        query: str,
        top_k: int = 5
    ) -> Dict:
        """
        智能查询 - 自动路由到最佳记忆源
        
        Args:
            query: 查询文本
            top_k: 返回数量
            
        Returns:
            {
                "query_type": "personal|project|mixed",
                "results": [...],
                "sources": {...}
            }
        """
        self.initialize()
        return await _smart_search(query, top_k=top_k)
    
    # ========== 统一统计 ==========
    
    async def stats(self) -> Dict:
        """获取完整统计"""
        self.initialize()
        
        mem_stats = await self.memory_stats()
        projects = await self.project_list()
        
        total_resources = 0
        for p in projects:
            p_stats = await self.project_stats(p['name'])
            total_resources += p_stats.get('total_resources', 0)
        
        return {
            "memory": {
                "count": mem_stats.get('total_memories', 0),
                "types": mem_stats.get('type_distribution', {})
            },
            "projects": {
                "count": len(projects),
                "total_resources": total_resources
            },
            "database_path": self.db_path
        }


# 全局实例
_omb = None


def get_openmembase(db_path: Optional[str] = None) -> OpenMemBase:
    """获取 OpenMemBase 实例（单例）"""
    global _omb
    if _omb is None:
        _omb = OpenMemBase(db_path)
    return _omb
