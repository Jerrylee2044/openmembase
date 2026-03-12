# OpenMemBase - 企业级统一记忆数据库

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/copaw/openmembase)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> 开箱即用的企业级记忆数据库，整合 Memory-LanceDB 和 Project KB，为 CoPaw 提供统一的记忆管理能力。

## 特性

- 🧠 **统一 API** - 一套接口管理会话记忆和项目知识
- 🎯 **智能路由** - 自动识别查询类型，路由到最佳记忆源
- 🔍 **混合检索** - Vector + BM25 + Cross-Encoder 重排序
- 📦 **自动归档** - 会话自动归档到项目知识库
- 📊 **性能监控** - 完整的指标收集和分析
- 🏢 **企业级** - 配置管理、错误处理、日志系统、类型安全
- 🖥️ **CLI 工具** - 完整的命令行管理界面

## 快速开始

### 安装

```bash
# 安装依赖
pip install lancedb numpy httpx

# 设置 API Key
export DASHSCOPE_API_KEY="your_key"
```

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

## 架构

```
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
```

## 文档

- [API 文档](docs/api.md)
- [配置指南](docs/config.md)
- [CLI 文档](docs/cli.md)
- [架构设计](docs/architecture.md)

## CLI 使用

```bash
# 初始化
openmembase init

# 添加记忆
openmembase memory add "用户喜欢蓝色主题" --type user_preference

# 搜索记忆
openmembase memory search "用户偏好"

# 创建项目
openmembase project create DC-AMS -d "数据中心资产管理系统"

# 智能查询
openmembase query "DC-AMS调拨功能怎么实现"

# 查看统计
openmembase stats
```

## 配置

### 环境变量

```bash
export DASHSCOPE_API_KEY="your_key"
export OPENMEMBASE_DB_PATH="~/.copaw/openmembase"
export OPENMEMBASE_DEBUG="false"
```

### 配置文件

`~/.copaw/openmembase.json`:

```json
{
  "database": {
    "path": "~/.copaw/openmembase",
    "backup_enabled": true
  },
  "embedding": {
    "provider": "dashscope",
    "model": "text-embedding-v2"
  },
  "search": {
    "default_top_k": 5,
    "rerank_enabled": true
  }
}
```

## 性能

- 平均搜索响应时间: ~1.9s
- 稳定性 (CV): 14.8%
- 支持并发: 是

## 贡献

欢迎提交 Issue 和 PR！

## 许可证

MIT License
