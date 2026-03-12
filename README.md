# OpenMemBase - 统一记忆数据库

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/Jerrylee2044/openmembase)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> 开箱即用的统一记忆数据库，为 CoPaw 提供会话记忆和项目知识管理能力。

## 特性

- 🧠 **统一 API** - 一套接口管理会话记忆和项目知识
- 🎯 **智能路由** - 自动识别查询类型，路由到最佳记忆源
- 🔍 **混合检索** - Vector + BM25 + Cross-Encoder 重排序
- 📦 **自动归档** - 会话自动归档到项目知识库
- 📊 **性能监控** - 完整的指标收集和分析
- ⚙️ **灵活配置** - 支持环境变量、配置文件、代码配置
- 🖥️ **CLI 工具** - 完整的命令行管理界面

## 快速开始

### 安装

```bash
# 安装依赖
pip install lancedb numpy httpx

# 设置 API Key（阿里云 DashScope）
export DASHSCOPE_API_KEY="your_key"
```

**API Key 获取方式**：
- 平台：阿里云 [DashScope](https://dashscope.aliyun.com/)
- 用途：文本嵌入（Embedding）服务，用于向量检索
- 步骤：
  1. 注册/登录阿里云账号
  2. 进入 DashScope 控制台
  3. 创建 API Key
  4. 复制 Key 并设置环境变量

### 基础使用

```python
import asyncio
from openmembase import memory_add, memory_search, smart_query

async def main():
    # 添加记忆
    memory_id = await memory_add(
        content="用户喜欢蓝色主题",
        memory_type="user_preference"
    )
    
    # 搜索记忆
    results = await memory_search("用户偏好")
    
    # 智能查询
    result = await smart_query("DC-AMS调拨功能怎么实现")
    print(result['query_type'])  # 'project'

asyncio.run(main())
```

## 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                    OpenMemBase                              │
│                    (统一接口层)                              │
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
```

### 核心概念

| 概念 | 说明 | 使用场景 |
|------|------|----------|
| **Session Memory** | 短期会话记忆，高频访问 | 用户偏好、对话上下文、临时决策 |
| **Project Knowledge** | 长期项目知识，结构化存储 | 项目文档、代码库、归档会话 |
| **Smart Query** | 智能路由查询 | 自动识别查询意图，选择最佳数据源 |

## API 文档

### 会话记忆 API

```python
# 添加记忆
memory_id = await memory_add(
    content="记忆内容",
    memory_type="user_preference",  # session/user_preference/fact/decision/entity/reflection/other
    metadata={"key": "value"}
)

# 搜索记忆
results = await memory_search(
    query="查询文本",
    top_k=5,
    scope="all"  # all/global/user/session
)

# 获取记忆
memory = await memory_get(memory_id)

# 删除记忆
success = await memory_delete(memory_id)

# 记忆统计
stats = await memory_stats()
```

### 项目知识 API

```python
# 创建项目
project_id = await project_create(
    name="DC-AMS",
    description="数据中心资产管理系统",
    path="/path/to/project"
)

# 列出项目
projects = await project_list()

# 删除项目
success = await project_delete("DC-AMS")

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

### 智能查询 API

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

### 归档管理 API

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

### 性能监控 API

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

## 配置指南

### 环境变量

```bash
# 必需 - 阿里云 DashScope API Key（用于文本嵌入）
export DASHSCOPE_API_KEY="your_key"

# 可选 - OpenMemBase 配置
export OPENMEMBASE_DB_PATH="~/.copaw/openmembase"
export OPENMEMBASE_EMBEDDING_PROVIDER="dashscope"
export OPENMEMBASE_EMBEDDING_MODEL="text-embedding-v2"
export OPENMEMBASE_SIMILARITY_THRESHOLD="0.5"
export OPENMEMBASE_ARCHIVE_ENABLED="true"
export OPENMEMBASE_DEBUG="false"

# 可选 - 重排序服务 API Key
export JINA_API_KEY="your_key"      # Jina AI 重排序
export COHERE_API_KEY="your_key"    # Cohere 重排序
```

### 配置文件

配置文件位置: `~/.copaw/openmembase.json`

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

### 配置优先级

配置加载优先级（高到低）：
1. 代码中传入的参数
2. 环境变量
3. 配置文件
4. 默认值

## CLI 文档

### 初始化

```bash
# 初始化配置
python -m openmembase init

# 指定数据库路径
python -m openmembase init --db-path /custom/path

# 指定 embedding 提供商
python -m openmembase init --embedding-provider dashscope
```

### 记忆管理

```bash
# 添加记忆
python -m openmembase memory add "用户喜欢蓝色主题" --type user_preference

# 搜索记忆
python -m openmembase memory search "用户偏好" --top-k 5

# 获取记忆统计
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
# 智能查询（自动路由）
python -m openmembase query "DC-AMS调拨功能怎么实现"
```

### 监控

```bash
# 查看统计
python -m openmembase stats

# 查看性能指标
python -m openmembase metrics
```

### 帮助

```bash
# 查看所有命令
python -m openmembase --help

# 查看具体命令帮助
python -m openmembase memory --help
python -m openmembase project create --help
```

## 性能

- **平均搜索响应时间**: ~1.9s
- **稳定性 (CV)**: 14.8%
- **支持并发**: 是
- **缓存支持**: 可配置

## 日志

日志位置: `~/.copaw/logs/openmembase.log`

```python
from openmembase.logger import get_logger

logger = get_logger()
logger.info("操作成功", user_id="user_001")
logger.error("操作失败", error="timeout", retry=3)
```

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

## 更多文档

- [SKILL.md](SKILL.md) - Skill 使用文档
- [STATUS.md](STATUS.md) - 项目状态报告

## 贡献

欢迎提交 Issue 和 PR！

## 许可证

MIT License
