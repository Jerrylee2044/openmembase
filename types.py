"""
OpenMemBase 类型定义 - 企业级类型系统
"""

from typing import Optional, List, Dict, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class MemoryType(str, Enum):
    """记忆类型"""
    SESSION = "session"
    USER_PREFERENCE = "user_preference"
    FACT = "fact"
    DECISION = "decision"
    ENTITY = "entity"
    REFLECTION = "reflection"
    OTHER = "other"


class ResourceType(str, Enum):
    """资源类型"""
    DOC = "doc"
    CODE = "code"
    WEB = "web"
    SESSION = "session"
    OTHER = "other"


class QueryType(str, Enum):
    """查询类型"""
    PERSONAL = "personal"
    PROJECT = "project"
    MIXED = "mixed"
    UNKNOWN = "unknown"


class ScopeLevel(str, Enum):
    """作用域级别"""
    GLOBAL = "global"
    USER = "user"
    SESSION = "session"


@dataclass
class Memory:
    """记忆数据模型"""
    id: str
    content: str
    memory_type: MemoryType
    scope: ScopeLevel
    scope_id: str
    importance: float = 0.5
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "content": self.content,
            "memory_type": self.memory_type.value,
            "scope": self.scope.value,
            "scope_id": self.scope_id,
            "importance": self.importance,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "metadata": self.metadata
        }


@dataclass
class Project:
    """项目数据模型"""
    id: str
    name: str
    description: str = ""
    path: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "path": self.path,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "metadata": self.metadata
        }


@dataclass
class Resource:
    """资源数据模型"""
    id: str
    project_id: str
    name: str
    resource_type: ResourceType
    content: str
    source_path: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "project_id": self.project_id,
            "name": self.name,
            "resource_type": self.resource_type.value,
            "content": self.content[:200] + "..." if len(self.content) > 200 else self.content,
            "source_path": self.source_path,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "metadata": self.metadata
        }


@dataclass
class SearchResult:
    """搜索结果"""
    id: str
    content: str
    score: float
    source: str  # "memory" or "project"
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "content": self.content,
            "score": round(self.score, 4),
            "source": self.source,
            "metadata": self.metadata
        }


@dataclass
class QueryResult:
    """查询结果"""
    query: str
    query_type: QueryType
    results: List[SearchResult]
    sources: Dict[str, List[SearchResult]]
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            "query": self.query,
            "query_type": self.query_type.value,
            "results": [r.to_dict() for r in self.results],
            "sources": {
                k: [r.to_dict() for r in v]
                for k, v in self.sources.items()
            },
            "metadata": self.metadata
        }


@dataclass
class ArchiveResult:
    """归档结果"""
    resource_id: Optional[str]
    success: bool
    message: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StatsResult:
    """统计结果"""
    memory_count: int
    memory_types: Dict[str, int]
    project_count: int
    resource_count: int
    database_path: str
    
    def to_dict(self) -> Dict:
        return {
            "memory": {
                "count": self.memory_count,
                "types": self.memory_types
            },
            "projects": {
                "count": self.project_count,
                "total_resources": self.resource_count
            },
            "database_path": self.database_path
        }


# 类型别名
MemoryList = List[Memory]
ProjectList = List[Project]
ResourceList = List[Resource]
SearchResultList = List[SearchResult]
JSONDict = Dict[str, Any]
