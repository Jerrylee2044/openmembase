"""
OpenMemBase 日志系统 - 企业级日志管理
"""

import os
import sys
import json
import logging
import logging.handlers
from typing import Optional, Dict, Any
from pathlib import Path
from datetime import datetime


class StructuredFormatter(logging.Formatter):
    """结构化日志格式化器"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # 添加额外字段
        if hasattr(record, "extra"):
            log_data.update(record.extra)
        
        # 添加异常信息
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data, ensure_ascii=False)


class ConsoleFormatter(logging.Formatter):
    """控制台日志格式化器"""
    
    COLORS = {
        "DEBUG": "\033[36m",      # Cyan
        "INFO": "\033[32m",       # Green
        "WARNING": "\033[33m",    # Yellow
        "ERROR": "\033[31m",      # Red
        "CRITICAL": "\033[35m",   # Magenta
        "RESET": "\033[0m"
    }
    
    def format(self, record: logging.LogRecord) -> str:
        level_color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        reset = self.COLORS["RESET"]
        
        return f"{level_color}[{record.levelname}]{reset} {record.getMessage()}"


class OpenMemBaseLogger:
    """OpenMemBase 日志管理器"""
    
    def __init__(self, name: str = "openmembase"):
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self._initialized = False
    
    def init(
        self,
        level: str = "INFO",
        log_dir: Optional[str] = None,
        max_bytes: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 5,
        console: bool = True,
        structured: bool = False
    ):
        """
        初始化日志
        
        Args:
            level: 日志级别
            log_dir: 日志目录
            max_bytes: 单个日志文件最大大小
            backup_count: 保留的备份文件数
            console: 是否输出到控制台
            structured: 是否使用结构化格式
        """
        if self._initialized:
            return
        
        self.logger.setLevel(getattr(logging, level.upper()))
        
        # 清除现有处理器
        self.logger.handlers.clear()
        
        # 控制台输出
        if console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.DEBUG)
            console_formatter = ConsoleFormatter()
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(console_handler)
        
        # 文件输出
        if log_dir:
            log_path = Path(log_dir).expanduser()
            log_path.mkdir(parents=True, exist_ok=True)
            
            # 主日志文件
            file_handler = logging.handlers.RotatingFileHandler(
                log_path / "openmembase.log",
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding="utf-8"
            )
            file_handler.setLevel(logging.DEBUG)
            
            if structured:
                file_formatter = StructuredFormatter()
            else:
                file_formatter = logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
            
            # 错误日志单独文件
            error_handler = logging.handlers.RotatingFileHandler(
                log_path / "openmembase.error.log",
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding="utf-8"
            )
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(file_formatter)
            self.logger.addHandler(error_handler)
        
        self._initialized = True
        self.logger.info(f"Logger initialized: level={level}, structured={structured}")
    
    def debug(self, msg: str, **kwargs):
        """调试日志"""
        self._log(logging.DEBUG, msg, **kwargs)
    
    def info(self, msg: str, **kwargs):
        """信息日志"""
        self._log(logging.INFO, msg, **kwargs)
    
    def warning(self, msg: str, **kwargs):
        """警告日志"""
        self._log(logging.WARNING, msg, **kwargs)
    
    def error(self, msg: str, **kwargs):
        """错误日志"""
        self._log(logging.ERROR, msg, **kwargs)
    
    def critical(self, msg: str, **kwargs):
        """严重错误日志"""
        self._log(logging.CRITICAL, msg, **kwargs)
    
    def _log(self, level: int, msg: str, **kwargs):
        """内部日志方法"""
        extra = {"extra": kwargs} if kwargs else {}
        self.logger.log(level, msg, extra=extra)
    
    def log_query(
        self,
        query_type: str,
        query: str,
        duration_ms: float,
        results_count: int,
        success: bool = True
    ):
        """记录查询日志"""
        self.info(
            f"Query [{query_type}]: {query[:50]}...",
            type="query",
            query_type=query_type,
            query=query[:200],
            duration_ms=duration_ms,
            results_count=results_count,
            success=success
        )
    
    def log_operation(
        self,
        operation: str,
        resource_type: str,
        resource_id: Optional[str] = None,
        success: bool = True,
        details: Optional[Dict] = None
    ):
        """记录操作日志"""
        self.info(
            f"Operation [{operation}]: {resource_type}",
            type="operation",
            operation=operation,
            resource_type=resource_type,
            resource_id=resource_id,
            success=success,
            details=details
        )


# 全局日志实例
_logger: Optional[OpenMemBaseLogger] = None


def get_logger(name: str = "openmembase") -> OpenMemBaseLogger:
    """获取日志实例"""
    global _logger
    if _logger is None:
        _logger = OpenMemBaseLogger(name)
    return _logger


def init_logger(
    level: str = "INFO",
    log_dir: Optional[str] = None,
    **kwargs
) -> OpenMemBaseLogger:
    """初始化日志"""
    logger = get_logger()
    
    if log_dir is None:
        log_dir = Path.home() / ".copaw" / "logs"
    
    logger.init(level=level, log_dir=str(log_dir), **kwargs)
    return logger
