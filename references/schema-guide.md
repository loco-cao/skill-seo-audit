# Structured Data Guide

> 供 `seo-schema-expert` 执行审计时参考。

---

## 角色定位

验证页面是否正确使用结构化数据标记，帮助搜索引擎理解内容语义并获取富媒体摘要（Rich Snippets）。结构化数据虽不直接影响排名，但能显著提升搜索结果点击率（CTR）。

---

## 排名因素关联

- **Schema 结构化数据**（Tier 2，第 11 位）：虽不直接影响排名，但能获取富媒体摘要，提升 CTR
- **内容格式**（Tier 3）：列表、表格、FAQ 等格式有助于获取 Featured Snippet

---

## 评估维度

### 1. JSON-LD 存在性

- 页面是否包含 JSON-LD 格式的结构化数据
- 是否放在 `<head>` 或 `<body>` 中（推荐 `<head>`）
- 是否使用内联 JSON-LD（推荐）而非 Microdata/RDFa

### 2. Schema.org 类型正确性

- 类型选择是否与页面内容匹配：
  - 首页/品牌 → `Organization` 或 `WebSite`
  - 文章/博客 → `Article` 或 `BlogPosting`
  - 产品页 → `Product`（含 `Offer`、`Review`）
  - 食谱 → `Recipe`
  - 事件 → `Event`
  - 常见问题 → `FAQPage`
  - 面包屑 → `BreadcrumbList`
- 必填属性是否完整
- 属性值是否准确（如价格、日期格式）

### 3. Rich Snippets 资格

- 是否具备以下富媒体展示资格：
  - 评分星级（`AggregateRating`）
  - 面包屑路径（`BreadcrumbList`）
  - FAQ 折叠面板（`FAQPage`）
  - 搜索框（`WebSite` + `potentialAction`）
  - 产品价格/库存（`Product` + `Offer`）

### 4. Open Graph 标签

- `og:title`、`og:description`、`og:image` 是否完整
- `og:url` 是否为规范 URL
- `og:type` 是否正确
- `og:image` 尺寸是否符合推荐（1200×630px）

### 5. Twitter Cards

- `twitter:card` 类型是否正确（`summary`、`summary_large_image`）
- `twitter:title`、`twitter:description`、`twitter:image` 是否配置

### 6. 结构化数据验证

- 数据是否通过 Google 富媒体测试工具（Rich Results Test）
- 是否存在语法错误（如缺少逗号、引号不匹配）
- 是否存在警告（非阻塞但建议修复）

---

## 评分指南

| 分数 | 等级 | 说明 |
|------|------|------|
| 90–100 | 优秀 | JSON-LD 完整、Schema 类型正确、Rich Snippets 资格充分、OG/Twitter 配置齐全、验证通过 |
| 70–89 | 良好 | 轻微问题：部分页面缺少结构化数据、个别属性值不准确、OG 标签部分缺失 |
| 60–69 | 有风险 | 大量页面无结构化数据、Schema 类型错误、富媒体测试有大量警告 |
| 0–59 | 严重 | 完全无结构化数据、JSON-LD 语法错误严重、Schema 类型完全不匹配 |
