"""
OpenMemBase CLI - 企业级命令行工具
"""

import sys
import asyncio
import argparse
from pathlib import Path
from typing import Optional

# 添加路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from openmembase import (
    get_openmembase,
    memory_search,
    memory_add,
    memory_stats,
    project_list,
    project_create,
    project_search,
    project_delete,
    smart_query,
    print_metrics,
    get_metrics,
)
from openmembase.config import init_config, get_config
from openmembase.logger import init_logger


def create_parser() -> argparse.ArgumentParser:
    """创建命令行解析器"""
    parser = argparse.ArgumentParser(
        prog="openmembase",
        description="OpenMemBase - 统一记忆数据库 CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  openmembase init                           # 初始化配置
  openmembase memory add "用户喜欢蓝色"       # 添加记忆
  openmembase memory search "用户偏好"        # 搜索记忆
  openmembase project create DC-AMS          # 创建项目
  openmembase project search "调拨功能"       # 搜索项目
  openmembase query "DC-AMS调拨怎么实现"      # 智能查询
  openmembase stats                          # 查看统计
  openmembase metrics                        # 查看性能指标
        """
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    parser.add_argument(
        "--config",
        "-c",
        help="配置文件路径"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="启用调试模式"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # init 命令
    init_parser = subparsers.add_parser("init", help="初始化配置")
    init_parser.add_argument("--db-path", help="数据库路径")
    init_parser.add_argument("--embedding-provider", default="dashscope")
    
    # memory 命令
    memory_parser = subparsers.add_parser("memory", help="记忆管理")
    memory_sub = memory_parser.add_subparsers(dest="memory_cmd")
    
    # memory add
    memory_add_cmd = memory_sub.add_parser("add", help="添加记忆")
    memory_add_cmd.add_argument("content", help="记忆内容")
    memory_add_cmd.add_argument("--type", default="session", help="记忆类型")
    memory_add_cmd.add_argument("--scope", default="global", help="作用域")
    
    # memory search
    memory_search_cmd = memory_sub.add_parser("search", help="搜索记忆")
    memory_search_cmd.add_argument("query", help="查询文本")
    memory_search_cmd.add_argument("--top-k", type=int, default=5)
    memory_search_cmd.add_argument("--scope", default="all")
    
    # memory stats
    memory_sub.add_parser("stats", help="记忆统计")
    
    # project 命令
    project_parser = subparsers.add_parser("project", help="项目管理")
    project_sub = project_parser.add_subparsers(dest="project_cmd")
    
    # project create
    project_create_cmd = project_sub.add_parser("create", help="创建项目")
    project_create_cmd.add_argument("name", help="项目名称")
    project_create_cmd.add_argument("--description", "-d", default="")
    project_create_cmd.add_argument("--path", default="")
    
    # project list
    project_sub.add_parser("list", help="列出项目")
    
    # project search
    project_search_cmd = project_sub.add_parser("search", help="搜索项目")
    project_search_cmd.add_argument("query", help="查询文本")
    project_search_cmd.add_argument("--project", "-p", help="限定项目")
    project_search_cmd.add_argument("--top-k", type=int, default=5)
    
    # project delete
    project_delete_cmd = project_sub.add_parser("delete", help="删除项目")
    project_delete_cmd.add_argument("name", help="项目名称")
    project_delete_cmd.add_argument("--force", action="store_true")
    
    # query 命令
    query_parser = subparsers.add_parser("query", help="智能查询")
    query_parser.add_argument("text", help="查询文本")
    query_parser.add_argument("--top-k", type=int, default=5)
    
    # stats 命令
    subparsers.add_parser("stats", help="查看统计")
    
    # metrics 命令
    subparsers.add_parser("metrics", help="查看性能指标")
    
    return parser


async def handle_init(args):
    """处理 init 命令"""
    config = init_config(
        db_path=args.db_path,
        embedding_provider=args.embedding_provider,
        debug=args.debug
    )
    
    # 保存配置
    config_file = Path.home() / ".copaw" / "openmembase.json"
    config.to_file(str(config_file))
    
    print(f"✅ 配置已初始化")
    print(f"   数据库路径: {config.db_path}")
    print(f"   Embedding: {config.embedding.provider}")
    print(f"   配置文件: {config_file}")


async def handle_memory_add(args):
    """处理 memory add 命令"""
    memory_id = await memory_add(
        content=args.content,
        memory_type=args.type,
        metadata={"scope": args.scope}
    )
    print(f"✅ 记忆已添加: {memory_id}")


async def handle_memory_search(args):
    """处理 memory search 命令"""
    results = await memory_search(
        query=args.query,
        top_k=args.top_k,
        scope=args.scope
    )
    
    print(f"找到 {len(results)} 条记忆:")
    for i, r in enumerate(results, 1):
        print(f"\n{i}. [{r.get('score', 0):.3f}] {r['content'][:100]}...")


async def handle_memory_stats(args):
    """处理 memory stats 命令"""
    stats = await memory_stats()
    print("记忆统计:")
    print(f"  总记忆数: {stats.get('total_memories', 0)}")
    print(f"  类型分布: {stats.get('type_distribution', {})}")


async def handle_project_create(args):
    """处理 project create 命令"""
    project_id = await project_create(
        name=args.name,
        description=args.description,
        path=args.path
    )
    print(f"✅ 项目已创建: {project_id}")


async def handle_project_list(args):
    """处理 project list 命令"""
    projects = await project_list()
    print(f"共有 {len(projects)} 个项目:")
    for p in projects:
        print(f"  - {p['name']}: {p.get('description', 'N/A')}")


async def handle_project_search(args):
    """处理 project search 命令"""
    results = await project_search(
        query=args.query,
        project_name=args.project,
        top_k=args.top_k
    )
    
    print(f"找到 {len(results)} 条结果:")
    for i, r in enumerate(results, 1):
        print(f"\n{i}. [{r.get('score', 0):.3f}] {r.get('name', 'Unknown')}")
        print(f"   {r.get('content', '')[:150]}...")


async def handle_project_delete(args):
    """处理 project delete 命令"""
    if not args.force:
        confirm = input(f"确认删除项目 '{args.name}'? [y/N]: ")
        if confirm.lower() != 'y':
            print("已取消")
            return
    
    success = await project_delete(args.name)
    if success:
        print(f"✅ 项目已删除: {args.name}")
    else:
        print(f"❌ 删除失败: {args.name}")


async def handle_query(args):
    """处理 query 命令"""
    result = await smart_query(args.text, top_k=args.top_k)
    
    print(f"查询: {result['query']}")
    print(f"类型: {result['query_type']}")
    print(f"耗时: {result['metadata']['search_time_ms']}ms")
    print(f"\n找到 {len(result['results'])} 条结果:")
    
    for i, r in enumerate(result['results'], 1):
        source = r.get('source', 'unknown')
        print(f"\n{i}. [{source}] {r.get('content', '')[:100]}...")


async def handle_stats(args):
    """处理 stats 命令"""
    omb = get_openmembase()
    stats = await omb.stats()
    
    print("OpenMemBase 统计:")
    print(f"\n记忆:")
    print(f"  总数: {stats['memory']['count']}")
    print(f"  类型: {stats['memory']['types']}")
    print(f"\n项目:")
    print(f"  项目数: {stats['projects']['count']}")
    print(f"  资源数: {stats['projects']['total_resources']}")
    print(f"\n数据库: {stats['database_path']}")


def handle_metrics(args):
    """处理 metrics 命令"""
    print_metrics()


async def main():
    """主函数"""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 初始化日志
    init_logger(
        level="DEBUG" if args.debug else "INFO",
        log_dir=Path.home() / ".copaw" / "logs"
    )
    
    # 加载配置
    if args.config:
        from openmembase.config import OpenMemBaseConfig
        config = OpenMemBaseConfig.from_file(args.config)
    else:
        config = get_config()
    
    if args.debug:
        config.debug = True
    
    # 处理命令
    try:
        if args.command == "init":
            await handle_init(args)
        elif args.command == "memory":
            if args.memory_cmd == "add":
                await handle_memory_add(args)
            elif args.memory_cmd == "search":
                await handle_memory_search(args)
            elif args.memory_cmd == "stats":
                await handle_memory_stats(args)
            else:
                parser.parse_args(["memory", "--help"])
        elif args.command == "project":
            if args.project_cmd == "create":
                await handle_project_create(args)
            elif args.project_cmd == "list":
                await handle_project_list(args)
            elif args.project_cmd == "search":
                await handle_project_search(args)
            elif args.project_cmd == "delete":
                await handle_project_delete(args)
            else:
                parser.parse_args(["project", "--help"])
        elif args.command == "query":
            await handle_query(args)
        elif args.command == "stats":
            await handle_stats(args)
        elif args.command == "metrics":
            handle_metrics(args)
    except Exception as e:
        print(f"❌ 错误: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def cli_main():
    """CLI 入口"""
    asyncio.run(main())


if __name__ == "__main__":
    cli_main()
