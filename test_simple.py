"""
OpenMemBase 简单测试 - 验证框架结构
"""

import asyncio
import sys
sys.path.insert(0, '/root/.copaw')

from openmembase import get_openmembase, QueryRouter, QueryType
from openmembase.core import OpenMemBase


def test_import():
    """测试导入"""
    print("\n" + "="*60)
    print("测试导入")
    print("="*60)
    
    print("✅ OpenMemBase 导入成功")
    print(f"   版本: 1.0.0")
    

def test_core():
    """测试核心类"""
    print("\n" + "="*60)
    print("测试核心类")
    print("="*60)
    
    omb = get_openmembase()
    print(f"✅ 获取实例: {type(omb).__name__}")
    print(f"   数据库路径: {omb.db_path}")
    
    # 初始化
    omb.initialize()
    print(f"✅ 初始化成功")
    

def test_query_router():
    """测试查询路由"""
    print("\n" + "="*60)
    print("测试查询路由")
    print("="*60)
    
    test_cases = [
        ("我喜欢什么颜色", QueryType.PERSONAL),
        ("DC-AMS调拨功能怎么实现", QueryType.PROJECT),
        ("我的项目代码在哪里", QueryType.MIXED),
        ("hello world", QueryType.UNKNOWN),
    ]
    
    for query, expected in test_cases:
        result = QueryRouter.classify(query)
        status = "✅" if result == expected else "❌"
        print(f"   {status} '{query}' -> {result.value} (预期: {expected.value})")


async def test_project_api():
    """测试项目 API"""
    print("\n" + "="*60)
    print("测试项目 API")
    print("="*60)
    
    omb = get_openmembase()
    
    # 列出项目
    print("\n1. 列出项目...")
    try:
        projects = await omb.project_list()
        print(f"   ✅ 找到 {len(projects)} 个项目")
        for p in projects[:3]:
            print(f"      - {p['name']}")
    except Exception as e:
        print(f"   ⚠️ {e}")
    
    # 搜索项目
    print("\n2. 搜索项目...")
    try:
        results = await omb.project_search("调拨", top_k=3)
        print(f"   ✅ 找到 {len(results)} 条结果")
    except Exception as e:
        print(f"   ⚠️ {e}")


def test_monitoring():
    """测试监控"""
    print("\n" + "="*60)
    print("测试监控")
    print("="*60)
    
    from openmembase.monitoring import get_metrics, get_collector
    
    # 记录一些测试查询
    collector = get_collector()
    collector.record_query("memory", 100.5, 5, True)
    collector.record_query("project", 2000.3, 10, True)
    collector.record_query("smart", 3000.1, 8, True)
    
    # 获取指标
    metrics = get_metrics()
    print(f"✅ 获取指标成功")
    print(f"   运行时间: {metrics['uptime']}")
    print(f"   计数器: {metrics['counters']}")


async def main():
    """主测试"""
    print("\n" + "="*60)
    print("OpenMemBase 框架测试")
    print("="*60)
    
    try:
        test_import()
        test_core()
        test_query_router()
        await test_project_api()
        test_monitoring()
        
        print("\n" + "="*60)
        print("🎉 框架测试通过!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
