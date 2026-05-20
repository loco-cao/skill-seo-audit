#!/usr/bin/env python3
"""
Google Analytics 4 Data API Client

免费，需要 OAuth 2.0 授权。
获取：页面互动率、平均互动时长、用户行为路径、流量来源。

使用方法:
    # 1. 到 Google Cloud Console 启用 GA4 Data API，下载 OAuth 凭证
    # 2. 将凭证保存为 scripts/config/ga4_credentials.json
    # 3. 运行:

    python scripts/ga4.py --property 123456789 --days 28

所需包:
    pip install google-analytics-data google-auth google-auth-oauthlib

注意:
    GA4 Property ID 是纯数字（如 123456789），在 GA4 设置中查看。
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta

try:
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import (
        RunReportRequest,
        DateRange,
        Dimension,
        Metric,
    )
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
except ImportError:
    print("请先安装依赖: pip install google-analytics-data google-auth google-auth-oauthlib")
    sys.exit(1)

SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), "config", "ga4_credentials.json")
TOKEN_FILE = os.path.join(os.path.dirname(__file__), "config", "ga4_token.json")


def get_client():
    """获取已授权的 GA4 Data API client。"""
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                print(f"错误: 未找到凭证文件 {CREDENTIALS_FILE}")
                print("请到 Google Cloud Console 下载 OAuth 凭证并重命名为 ga4_credentials.json")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return BetaAnalyticsDataClient(credentials=creds)


def run_report(client, property_id: str, days: int = 28):
    """获取核心行为指标。"""
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    request = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        dimensions=[
            Dimension(name="pageTitle"),
            Dimension(name="pagePath"),
        ],
        metrics=[
            Metric(name="sessions"),
            Metric(name="engagementRate"),
            Metric(name="averageEngagementTimePerSession"),
            Metric(name="bounceRate"),
            Metric(name="newUsers"),
            Metric(name="screenPageViews"),
        ],
        limit=100,
    )

    response = client.run_report(request)

    pages = []
    for row in response.rows:
        pages.append({
            "pageTitle": row.dimension_values[0].value,
            "pagePath": row.dimension_values[1].value,
            "sessions": int(row.metric_values[0].value),
            "engagementRate": round(float(row.metric_values[1].value) * 100, 2),
            "avgEngagementTimeSec": round(float(row.metric_values[2].value), 1),
            "bounceRate": round(float(row.metric_values[3].value) * 100, 2),
            "newUsers": int(row.metric_values[4].value),
            "pageViews": int(row.metric_values[5].value),
        })

    return {
        "propertyId": property_id,
        "period": f"{start_date} to {end_date}",
        "totalPages": len(pages),
        "pages": pages,
    }


def get_traffic_sources(client, property_id: str, days: int = 28):
    """获取流量来源分布。"""
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    request = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
        dimensions=[Dimension(name="sessionDefaultChannelGroup")],
        metrics=[
            Metric(name="sessions"),
            Metric(name="engagementRate"),
        ],
    )

    response = client.run_report(request)

    sources = []
    for row in response.rows:
        sources.append({
            "channel": row.dimension_values[0].value,
            "sessions": int(row.metric_values[0].value),
            "engagementRate": round(float(row.metric_values[1].value) * 100, 2),
        })

    return {
        "period": f"{start_date} to {end_date}",
        "sources": sources,
    }


def main():
    parser = argparse.ArgumentParser(description="Google Analytics 4 Data API Client")
    parser.add_argument("--property", required=True, help="GA4 Property ID（纯数字）")
    parser.add_argument("--days", type=int, default=28, help="查询天数（默认 28）")
    parser.add_argument("--traffic", action="store_true", help="获取流量来源")
    parser.add_argument("--all", action="store_true", help="获取所有数据")

    args = parser.parse_args()

    try:
        client = get_client()
        result = {"propertyId": args.property}

        if args.all or not args.traffic:
            result["pageMetrics"] = run_report(client, args.property, args.days)

        if args.all or args.traffic:
            result["trafficSources"] = get_traffic_sources(client, args.property, args.days)

        print(json.dumps(result, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
