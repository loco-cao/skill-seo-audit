#!/usr/bin/env python3
"""
Google Search Console API Client

免费，需要 OAuth 2.0 授权或 Service Account。
获取：搜索查询数据、索引覆盖率、CWV 字段数据、外链列表。

使用方法:
    # 1. 先到 Google Cloud Console 创建 OAuth 凭证，下载 client_secret.json
    # 2. 第一次运行会弹出浏览器授权，生成 token.json
    # 3. 之后自动使用 token.json

    python scripts/gsc.py --site https://example.com/ --days 28

功能:
    --queries     获取搜索查询数据（展示、点击、CTR、排名）
    --coverage    获取索引覆盖率（已索引/未索引/排除）
    --links       获取外链数据（Google 提供的外链列表）
    --cwv         获取 Core Web Vitals 报告

所需包:
    pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta

# Google API 客户端
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
except ImportError:
    print("请先安装依赖: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    sys.exit(1)

# OAuth 范围
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "config", "gsc_credentials.json")
TOKEN_FILE = os.path.join(os.path.dirname(__file__), "config", "gsc_token.json")


def get_service():
    """获取已授权的 GSC API service。"""
    creds = None

    # 尝试加载已有 token
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # 如果没有有效凭证，启动 OAuth 流程
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                print(f"错误: 未找到凭证文件 {CREDENTIALS_FILE}")
                print("请到 Google Cloud Console 下载 OAuth client_secret.json 并重命名为 gsc_credentials.json")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        # 保存 token 供下次使用
        os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return build("webmasters", "v3", credentials=creds, cache_discovery=False)


def get_search_queries(service, site_url: str, days: int = 28):
    """获取搜索查询数据：展示、点击、CTR、平均排名。"""
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    request = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": ["query"],
        "rowLimit": 100,
    }

    response = service.searchanalytics().query(siteUrl=site_url, body=request).execute()
    rows = response.get("rows", [])

    queries = []
    for row in rows:
        queries.append({
            "query": row["keys"][0],
            "clicks": row.get("clicks", 0),
            "impressions": row.get("impressions", 0),
            "ctr": round(row.get("ctr", 0) * 100, 2),
            "position": round(row.get("position", 0), 1),
        })

    return {
        "period": f"{start_date} to {end_date}",
        "totalQueries": len(queries),
        "queries": queries,
    }


def get_index_coverage(service, site_url: str):
    """获取索引覆盖率：已索引、未索引、排除页面。"""
    response = service.sites().get(siteUrl=site_url).execute()
    permission = response.get("permissionLevel", "unknown")

    # 注意：GSC API v3 不直接提供 coverage 数据，需要用户通过 GSC 界面查看
    # 这里返回站点权限信息，实际 coverage 数据建议通过 Search Console 界面导出
    return {
        "siteUrl": site_url,
        "permissionLevel": permission,
        "note": "详细的索引覆盖率（已索引/未索引/排除）请通过 GSC 界面导出 CSV 后提供给 skill 分析。",
    }


def get_links(service, site_url: str):
    """获取 Google 发现的外链数据。"""
    response = service.links().list(siteUrl=site_url).execute()
    external = response.get("externalLinks", [])

    links = []
    for link in external[:100]:  # 限制前 100 条
        links.append({
            "sourceUrl": link.get("source", {}).get("url"),
            "targetUrl": link.get("target", {}).get("url"),
            "type": link.get("type"),
        })

    return {
        "totalExternalLinks": len(external),
        "sampleLinks": links,
    }


def main():
    parser = argparse.ArgumentParser(description="Google Search Console API Client")
    parser.add_argument("--site", required=True, help="站点 URL，如 https://example.com/")
    parser.add_argument("--days", type=int, default=28, help="查询天数（默认 28）")
    parser.add_argument("--queries", action="store_true", help="获取搜索查询数据")
    parser.add_argument("--coverage", action="store_true", help="获取索引覆盖率")
    parser.add_argument("--links", action="store_true", help="获取外链数据")
    parser.add_argument("--all", action="store_true", help="获取所有数据")

    args = parser.parse_args()

    if not any([args.queries, args.coverage, args.links, args.all]):
        parser.print_help()
        sys.exit(1)

    try:
        service = get_service()
        result = {"siteUrl": args.site}

        if args.all or args.queries:
            result["searchQueries"] = get_search_queries(service, args.site, args.days)

        if args.all or args.coverage:
            result["indexCoverage"] = get_index_coverage(service, args.site)

        if args.all or args.links:
            result["links"] = get_links(service, args.site)

        print(json.dumps(result, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
