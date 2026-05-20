#!/usr/bin/env node
/**
 * PageSpeed Insights API Client — 零依赖 Node.js 版本
 *
 * 完全免费，只需 Google Cloud API Key（无需 OAuth）。
 * 获取 Core Web Vitals 字段数据（真实用户）+ Lighthouse 实验室数据。
 *
 * 使用方法:
 *   node scripts/pagespeed.js https://example.com YOUR_API_KEY
 *
 * API Key 获取: https://developers.google.com/speed/docs/insights/v5/get-started
 */

const ENDPOINT = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed";

async function runPageSpeed(url, apiKey, strategy = "mobile") {
  const params = new URLSearchParams({
    url,
    strategy,
    category: "PERFORMANCE,SEO,ACCESSIBILITY,BEST_PRACTICES",
  });
  if (apiKey) params.set("key", apiKey);

  const res = await fetch(`${ENDPOINT}?${params}`, { method: "GET" });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(`PSI API ${res.status}: ${err.error?.message || res.statusText}`);
  }
  return parseResult(await res.json());
}

function parseResult(data) {
  const result = { url: data.id };

  // 字段数据：Chrome User Experience Report（真实用户）
  const metrics = data.loadingExperience?.metrics || {};
  result.fieldData = {
    LCP: extractMetric(metrics.LARGEST_CONTENTFUL_PAINT_MS),
    INP: extractMetric(metrics.INTERACTION_TO_NEXT_PAINT),
    CLS: extractMetric(metrics.CUMULATIVE_LAYOUT_SHIFT_SCORE),
    FCP: extractMetric(metrics.FIRST_CONTENTFUL_PAINT_MS),
    TTFB: extractMetric(metrics.EXPERIMENTAL_TIME_TO_FIRST_BYTE),
    overallCategory: data.loadingExperience?.overall_category,
  };

  // 实验室数据：Lighthouse
  const lh = data.lighthouseResult;
  if (lh) {
    const cats = lh.categories || {};
    result.labData = {
      performanceScore: to100(cats.performance?.score),
      seoScore: to100(cats.seo?.score),
      accessibilityScore: to100(cats.accessibility?.score),
      bestPracticesScore: to100(cats["best-practices"]?.score),
      audits: extractAudits(lh.audits || {}),
    };
  }

  return result;
}

function extractMetric(m) {
  if (!m) return null;
  return {
    value: m.percentile ?? m.numericValue,
    unit: m.numericUnit,
    category: m.category,
  };
}

function to100(score) {
  return score != null ? Math.round(score * 100) : null;
}

function extractAudits(audits) {
  const keys = [
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
  ];
  const extracted = {};
  for (const key of keys) {
    const a = audits[key];
    if (a) {
      extracted[key] = {
        score: a.score,
        displayValue: a.displayValue,
        title: a.title,
      };
    }
  }
  return extracted;
}

// CLI
const [,, url, apiKey, strategy] = process.argv;
if (!url) {
  console.error("Usage: node scripts/pagespeed.js <URL> [API_KEY] [mobile|desktop]");
  process.exit(1);
}

runPageSpeed(url, apiKey || "", strategy || "mobile")
  .then(d => console.log(JSON.stringify(d, null, 2)))
  .catch(e => {
    console.error("Error:", e.message);
    process.exit(1);
  });
