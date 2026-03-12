"""
OpenMemBase 配置管理 - 企业级配置系统
"""

import os
import json
from typing import Optional, Dict, Any
from pathlib import Path
from dataclasses import dataclass, field, asdict


@dataclass
class DatabaseConfig:
    """数据库配置"""
    path: str = "~/.copaw/openmembase"
    table_memories: str = "memories"
    table_projects: str = "projects"
    table_resources: str = "project_resources"
    table_chunks: str = "resource_chunks"
    backup_enabled: bool = True
    backup_interval_days: int = 7


@dataclass
class EmbeddingConfig:
    """Embedding 配置"""
    provider: str = "dashscope"  # dashscope, openai, local
    model: str = "text-embedding-v2"
    dimensions: int = 1536
    batch_size: int = 10
    timeout: int = 30
    max_retries: int = 3
    
    @property
    def api_key(self) -> Optional[str]:
        return os.getenv("DASHSCOPE_API_KEY") or os.getenv("OPENMEMBASE_API_KEY")


@dataclass
class SearchConfig:
    """搜索配置"""
    default_top_k: int = 5
    max_top_k: int = 50
    vector_weight: float = 0.5
    bm25_weight: float = 0.5
    similarity_threshold: float = 0.5
    rerank_enabled: bool = True
    rerank_provider: str = "jina"  # jina, cohere, local
    
    @property
    def rerank_api_key(self) -> Optional[str]:
        if self.rerank_provider == "jina":
            return os.getenv("JINA_API_KEY")
        elif self.rerank_provider == "cohere":
            return os.getenv("COHERE_API_KEY")
        return None


@dataclass
class ArchiveConfig:
    """归档配置"""
    enabled: bool = True
    interval_hours: int = 24
    archive_after_days: int = 7
    min_messages: int = 5
    auto_start: bool = False


@dataclass
class MonitoringConfig:
    """监控配置"""
    enabled: bool = True
    log_queries: bool = True
    slow_query_threshold_ms: float = 2000.0
    max_log_size: int = 1000
    metrics_retention_days: int = 30


@dataclass
class SecurityConfig:
    """安全配置"""
    encrypt_backups: bool = False
    access_log_enabled: bool = True
    max_content_length: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: list = field(default_factory=lambda: [
        ".py", ".js", ".java", ".md", ".txt", ".json", ".yaml", ".yml",
        ".html", ".css", ".sql", ".sh", ".conf"
    ])


@dataclass
class OpenMemBaseConfig:
    """OpenMemBase 完整配置"""
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    embedding: EmbeddingConfig = field(default_factory=EmbeddingConfig)
    search: SearchConfig = field(default_factory=SearchConfig)
    archive: ArchiveConfig = field(default_factory=ArchiveConfig)
    monitoring: MonitoringConfig = field(default_factory=MonitoringConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    
    # 运行时配置
    debug: bool = False
    version: str = "1.0.0"
    
    @classmethod
    def from_env(cls) -> "OpenMemBaseConfig":
        """从环境变量加载配置"""
        config = cls()
        
        # 数据库路径
        if db_path := os.getenv("OPENMEMBASE_DB_PATH"):
            config.database.path = db_path
        
        # Embedding 配置
        if provider := os.getenv("OPENMEMBASE_EMBEDDING_PROVIDER"):
            config.embedding.provider = provider
        if model := os.getenv("OPENMEMBASE_EMBEDDING_MODEL"):
            config.embedding.model = model
        
        # 搜索配置
        if threshold := os.getenv("OPENMEMBASE_SIMILARITY_THRESHOLD"):
            config.search.similarity_threshold = float(threshold)
        
        # 归档配置
        if os.getenv("OPENMEMBASE_ARCHIVE_ENABLED", "").lower() == "false":
            config.archive.enabled = False
        if os.getenv("OPENMEMBASE_ARCHIVE_AUTO_START", "").lower() == "true":
            config.archive.auto_start = True
        
        # 调试模式
        if os.getenv("OPENMEMBASE_DEBUG", "").lower() == "true":
            config.debug = True
        
        return config
    
    @classmethod
    def from_file(cls, path: str) -> "OpenMemBaseConfig":
        """从文件加载配置"""
        config_path = Path(path).expanduser()
        if not config_path.exists():
            return cls.from_env()
        
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return cls(
            database=DatabaseConfig(**data.get('database', {})),
            embedding=EmbeddingConfig(**data.get('embedding', {})),
            search=SearchConfig(**data.get('search', {})),
            archive=ArchiveConfig(**data.get('archive', {})),
            monitoring=MonitoringConfig(**data.get('monitoring', {})),
            security=SecurityConfig(**data.get('security', {})),
            debug=data.get('debug', False)
        )
    
    def to_file(self, path: str):
        """保存配置到文件"""
        config_path = Path(path).expanduser()
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(self), f, indent=2, ensure_ascii=False)
    
    def validate(self) -> list:
        """验证配置，返回错误列表"""
        errors = []
        
        # 检查 API Key
        if not self.embedding.api_key:
            errors.append("DASHSCOPE_API_KEY 或 OPENMEMBASE_API_KEY 未设置")
        
        # 检查路径
        db_path = Path(self.database.path).expanduser()
        if not db_path.parent.exists():
            errors.append(f"数据库父目录不存在: {db_path.parent}")
        
        # 检查权重
        total_weight = self.search.vector_weight + self.search.bm25_weight
        if abs(total_weight - 1.0) > 0.01:
            errors.append(f"搜索权重之和应为 1.0，当前: {total_weight}")
        
        return errors
    
    @property
    def db_path(self) -> Path:
        """获取数据库路径"""
        return Path(self.database.path).expanduser()


# 全局配置实例
_config: Optional[OpenMemBaseConfig] = None


def get_config() -> OpenMemBaseConfig:
    """获取配置（单例）"""
    global _config
    if _config is None:
        # 尝试从文件加载
        config_file = Path.home() / ".copaw" / "openmembase.json"
        if config_file.exists():
            _config = OpenMemBaseConfig.from_file(str(config_file))
        else:
            _config = OpenMemBaseConfig.from_env()
    return _config


def set_config(config: OpenMemBaseConfig):
    """设置配置"""
    global _config
    _config = config


def init_config(
    db_path: Optional[str] = None,
    embedding_provider: Optional[str] = None,
    debug: bool = False
) -> OpenMemBaseConfig:
    """
    初始化配置
    
    Args:
        db_path: 数据库路径
        embedding_provider: Embedding 提供商
        debug: 调试模式
        
    Returns:
        配置对象
    """
    config = OpenMemBaseConfig.from_env()
    
    if db_path:
        config.database.path = db_path
    if embedding_provider:
        config.embedding.provider = embedding_provider
    config.debug = debug
    
    set_config(config)
    return config
