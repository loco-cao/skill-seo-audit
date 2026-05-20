#!/usr/bin/env python3
"""
Google Trends Client (via pytrends)

免费，非官方 API，但稳定可用。
获取品牌/关键词搜索量趋势，用于评估品牌信号和内容热度。

使用方法:
    python scripts/trends.py --keywords "品牌名,竞品A,竞品B" --region CN --days 90

所需包:
    pip install pytrends

注意:
    pytrends 使用 Google Trends 的内部接口，可能存在请求频率限制。
    建议每次查询间隔 1-2 秒，避免被封 IP。
"""

import sys
import json
import argparse
import time

try:
    from pytrends.request import TrendReq
except ImportError:
    print("请先安装依赖: pip install pytrends")
    sys.exit(1)


def get_interest_over_time(keywords: list, region: str = "", days: int = 90):
    """获取关键词搜索趋势（相对热度 0-100）。"""
    pytrends = TrendReq(hl="zh-CN", tz=480)

    # Google Trends 时间格式
    timeframe = f"today {days}-d"

    pytrends.build_payload(keywords, cat=0, timeframe=timeframe, geo=region)
    data = pytrends.interest_over_time()

    if data.empty:
        return {"error": "无数据返回，可能关键词搜索量过低或被封"}

    result = {
        "keywords": keywords,
        "region": region or "worldwide",
        "timeframe": timeframe,
        "isPartial": data.get("isPartial", [False]).iloc[-1] if "isPartial" in data.columns else False,
        "dataPoints": [],
    }

    for date, row in data.iterrows():
        point = {"date": date.strftime("%Y-%m-%d")}
        for kw in keywords:
            point[kw] = int(row[kw])
        result["dataPoints"].append(point)

    # 计算平均热度
    result["averageInterest"] = {}
    for kw in keywords:
        result["averageInterest"][kw] = round(float(data[kw].mean()), 1)

    return result


def get_related_queries(keywords: list, region: str = ""):
    """获取相关查询（上升和相关）。"""
    pytrends = TrendReq(hl="zh-CN", tz=480)
    pytrends.build_payload(keywords, cat=0, timeframe="today 12-m", geo=region)

    related = pytrends.related_queries()
    result = {}

    for kw in keywords:
        result[kw] = {
            "rising": [],
            "top": [],
        }
        if kw in related and related[kw]:
            if "rising" in related[kw] and related[kw]["rising"] is not None:
                df = related[kw]["rising"].head(10)
                for _, row in df.iterrows():
                    result[kw]["rising"].append({
                        "query": row["query"],
                        "value": int(row["value"]) if not isinstance(row["value"], str) else row["value"],
                    })
            if "top" in related[kw] and related[kw]["top"] is not None:
                df = related[kw]["top"].head(10)
                for _, row in df.iterrows():
                    result[kw]["top"].append({
                        "query": row["query"],
                        "value": int(row["value"]),
                    })

    return result


def main():
    parser = argparse.ArgumentParser(description="Google Trends Client")
    parser.add_argument("--keywords", required=True, help="关键词列表，逗号分隔，如: 品牌A,品牌B")
    parser.add_argument("--region", default="", help="地区代码，如 CN, US, JP（留空为全球）")
    parser.add_argument("--days", type=int, default=90, help="查询天数（默认 90）")
    parser.add_argument("--related", action="store_true", help="获取相关查询")

    args = parser.parse_args()

    keywords = [k.strip() for k in args.keywords.split(",")]
    if len(keywords) > 5:
        print("错误: 每次最多查询 5 个关键词（Google Trends 限制）")
        sys.exit(1)

    try:
        result = {
            "interestOverTime": get_interest_over_time(keywords, args.region, args.days),
        }

        if args.related:
            time.sleep(1)  # 避免频率限制
            result["relatedQueries"] = get_related_queries(keywords, args.region)

        print(json.dumps(result, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
