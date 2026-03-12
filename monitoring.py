"""
OpenMemBase 监控模块 - 性能指标收集
"""

import time
import json
from typing import Dict, List, Optional
from datetime import datetime
from collections import defaultdict

from .core import get_openmembase


class MetricsCollector:
    """指标收集器"""
    
    def __init__(self):
        self._counters = defaultdict(int)
        self._timers = defaultdict(list)
        self._start_time = datetime.now()
        self._query_log = []
        self._max_log_size = 1000
    
    def record_query(
        self,
        query_type: str,
        duration_ms: float,
        result_count: int,
        success: bool = True
    ):
        """记录查询"""
        self._counters[f"{query_type}_queries"] += 1
        if success:
            self._counters[f"{query_type}_success"] += 1
        else:
            self._counters[f"{query_type}_errors"] += 1
        
        self._timers[f"{query_type}_time"].append(duration_ms)
        
        # 记录日志
        self._query_log.append({
            "timestamp": datetime.now().isoformat(),
            "type": query_type,
            "duration_ms": round(duration_ms, 2),
            "results": result_count,
            "success": success
        })
        
        # 限制日志大小
        if len(self._query_log) > self._max_log_size:
            self._query_log = self._query_log[-self._max_log_size:]
    
    def get_metrics(self) -> Dict:
        """获取指标"""
        metrics = {
            "uptime": str(datetime.now() - self._start_time),
            "counters": dict(self._counters),
            "timers": {}
        }
        
        # 计算时间统计
        for name, times in self._timers.items():
            if times:
                metrics["timers"][name] = {
                    "count": len(times),
                    "avg_ms": round(sum(times) / len(times), 2),
                    "min_ms": round(min(times), 2),
                    "max_ms": round(max(times), 2)
                }
        
        return metrics
    
    def get_recent_queries(self, n: int = 10) -> List[Dict]:
        """获取最近查询"""
        return self._query_log[-n:]
    
    def get_slow_queries(self, threshold_ms: float = 2000) -> List[Dict]:
        """获取慢查询"""
        return [q for q in self._query_log if q["duration_ms"] > threshold_ms]
    
    def reset(self):
        """重置指标"""
        self._counters.clear()
        self._timers.clear()
        self._query_log.clear()
        self._start_time = datetime.now()


# 全局收集器
_collector = MetricsCollector()


def get_collector() -> MetricsCollector:
    """获取指标收集器"""
    return _collector


def get_metrics() -> Dict:
    """获取所有指标"""
    return _collector.get_metrics()


def print_metrics():
    """打印指标报告"""
    metrics = get_metrics()
    
    print(f"\n{'='*60}")
    print("OpenMemBase 监控报告")
    print(f"{'='*60}")
    print(f"运行时间: {metrics['uptime']}")
    print()
    
    if metrics['counters']:
        print("查询统计:")
        for key, value in sorted(metrics['counters'].items()):
            print(f"  {key}: {value}")
    
    if metrics['timers']:
        print("\n响应时间:")
        for name, stats in sorted(metrics['timers'].items()):
            print(f"  {name}:")
            print(f"    次数: {stats['count']}")
            print(f"    平均: {stats['avg_ms']}ms")
            print(f"    范围: [{stats['min_ms']}, {stats['max_ms']}]ms")
    
    # 慢查询
    slow = _collector.get_slow_queries()
    if slow:
        print(f"\n慢查询 ({len(slow)} 条):")
        for q in slow[-5:]:
            print(f"  - {q['type']}: {q['duration_ms']}ms")
    
    print(f"{'='*60}\n")


def reset_metrics():
    """重置指标"""
    _collector.reset()
    print("✅ 监控指标已重置")


# 装饰器
def monitored(query_type: str):
    """监控装饰器"""
    def decorator(func):
        async def async_wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = await func(*args, **kwargs)
                success = True
                result_count = len(result) if isinstance(result, list) else 0
            except Exception as e:
                success = False
                result_count = 0
                raise
            finally:
                duration = (time.time() - start) * 1000
                _collector.record_query(query_type, duration, result_count, success)
            return result
        
        def sync_wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = func(*args, **kwargs)
                success = True
                result_count = len(result) if isinstance(result, list) else 0
            except Exception as e:
                success = False
                result_count = 0
                raise
            finally:
                duration = (time.time() - start) * 1000
                _collector.record_query(query_type, duration, result_count, success)
            return result
        
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    return decorator
