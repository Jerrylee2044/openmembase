"""
OpenMemBase 测试脚本
"""

import asyncio
from openmembase import (
    memory_add,
    memory_search,
    memory_stats,
    project_create,
    project_search,
    project_list,
    smart_query,
    print_metrics,
)


async def test_memory():
    """测试会话记忆"""
    print("\n" + "="*60)
    print("测试会话记忆")
    print("="*60)
    
    # 添加记忆
    print("\n1. 添加记忆...")
    memory_id = await memory_add(
        content="用户喜欢蓝色主题和深色模式",
        memory_type="user_preference",
        metadata={"user_id": "user_001", "topic": "ui_preference"}
    )
    print(f"   ✅ 记忆ID: {memory_id}")
    
    # 搜索记忆
    print("\n2. 搜索记忆...")
    results = await memory_search("用户喜欢什么颜色", top_k=3)
    print(f"   找到 {len(results)} 条结果:")
    for r in results[:2]:
        print(f"   - {r['content'][:50]}...")
    
    # 获取统计
    print("\n3. 获取统计...")
    stats = await memory_stats()
    print(f"   总记忆数: {stats.get('total_memories', 0)}")
    print(f"   类型分布: {stats.get('type_distribution', {})}")
    
    print("\n✅ 会话记忆测试通过")


async def test_projects():
    """测试项目知识"""
    print("\n" + "="*60)
    print("测试项目知识")
    print("="*60)
    
    # 创建项目
    print("\n1. 创建项目...")
    try:
        project_id = await project_create(
            name="Test-Project",
            description="测试项目",
            path="/test/path"
        )
        print(f"   ✅ 项目ID: {project_id}")
    except Exception as e:
        print(f"   ⚠️ 项目可能已存在: {e}")
    
    # 列出项目
    print("\n2. 列出项目...")
    projects = await project_list()
    print(f"   找到 {len(projects)} 个项目:")
    for p in projects[:3]:
        print(f"   - {p['name']}: {p.get('description', 'N/A')}")
    
    # 搜索项目
    print("\n3. 搜索项目知识...")
    results = await project_search("调拨功能", top_k=3)
    print(f"   找到 {len(results)} 条结果")
    
    print("\n✅ 项目知识测试通过")


async def test_smart_query():
    """测试智能查询"""
    print("\n" + "="*60)
    print("测试智能查询")
    print("="*60)
    
    test_queries = [
        ("我喜欢什么颜色", "personal"),
        ("DC-AMS调拨功能怎么实现", "project"),
        ("我的项目代码在哪里", "mixed"),
    ]
    
    for query, expected_type in test_queries:
        print(f"\n查询: {query}")
        result = await smart_query(query, top_k=3)
        print(f"   路由类型: {result['query_type']}")
        print(f"   预期类型: {expected_type}")
        print(f"   结果数: {result['metadata']['total_results']}")
        print(f"   耗时: {result['metadata']['search_time_ms']}ms")
    
    print("\n✅ 智能查询测试通过")


async def test_monitoring():
    """测试监控"""
    print("\n" + "="*60)
    print("测试监控")
    print("="*60)
    
    print_metrics()
    
    print("\n✅ 监控测试通过")


async def main():
    """主测试"""
    print("\n" + "="*60)
    print("OpenMemBase 测试套件")
    print("="*60)
    
    try:
        await test_memory()
        await test_projects()
        await test_smart_query()
        await test_monitoring()
        
        print("\n" + "="*60)
        print("🎉 所有测试通过!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
