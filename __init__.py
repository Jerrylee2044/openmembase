"""
OpenMemBase - 企业级统一记忆数据库系统

整合 Memory-LanceDB (会话记忆) + Project KB (项目知识库)
提供统一的记忆管理、检索和归档能力

Architecture:
┌─────────────────────────────────────────────────────────────┐
│                    OpenMemBase                              │
├─────────────────────────────────────────────────────────────┤
│  Unified API                                                │
│  ├── memory_add()      - 添加会话记忆                      │
│  ├── memory_search()   - 搜索记忆                          │
│  ├── project_create()  - 创建项目                          │
│  ├── project_search()  - 搜索项目知识                      │
│  └── smart_query()     - 智能路由查询                      │
├─────────────────────────────────────────────────────────────┤
│  Memory Layer                                               │
│  ├── SessionMemory     - 短期会话记忆 (热数据)              │
│  └── ProjectKnowledge  - 长期项目知识 (冷数据)              │
├─────────────────────────────────────────────────────────────┤
│  Storage Layer                                              │
│  └── LanceDB           - 统一向量数据库                     │
└─────────────────────────────────────────────────────────────┘

Version: 1.0.0
Author: CoPaw
"""

__version__ = "1.0.0"
__author__ = "CoPaw"
__license__ = "MIT"

# 配置
from .config import (
    OpenMemBaseConfig,
    DatabaseConfig,
    EmbeddingConfig,
    SearchConfig,
    ArchiveConfig,
    MonitoringConfig,
    SecurityConfig,
    get_config,
    set_config,
    init_config,
)

# 类型
from .types import (
    Memory,
    Project,
    Resource,
    SearchResult,
    QueryResult,
    ArchiveResult,
    StatsResult,
    MemoryType,
    ResourceType,
    QueryType,
    ScopeLevel,
)

# 异常
from .exceptions import (
    OpenMemBaseError,
    ConfigurationError,
    DatabaseError,
    EmbeddingError,
    SearchError,
    ProjectError,
    ResourceError,
    ValidationError,
    NotFoundError,
    PermissionError,
    RateLimitError,
    ArchiveError,
)

# 日志
from .logger import (
    OpenMemBaseLogger,
    get_logger,
    init_logger,
)

# 核心
from .core import (
    OpenMemBase,
    get_openmembase,
)

# 会话记忆 API
from .memory import (
    memory_add,
    memory_search,
    memory_get,
    memory_delete,
    memory_stats,
)

# 项目知识 API
from .projects import (
    project_create,
    project_delete,
    project_list,
    project_get,
    project_stats,
    project_add_resource,
    project_search,
    project_sync_files,
)

# 智能查询
from .query import (
    smart_query,
    QueryRouter,
    unified_search,
)

# 归档管理
from .archive import (
    archive_session,
    archive_old_sessions,
    auto_archive_start,
    auto_archive_stop,
    auto_archive_configure,
)

# 监控
from .monitoring import (
    get_metrics,
    print_metrics,
    reset_metrics,
    monitored,
)

__all__ = [
    # 版本信息
    "__version__",
    "__author__",
    "__license__",
    
    # 配置
    "OpenMemBaseConfig",
    "DatabaseConfig",
    "EmbeddingConfig",
    "SearchConfig",
    "ArchiveConfig",
    "MonitoringConfig",
    "SecurityConfig",
    "get_config",
    "set_config",
    "init_config",
    
    # 类型
    "Memory",
    "Project",
    "Resource",
    "SearchResult",
    "QueryResult",
    "ArchiveResult",
    "StatsResult",
    "MemoryType",
    "ResourceType",
    "QueryType",
    "ScopeLevel",
    
    # 异常
    "OpenMemBaseError",
    "ConfigurationError",
    "DatabaseError",
    "EmbeddingError",
    "SearchError",
    "ProjectError",
    "ResourceError",
    "ValidationError",
    "NotFoundError",
    "PermissionError",
    "RateLimitError",
    "ArchiveError",
    
    # 日志
    "OpenMemBaseLogger",
    "get_logger",
    "init_logger",
    
    # 核心
    "OpenMemBase",
    "get_openmembase",
    
    # 会话记忆
    "memory_add",
    "memory_search",
    "memory_get",
    "memory_delete",
    "memory_stats",
    
    # 项目知识
    "project_create",
    "project_delete",
    "project_list",
    "project_get",
    "project_stats",
    "project_add_resource",
    "project_search",
    "project_sync_files",
    
    # 智能查询
    "smart_query",
    "QueryRouter",
    "unified_search",
    
    # 归档
    "archive_session",
    "archive_old_sessions",
    "auto_archive_start",
    "auto_archive_stop",
    "auto_archive_configure",
    
    # 监控
    "get_metrics",
    "print_metrics",
    "reset_metrics",
    "monitored",
]
