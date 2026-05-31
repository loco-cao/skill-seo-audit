#!/usr/bin/env python3
"""
SEO Audit 知识库检索工具

在 references/ 目录中搜索关键词，快速定位相关审查指南和官方文档。
供审计入口点和各专家 agent 在执行审计时快速查找相关规范。

用法：
    python scripts/search_kb.py "关键词"
    python scripts/search_kb.py "canonical noindex"
    python scripts/search_kb.py --list              # 列出所有参考文档
    python scripts/search_kb.py "schema product" --max 10

来源：改编自 Google-SEOs.skill (MIT License)
"""

import os
import sys
import re
import argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

KB_ROOT = Path(__file__).resolve().parent.parent / "references"


def get_all_markdown_files():
    """收集 references/ 目录下所有 .md 文件"""
    results = []
    for category in sorted(KB_ROOT.iterdir()):
        if not category.is_dir():
            continue
        for file_path in category.glob("*.md"):
            results.append((category.name, file_path))
    return results


def search_file(category, file_path, keywords):
    """在单个文件中搜索多个关键词"""
    matches = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        filename_lower = file_path.name.lower()

        # 检查文件名匹配
        filename_match = False
        for kw in keywords:
            if kw.lower() in filename_lower:
                filename_match = True
                break

        # 检查内容匹配
        for i, line in enumerate(lines):
            line_lower = line.lower()
            for kw in keywords:
                if kw.lower() in line_lower:
                    # 提取上下文（±2 行）
                    start = max(0, i - 2)
                    end = min(len(lines), i + 3)
                    context = "".join(lines[start:end]).strip()

                    matches.append({
                        "line_num": i + 1,
                        "keyword": kw,
                        "context": context,
                    })
                    break  # 一行只记录一次

            if len(matches) >= 5:
                break

        return {
            "category": category,
            "file_path": str(file_path.relative_to(KB_ROOT)),
            "filename": file_path.name,
            "filename_match": filename_match,
            "matches": matches,
        }
    except Exception:
        return None


def search_kb(keywords):
    """并行搜索知识库"""
    all_files = get_all_markdown_files()

    if not all_files:
        print("错误: references/ 目录中未找到任何 .md 文件")
        sys.exit(1)

    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(search_file, cat, fp, keywords): (cat, fp)
            for cat, fp in all_files
        }
        for future in as_completed(futures):
            result = future.result()
            if result and result["matches"]:
                results.append(result)

    # 排序：文件名匹配优先，然后按匹配数降序
    results.sort(key=lambda r: (
        not r["filename_match"],
        -len(r["matches"]),
    ))

    return results


def list_categories():
    """列出所有知识库目录及文件"""
    print("\n  SEO Audit 知识库结构\n  " + "=" * 50)
    total_files = 0
    for category in sorted(KB_ROOT.iterdir()):
        if not category.is_dir():
            continue
        files = list(category.glob("*.md"))
        total_files += len(files)
        print(f"\n  [{category.name}] ({len(files)} 个文件)")
        for f in files[:5]:
            print(f"    - {f.name}")
        if len(files) > 5:
            print(f"    ... 还有 {len(files) - 5} 个文件")
    print(f"\n  {'=' * 50}")
    print(f"  总计: {total_files} 个参考文档")


def print_results(results, keywords, max_results=20):
    """格式化输出搜索结果"""
    kw_str = ", ".join(keywords)
    total_matches = sum(len(r["matches"]) for r in results)

    print(f"\n  搜索: {kw_str}")
    print(f"  找到 {len(results)} 个相关文件 (共 {total_matches} 处匹配)\n")

    shown = 0
    for result in results:
        if shown >= max_results:
            break

        icon = "\U0001F3AF" if result["filename_match"] else "\U0001F4C4"
        print(f"  {icon} [{result['category']}] {result['file_path']}")

        for m in result["matches"][:3]:
            print(f"     L{m['line_num']} [{m['keyword']}]:")
            for cl in m["context"].split("\n")[:3]:
                print(f"       | {cl[:100]}")
            print()

        shown += 1

    if len(results) > max_results:
        print(f"  ... 还有 {len(results) - max_results} 个结果未显示 "
              f"(使用 --max 调整上限)")

    print(f"\n  共 {total_matches} 处匹配，显示 {min(shown, max_results)} 个文件")


def main():
    parser = argparse.ArgumentParser(
        description="SEO Audit 知识库检索工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/search_kb.py "canonical"
  python scripts/search_kb.py "structured data product"
  python scripts/search_kb.py --list
  python scripts/search_kb.py "核心网页指标" --max 10
        """,
    )
    parser.add_argument(
        "keywords", nargs="?", default="",
        help="搜索关键词（支持多个，用空格分隔）"
    )
    parser.add_argument(
        "--list", "-l", action="store_true",
        help="列出所有参考文档目录结构"
    )
    parser.add_argument(
        "--max", "-m", type=int, default=20,
        help="最大显示结果数（默认 20）"
    )

    args = parser.parse_args()

    if args.list:
        list_categories()
        return

    if not args.keywords.strip():
        parser.print_help()
        print("\n提示: 请提供搜索关键词，或使用 --list 查看所有文档")
        sys.exit(1)

    keywords = [kw.strip().lower() for kw in args.keywords.split() if kw.strip()]
    if not keywords:
        print("错误: 请提供有效的搜索关键词")
        sys.exit(1)

    results = search_kb(keywords)
    if not results:
        print(f"\n  未找到与 \"{args.keywords}\" 相关的结果")
        print("  提示: 使用 --list 查看所有可用文档")
    else:
        print_results(results, keywords, args.max)


if __name__ == "__main__":
    main()