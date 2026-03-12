---
name: openmembase
description: 统一记忆数据库 - 整合 Memory-LanceDB (会话记忆) + Project KB (项目知识库)
metadata:
  copaw:
    emoji: 🧠
    version: "1.0.0"
    author: "CoPaw"
    category: "memory"
---

# OpenMemBase - 统一记忆数据库

开箱即用的统一记忆数据库 Skill，整合 Memory-LanceDB 和 Project KB，为 CoPaw 提供统一的记忆管理能力。

## 功能特性

### 核心功能 ✅
- **统一 API**: 一套接口管理会话记忆和项目知识
- **智能路由**: 自动识别查询类型，路由到最佳记忆源
- **混合检索**: Vector + BM25 + Cross-Encoder 重排序
- **自动归档**: 会话自动归档到项目知识库
- **性能监控**: 完整的指标收集和分析

### 工程特性 ⚙️
- **灵活配置**: 支持环境变量、配置文件、代码配置
- **完善错误处理**: 结构化异常体系，详细的错误信息
- **日志系统**: 结构化日志，支持文件轮转和级别控制
- **类型安全**: 完整的类型注解和数据模型
- **CLI 工具**: 完整的命令行管理界面

## 快速开始

### 1. 安装依赖

```bash
# 确保已安装
pip install lancedb numpy httpx

# 设置 API Key
export DASHSCOPE_API_KEY="your_key"
export JINA_API_KEY="your_key"  # 可选，用于重排序
```

### 2. 初始化配置

```bash
# 使用 CLI 初始化
python -m openmembase init --db-path ~/.copaw/openmembase

# 或代码初始化
from openmembase import init_config
config = init_config(db_path="~/.copaw/openmembase", debug=False)
```

### 3. 基础使用

```python
import asyncio
from openmembase import (
    memory_add,
    memory_search,
    project_create,
    project_search,
    smart_query,
)

async def main():
    # 添加会话记忆
    memory_id = await memory_add(
        content="用户喜欢蓝色主题",
        memory_type="user_preference"
    )
    
    # 创建项目
    project_id = await project_create(
        name="DC-AMS",
        description="数据中心资产管理系统"
    )
    
    # 智能查询（自动路由）
    result = await smart_query("DC-AMS调拨功能怎么实现")
    print(f"路由类型: {result['query_type']}")
    print(f"结果数: {len(result['results'])}")

asyncio.run(main())
```

## API 参考

### 会话记忆

```python
# 添加记忆
memory_id = await memory_add(
    content="记忆内容",
    memory_type="session",  # session/user_preference/fact/decision/entity/reflection/other
    metadata={"key": "value"}
)

# 搜索记忆
results = await memory_search(
    query="查询文本",
    top_k=5,
    scope="all"  # all/global/user/session
)

# 获取/删除/统计
memory = await memory_get(memory_id)
success = await memory_delete(memory_id)
stats = await memory_stats()
```

### 项目知识

```python
# 创建项目
project_id = await project_create(
    name="项目名称",
    description="项目描述",
    path="/path/to/project"
)

# 列出/删除项目
projects = await project_list()
success = await project_delete("项目名称")

# 添加资源
resource_id = await project_add_resource(
    project_name="DC-AMS",
    source_path="app.py",
    content="...",
    resource_type="code"  # doc/code/web/session/other
)

# 搜索项目
results = await project_search(
    query="调拨功能",
    project_name="DC-AMS",  # None 搜索所有项目
    top_k=5
)

# 导入目录
from openmembase.projects import project_import_directory
result = await project_import_directory(
    project_name="DC-AMS",
    directory="/path/to/project",
    dry_run=False
)
```

### 智能查询

```python
# 自动路由查询
result = await smart_query("查询文本", top_k=5)

# 返回结构
{
    "query": "原始查询",
    "query_type": "personal|project|mixed",
    "results": [
        {
            "id": "...",
            "content": "...",
            "score": 0.95,
            "source": "memory|project",
            "metadata": {...}
        }
    ],
    "sources": {
        "memory": [...],
        "projects": [...]
    },
    "metadata": {
        "total_results": 10,
        "search_time_ms": 1500
    }
}
```

### 归档管理

```python
from openmembase import (
    archive_session,
    archive_old_sessions,
    auto_archive_start,
    auto_archive_stop
)

# 归档单个会话
resource_id = await archive_session(
    session_id="session_001",
    messages=[
        {"role": "user", "content": "如何调拨资产?"},
        {"role": "assistant", "content": "调拨功能在..."}
    ]
)

# 归档旧会话
stats = await archive_old_sessions(days=7)

# 自动归档
auto_archive_start()  # 启动后台归档
auto_archive_stop()   # 停止
```

### 监控

```python
from openmembase import (
    get_metrics,
    print_metrics,
    reset_metrics
)

# 打印性能报告
print_metrics()

# 获取指标数据
metrics = get_metrics()
print(f"查询次数: {metrics['counters']}")
print(f"平均响应: {metrics['timers']['avg_ms']}ms")

# 重置指标
reset_metrics()
```

## CLI 命令行工具

### 初始化

```bash
# 初始化配置
python -m openmembase init
python -m openmembase init --db-path /custom/path --embedding-provider dashscope
```

### 记忆管理

```bash
# 添加记忆
python -m openmembase memory add "用户喜欢蓝色主题" --type user_preference

# 搜索记忆
python -m openmembase memory search "用户偏好" --top-k 5

# 记忆统计
python -m openmembase memory stats
```

### 项目管理

```bash
# 创建项目
python -m openmembase project create DC-AMS -d "数据中心资产管理系统"

# 列出项目
python -m openmembase project list

# 搜索项目
python -m openmembase project search "调拨功能" -p DC-AMS

# 删除项目
python -m openmembase project delete DC-AMS --force
```

### 智能查询

```bash
# 智能查询
python -m openmembase query "DC-AMS调拨功能怎么实现"
```

### 监控

```bash
# 查看统计
python -m openmembase stats

# 查看性能指标
python -m openmembase metrics
```

## 配置

### 环境变量

```bash
# 必需
export DASHSCOPE_API_KEY="your_key"

# 可选
export OPENMEMBASE_DB_PATH="~/.copaw/openmembase"
export OPENMEMBASE_EMBEDDING_PROVIDER="dashscope"
export OPENMEMBASE_EMBEDDING_MODEL="text-embedding-v2"
export OPENMEMBASE_SIMILARITY_THRESHOLD="0.5"
export OPENMEMBASE_ARCHIVE_ENABLED="true"
export OPENMEMBASE_DEBUG="false"

# 重排序（可选）
export JINA_API_KEY="your_key"
export COHERE_API_KEY="your_key"
```

### 配置文件

```json
{
  "database": {
    "path": "~/.copaw/openmembase",
    "backup_enabled": true,
    "backup_interval_days": 7
  },
  "embedding": {
    "provider": "dashscope",
    "model": "text-embedding-v2",
    "dimensions": 1536,
    "batch_size": 10
  },
  "search": {
    "default_top_k": 5,
    "vector_weight": 0.5,
    "bm25_weight": 0.5,
    "similarity_threshold": 0.5,
    "rerank_enabled": true
  },
  "archive": {
    "enabled": true,
    "interval_hours": 24,
    "archive_after_days": 7
  },
  "monitoring": {
    "enabled": true,
    "log_queries": true,
    "slow_query_threshold_ms": 2000
  },
  "debug": false
}
```

配置文件位置: `~/.copaw/openmembase.json`

## 架构

```
┌─────────────────────────────────────────────────────────────┐
│                    OpenMemBase                              │
│                    (统一接口层)                              │
├─────────────────────────────────────────────────────────────┤
│  Unified API                                                │
│  ├── memory_add/search/stats                                │
│  ├── project_create/search/list                             │
│  ├── smart_query (自动路由)                                  │
│  └── archive/monitoring                                     │
├─────────────────────────────────────────────────────────────┤
│  Memory Layer                                               │
│  ┌─────────────────────┐    ┌─────────────────────────────┐ │
│  │   memory_lancedb    │    │       project_kb            │ │
│  │   (会话记忆)         │    │      (项目知识库)            │ │
│  │  • Session 记忆      │    │  • 项目文档                  │ │
│  │  • User 偏好         │    │  • 代码库                    │ │
│  │  • 实时对话          │    │  • 会话归档                  │ │
│  └─────────────────────┘    └─────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  Storage Layer                                              │
│  └── LanceDB (统一向量数据库)                                │
│      ├── memories 表 (会话记忆)                              │
│      ├── projects 表 (项目)                                  │
│      ├── project_resources 表 (资源)                         │
│      └── resource_chunks 表 (分块)                           │
└─────────────────────────────────────────────────────────────┘
```

## 文件结构

```
openmembase/
├── __init__.py        # 模块入口，导出所有 API
├── core.py            # 核心管理器 (OpenMemBase 类)
├── config.py          # 配置管理
├── types.py           # 类型定义 (数据模型、枚举)
├── exceptions.py      # 异常定义 (结构化错误处理)
├── logger.py          # 日志系统 (结构化日志)
├── memory.py          # 会话记忆 API
├── projects.py        # 项目知识 API
├── query.py           # 智能查询 (QueryRouter)
├── archive.py         # 归档管理
├── monitoring.py      # 性能监控
├── cli.py             # 命令行工具
├── SKILL.md           # 本文档
└── README.md          # 详细文档
```

## 性能

- **平均搜索响应时间**: ~1.9s
- **稳定性 (CV)**: 14.8%
- **支持并发**: 是
- **缓存支持**: 可配置

## 错误处理

```python
from openmembase.exceptions import (
    ConfigurationError,
    DatabaseError,
    NotFoundError,
    ValidationError
)

try:
    result = await smart_query("查询")
except NotFoundError as e:
    print(f"未找到: {e.message}")
except ValidationError as e:
    print(f"验证错误: {e.message}")
except OpenMemBaseError as e:
    print(f"错误 [{e.code}]: {e.message}")
```

## 日志

日志位置: `~/.copaw/logs/openmembase.log`

```python
from openmembase.logger import get_logger

logger = get_logger()
logger.info("操作成功", user_id="user_001")
logger.error("操作失败", error="timeout", retry=3)
```

## 版本

- **版本**: 1.0.0
- **状态**: 稳定
- **Python**: >= 3.8
- **依赖**: lancedb, numpy, httpx

## 许可证

MIT License
