# API Integration Guide

> 说明 seo-audit skill 如何接入第三方免费 API 来增强审计数据。
> 所有脚本位于 `scripts/` 目录，Agent 执行审计时通过 Bash 调用。

---

## 概述

纯页面扫描能发现代码层面的 SEO 问题，但无法获取**真实用户数据**和**Google 官方指标**。
通过接入以下免费 API，审计从"代码检查"升级为"数据驱动的权威审计"：

| API | 获取的数据 | 替代/增强的 Expert |
|-----|-----------|-------------------|
| **PageSpeed Insights** | 真实用户 CWV（LCP/INP/CLS）、Lighthouse 分数 | `seo-core-web-vitals-expert` |
| **Google Search Console** | 搜索查询（CTR/排名）、外链列表、索引状态 | `seo-crawlability-expert`、`seo-indexability-expert` |
| **Google Analytics 4** | 页面互动率、平均停留时间、流量来源 | `seo-content-expert`、`seo-ux-expert` |
| **Google Trends** | 品牌/关键词搜索热度趋势 | `seo-eeat-expert`（品牌信号辅助） |

---

## PageSpeed Insights API

### 脚本

```bash
node scripts/pagespeed.js <URL> [API_KEY] [mobile|desktop]
```

### 认证配置

1. 到 [Google Cloud Console](https://console.cloud.google.com/apis/credentials) 创建 API Key
2. 启用 **PageSpeed Insights API**
3. 无需 OAuth，直接 URL 传参

### 返回数据结构

```json
{
  "url": "https://example.com/",
  "fieldData": {
    "LCP": { "value": 1200, "unit": "ms", "category": "FAST" },
    "INP": { "value": 120, "unit": "ms", "category": "FAST" },
    "CLS": { "value": 0.05, "unit": "unitless", "category": "FAST" },
    "FCP": { "value": 900, "unit": "ms", "category": "FAST" },
    "TTFB": { "value": 400, "unit": "ms", "category": "FAST" },
    "overallCategory": "FAST"
  },
  "labData": {
    "performanceScore": 95,
    "seoScore": 92,
    "accessibilityScore": 88,
    "bestPracticesScore": 90,
    "audits": {
      "largest-contentful-paint": { "score": 1, "displayValue": "1.2 s" },
      "cumulative-layout-shift": { "score": 1, "displayValue": "0.05" }
    }
  }
}
```

### 数据解读

- **`fieldData`**：来自 Chrome User Experience Report（真实用户数据），**最权威**
  - `category` 为 `FAST`/`AVERAGE`/`SLOW`，直接对应评分
  - LCP < 2500ms = FAST；2500-4000ms = AVERAGE；> 4000ms = SLOW
  - INP < 200ms = FAST；200-500ms = AVERAGE；> 500ms = SLOW
  - CLS < 0.1 = FAST；0.1-0.25 = AVERAGE；> 0.25 = SLOW
- **`labData.performanceScore`**：Lighthouse 实验室分数（0-100）
- **`labData.seoScore`**：Lighthouse SEO 审计分数

### Expert 使用方式

`seo-core-web-vitals-expert` 审计时：
1. 先执行 `node scripts/pagespeed.js <URL> <API_KEY>`
2. 读取返回的 JSON
3. 用 `fieldData` 替代 AI 推断的 CWV 数据，直接评分
4. 用 `labData.audits` 补充具体的性能优化建议

---

## Google Search Console API

### 脚本

```bash
node scripts/gsc.js --site https://example.com/ [--queries] [--links] [--all] [--days 28]
```

### 认证配置（Service Account）

**为什么用 Service Account 而不是 OAuth：**
- 不需要浏览器弹窗授权
- 不需要 `google-auth` npm 包
- 脚本用 Node.js 内置 `crypto` 做 RSA-SHA256 签名生成 JWT

**配置步骤：**

1. **Google Cloud Console** → IAM & Admin → Service Accounts → Create
2. 下载 JSON 密钥，保存为 `scripts/config/gsc_service_account.json`
3. 打开 GSC（Search Console）→ 设置 → 用户和权限 → 添加用户
4. 把 Service Account 的 `client_email`（如 `xxx@project.iam.gserviceaccount.com`）添加为**拥有者**或**完整权限**
5. 在 Cloud Console 启用 **Google Search Console API**

### 返回数据结构

```json
{
  "siteUrl": "https://example.com/",
  "searchQueries": {
    "period": "2026-04-21 to 2026-05-19",
    "totalQueries": 42,
    "queries": [
      {
        "query": "seo audit tool",
        "clicks": 156,
        "impressions": 3200,
        "ctr": 4.88,
        "position": 8.2
      }
    ]
  },
  "links": {
    "totalExternalLinks": 245,
    "sampleLinks": [
      { "sourceUrl": "https://example-blog.com/post", "targetUrl": "https://example.com/", "type": "EXTERNAL" }
    ]
  }
}
```

### 数据解读

- **`searchQueries`**：用户通过哪些搜索词找到网站
  - `ctr` < 3%：标题/description 可能需要优化（排名高但点击少）
  - `position` > 10：关键词排名在第二页以后，需要内容优化
  - `impressions` 高但 `clicks` 低：SERP 展示吸引力不足
- **`links`**：Google 发现的外链列表
  - 数量趋势比绝对值更重要
  - 注意外链来源的质量（是否来自相关/权威站点）

### Expert 使用方式

- `seo-crawlability-expert`：用 `links` 数据补充外链健康度分析
- `seo-content-expert`：用 `searchQueries` 验证内容是否匹配用户搜索意图
- `seo-meta-expert`：用 `ctr` 低的查询词定位需要优化的 title/description

---

## Google Analytics 4 Data API

### 脚本

```bash
node scripts/ga4.js --property 123456789 [--days 28] [--traffic] [--all]
```

### 认证配置（Service Account）

1. 到 Google Cloud Console 创建 Service Account（可与 GSC 共用，但建议分开）
2. 下载 JSON 密钥，保存为 `scripts/config/ga4_service_account.json`
3. GA4 后台 → 管理 → 账号访问管理 → 添加用户
4. 把 Service Account 邮箱添加为**查看者**或**分析师**
5. 在 Cloud Console 启用 **Google Analytics Data API**

### 返回数据结构

```json
{
  "propertyId": "123456789",
  "pageMetrics": {
    "period": "2026-04-21 to 2026-05-19",
    "totalPages": 87,
    "pages": [
      {
        "pageTitle": "首页",
        "pagePath": "/",
        "sessions": 5230,
        "engagementRate": 68.5,
        "avgEngagementTimeSec": 145.2,
        "bounceRate": 31.5,
        "newUsers": 2100,
        "pageViews": 8900
      }
    ]
  },
  "trafficSources": {
    "period": "2026-04-21 to 2026-05-19",
    "sources": [
      { "channel": "Organic Search", "sessions": 4200, "engagementRate": 72.1 },
      { "channel": "Direct", "sessions": 1800, "engagementRate": 65.3 }
    ]
  }
}
```

### 数据解读

- **`engagementRate`**（互动率）：GA4 替代"跳出率"的核心指标
  - > 60%：良好
  - 40-60%：一般
  - < 40%：需要优化内容和用户体验
- **`avgEngagementTimeSec`**：平均互动时长
  - > 120 秒：内容吸引力强
  - < 30 秒：可能存在内容不匹配或加载问题
- **`bounceRate`**：跳出率（GA4 保留的兼容指标）
  - < 40%：良好；40-60%：一般；> 60%：需优化
- **`trafficSources`**：流量来源分布
  - Organic Search 占比 < 30%：SEO 流量基础薄弱

### Expert 使用方式

- `seo-content-expert`：用 `engagementRate` 和 `avgEngagementTimeSec` 验证内容质量
- `seo-ux-expert`：用 `bounceRate` 和页面级数据定位体验问题
- `seo-eeat-expert`：用 `trafficSources` 中的 Direct 流量比例推断品牌认知度

---

## Google Trends（pytrends）

### 脚本

```bash
python scripts/trends.py --keywords "品牌A,品牌B,竞品C" --region CN --days 90 [--related]
```

### 依赖

```bash
pip install pytrends
```

### 返回数据结构

```json
{
  "interestOverTime": {
    "keywords": ["品牌A", "品牌B"],
    "region": "CN",
    "averageInterest": {
      "品牌A": 45.2,
      "品牌B": 78.5
    },
    "dataPoints": [
      { "date": "2026-02-19", "品牌A": 40, "品牌B": 75 }
    ]
  },
  "relatedQueries": {
    "品牌A": {
      "rising": [{ "query": "品牌A 怎么样", "value": 120 }],
      "top": [{ "query": "品牌A 官网", "value": 100 }]
    }
  }
}
```

### 数据解读

- `averageInterest`：相对热度（0-100），用于品牌对比
- `rising`：近期搜索量快速增长的相关查询（发现新机会）
- 每次最多 5 个关键词（Google Trends 限制）

### Expert 使用方式

- `seo-eeat-expert`：用品牌搜索趋势验证品牌权威性信号
- `seo-content-expert`：用 `relatedQueries.rising` 发现新的内容主题机会

---

## Agent 执行流程（统一模式）

所有接入 API 的 expert 遵循以下执行流程：

```
1. 检查认证文件是否存在
   - PSI: 检查 API Key 是否通过参数传入
   - GSC: 检查 scripts/config/gsc_service_account.json
   - GA4: 检查 scripts/config/ga4_service_account.json

2. 若认证就绪 → 运行对应脚本获取数据
   若认证缺失 → 跳过 API 数据，降级为纯页面扫描模式

3. 读取脚本返回的 JSON

4. 结合 reference 中的评分标准进行审计

5. 生成 report.json（包含 API 数据字段）
```

### 降级策略

**不要因为 API 认证缺失而阻塞审计。**

- PSI API Key 缺失 → 用 AI 推断 CWV（从 HTML/资源分析推断）
- GSC Service Account 缺失 → 跳过搜索查询和外链数据
- GA4 Service Account 缺失 → 跳过用户行为数据
- Trends 未安装 → 跳过品牌趋势分析

---

## 认证文件清单

```
scripts/config/
├── gsc_service_account.json      # GSC Service Account 密钥
├── ga4_service_account.json      # GA4 Service Account 密钥
└── .gitignore                    # 确保密钥文件不提交到 Git
```

**`.gitignore` 内容：**

```
# API 密钥和认证文件（绝不提交到 Git）
scripts/config/*.json
scripts/config/*.token
```

---

## 成本总结

| API | 费用 | 限制 |
|-----|------|------|
| PageSpeed Insights | 免费 | 每日 25,000 次查询（足够） |
| Google Search Console | 免费 | 无明确限制（Service Account） |
| Google Analytics 4 Data | 免费 | 无明确限制（Service Account） |
| Google Trends (pytrends) | 免费 | 请求频率限制（建议间隔 1-2 秒） |

**总计：$0/月**，只需一次性配置 Service Account。
