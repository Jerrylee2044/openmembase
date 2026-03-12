"""
OpenMemBase 归档模块 - 自动归档管理
"""

import asyncio
from typing import Optional, Dict, List
from datetime import datetime, timedelta

from .core import get_openmembase


async def archive_session(
    session_id: str,
    messages: List[Dict],
    metadata: Optional[Dict] = None
) -> Optional[str]:
    """
    归档单个会话到项目知识库
    
    Args:
        session_id: 会话ID
        messages: 消息列表
        metadata: 元数据
        
    Returns:
        资源ID
        
    Example:
        >>> resource_id = await archive_session(
        ...     session_id="session_001",
        ...     messages=[
        ...         {"role": "user", "content": "如何调拨资产?"},
        ...         {"role": "assistant", "content": "调拨功能在..."}
        ...     ]
        ... )
    """
    from project_kb import archive_session as _archive
    return await _archive(session_id, messages, metadata)


async def archive_old_sessions(
    days: int = 7,
    min_messages: int = 5
) -> Dict:
    """
    归档旧会话
    
    Args:
        days: 归档多少天前的会话
        min_messages: 最少消息数
        
    Returns:
        {
            "archived": 15,
            "skipped": 3,
            "errors": 0
        }
    """
    from project_kb import archive_old_sessions as _archive_old
    return await _archive_old(days)


class AutoArchiveManager:
    """自动归档管理器"""
    
    def __init__(self):
        self._running = False
        self._task = None
        self.config = {
            "enabled": True,
            "interval_hours": 24,
            "archive_after_days": 7,
            "min_messages": 5
        }
    
    async def _archive_loop(self):
        """归档循环"""
        while self._running:
            try:
                if self.config["enabled"]:
                    print(f"[AutoArchive] {datetime.now()}: 开始归档...")
                    result = await archive_old_sessions(
                        days=self.config["archive_after_days"],
                        min_messages=self.config["min_messages"]
                    )
                    print(f"[AutoArchive] 完成: {result}")
                
                # 等待下次执行
                await asyncio.sleep(self.config["interval_hours"] * 3600)
                
            except Exception as e:
                print(f"[AutoArchive] 错误: {e}")
                await asyncio.sleep(3600)  # 出错后1小时重试
    
    def start(self):
        """启动自动归档"""
        if self._running:
            return
        
        self._running = True
        self._task = asyncio.create_task(self._archive_loop())
        print("[AutoArchive] 已启动")
    
    def stop(self):
        """停止自动归档"""
        self._running = False
        if self._task:
            self._task.cancel()
        print("[AutoArchive] 已停止")
    
    def configure(
        self,
        enabled: Optional[bool] = None,
        interval_hours: Optional[int] = None,
        archive_after_days: Optional[int] = None,
        min_messages: Optional[int] = None
    ):
        """配置自动归档"""
        if enabled is not None:
            self.config["enabled"] = enabled
        if interval_hours is not None:
            self.config["interval_hours"] = interval_hours
        if archive_after_days is not None:
            self.config["archive_after_days"] = archive_after_days
        if min_messages is not None:
            self.config["min_messages"] = min_messages
        
        print(f"[AutoArchive] 配置更新: {self.config}")


# 全局管理器
_archive_manager = None


def get_archive_manager() -> AutoArchiveManager:
    """获取归档管理器"""
    global _archive_manager
    if _archive_manager is None:
        _archive_manager = AutoArchiveManager()
    return _archive_manager


def auto_archive_start():
    """启动自动归档"""
    manager = get_archive_manager()
    manager.start()


def auto_archive_stop():
    """停止自动归档"""
    manager = get_archive_manager()
    manager.stop()


def auto_archive_configure(**kwargs):
    """配置自动归档"""
    manager = get_archive_manager()
    manager.configure(**kwargs)
