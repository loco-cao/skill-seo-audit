#!/usr/bin/env python3
"""
PageSpeed Insights API Client

完全免费，只需 Google Cloud API Key（无需 OAuth）。
获取 Core Web Vitals 字段数据（真实用户）+ Lighthouse 实验室数据。

使用方法:
    python scripts/pagespeed.py https://example.com YOUR_API_KEY

API Key 获取: https://developers.google.com/speed/docs/insights/v5/get-started
"""

import sys
import json
import requests

ENDPOINT = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"


def run_pagespeed(url: str, api_key: str = "", strategy: str = "mobile") -> dict:
    """调用 PageSpeed Insights API，返回结构化的 CWV + Lighthouse 数据。"""
    params = {
        "url": url,
        "strategy": strategy,
        "category": "PERFORMANCE,SEO,ACCESSIBILITY,BEST_PRACTICES",
    }
    if api_key:
        params["key"] = api_key

    resp = requests.get(ENDPOINT, params=params, timeout=30)
    resp.raise_for_status()
    return parse_result(resp.json())


def parse_result(data: dict) -> dict:
    """解析 PSI API 返回的原始 JSON。"""
    result = {
        "url": data.get("id"),
        "strategy": data.get("analysisUTCTimestamp", ""),
    }

    # 字段数据：Chrome User Experience Report（真实用户）
    metrics = data.get("loadingExperience", {}).get("metrics", {})
    result["fieldData"] = {
        "LCP": extract_metric(metrics.get("LARGEST_CONTENTFUL_PAINT_MS")),
        "INP": extract_metric(metrics.get("INTERACTION_TO_NEXT_PAINT")),
        "CLS": extract_metric(metrics.get("CUMULATIVE_LAYOUT_SHIFT_SCORE")),
        "FCP": extract_metric(metrics.get("FIRST_CONTENTFUL_PAINT_MS")),
        "TTFB": extract_metric(metrics.get("EXPERIMENTAL_TIME_TO_FIRST_BYTE")),
        "overallCategory": data.get("loadingExperience", {}).get("overall_category"),
    }

    # 实验室数据：Lighthouse
    lh = data.get("lighthouseResult")
    if lh:
        cats = lh.get("categories", {})
        result["labData"] = {
            "performanceScore": to_100(cats.get("performance", {}).get("score")),
            "seoScore": to_100(cats.get("seo", {}).get("score")),
            "accessibilityScore": to_100(cats.get("accessibility", {}).get("score")),
            "bestPracticesScore": to_100(cats.get("best-practices", {}).get("score")),
            "audits": extract_audits(lh.get("audits", {})),
        }

    return result


def extract_metric(m):
    if not m:
        return None
    return {
        "value": m.get("percentile") if m.get("percentile") is not None else m.get("numericValue"),
        "unit": m.get("numericUnit"),
        "category": m.get("category"),
    }


def to_100(score):
    return round(score * 100) if score is not None else None


def extract_audits(audits: dict) -> dict:
    keys = [
        "largest-contentful-paint",
        "total-blocking-time",
        "cumulative-layout-shift",
        "server-response-time",
        "redirects",
        "unused-javascript",
        "unused-css-rules",
        "modern-image-formats",
        "render-blocking-resources",
        "uses-long-cache-ttl",
    ]
    extracted = {}
    for key in keys:
        a = audits.get(key)
        if a:
            extracted[key] = {
                "score": a.get("score"),
                "displayValue": a.get("displayValue"),
                "title": a.get("title"),
            }
    return extracted


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/pagespeed.py <URL> [API_KEY] [mobile|desktop]")
        sys.exit(1)

    url = sys.argv[1]
    api_key = sys.argv[2] if len(sys.argv) > 2 else ""
    strategy = sys.argv[3] if len(sys.argv) > 3 else "mobile"

    try:
        data = run_pagespeed(url, api_key, strategy)
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except requests.HTTPError as e:
        print(f"API Error: {e.response.status_code} - {e.response.text}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
