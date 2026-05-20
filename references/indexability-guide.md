# Indexability Guide

> 供 `seo-indexability-expert` 执行审计时参考。

---

## 角色定位

验证搜索引擎能否正确理解页面关系并将页面纳入索引。爬虫能抓到页面不代表页面会被索引——规范化、重复内容、noindex 等问题会直接阻止索引。

---

## Google 索引机制

| 环节 | 说明 | 审计要点 |
|------|------|---------|
| **规范化 (Canonicalization)** | 多个 URL 内容相似时，Google 选择"规范页面"作为代表 | 是否有 `<link rel="canonical">` 指明首选 URL；参数化 URL 是否导致重复内容 |
| **索引状态** | 页面可能被索引、未索引或被排除 | 关键页面是否可索引；不应索引的页面是否被误收录 |
| **重复内容** | 相同或高度相似的内容出现在多个 URL 上 | 是否浪费抓取预算；是否分散排名信号 |
| **渲染页面** | 现代 Googlebot 能执行 JavaScript，但仍建议 SSR/SSG | 关键内容是否以纯 HTML 形式即时可用 |

---

## 评估维度

### 1. Canonical 标签

- 首页和主要页面是否有 canonical 标签
- canonical 是否指向正确的首选 URL
- 是否存在 canonical 链（A→B→C）
- 是否存在自引用 canonical 错误
- 跨域 canonical 使用是否正确

### 2. Noindex / Nofollow

- 关键页面是否被误加 noindex（如产品页、文章页）
- 内链是否大量使用了 nofollow（浪费权重传递）
- noindex 页面是否仍出现在 Sitemap 中（矛盾信号）
- nofollow 是否被滥用（如导航链接）

### 3. Sitemap.xml

- 文件是否存在且可访问
- XML 格式合法性（正确命名空间、urlset 结构）
- URL 数量是否合理（与网站规模匹配）
- 是否包含已被 noindex 或 robots.txt 阻止的 URL
- 最后修改日期（lastmod）是否更新
- 优先级（priority）和变更频率（changefreq）是否合理

### 4. 重复内容检测

- 是否存在参数化 URL 导致内容重复（如 `?page=1`、`?sort=price`）
- 是否存在 www vs non-www、http vs https 的重复
- 是否存在分页重复内容
- 是否存在打印版/AMP 页面未设置 canonical

### 5. Hreflang（多语言站点）

- 多语言站点是否正确使用 hreflang 标签
- hreflang 与 canonical 是否一致
- 是否存在语言代码错误（如 `zh` vs `zh-CN`）

### 6. JavaScript SEO 与渲染检查

- 关键内容（标题、正文、链接）是否以纯 HTML 形式存在于源码中
- 是否依赖客户端 JavaScript 渲染关键 SEO 元素（title、meta、canonical）
- 是否使用 SSR/SSG（Next.js getServerSideProps/getStaticProps、Nuxt SSR）
- 动态渲染（Dynamic Rendering）是否正确配置
- 懒加载内容（图片、无限滚动）是否对爬虫友好
- 路由是否为 History API 路由（非 Hash 路由 `#/page`）
- 是否使用了 `<noscript>` 降级方案
- 对于 SPA（单页应用），是否实现了正确的预渲染或 SSR

---

## 排名因素关联

- **规范化**（Tier 2 背景）：Canonical 标签帮助集中排名信号，避免内容重复分散权重
- **内容新鲜度**（Tier 1）：Sitemap 中的 lastmod 帮助 Google 识别更新内容

---

## 评分指南

| 分数 | 等级 | 说明 |
|------|------|------|
| 90–100 | 优秀 | canonical 完整正确，无重复内容，sitemap 规范，noindex 使用精准 |
| 70–89 | 良好 | 轻微问题：少数页面缺少 canonical、部分参数化 URL 未处理、sitemap 有少量无效 URL |
| 60–69 | 有风险 | 关键页面缺少 canonical、存在明显重复内容、noindex 误用、sitemap 大量错误 |
| 0–59 | 严重 | 大量页面未设置 canonical、严重重复内容、关键页面被 noindex、sitemap 完全缺失 |

---

## 否决权规则

本 expert 拥有 **二级否决权**：
- 若分数 < 50（如大量关键页面被 noindex、严重重复内容未处理），总分扣减 **10 分**

---

## 算法背景

- **Canonical 标签支持（2009）**：允许站长指定规范 URL，解决重复内容问题
- **Hummingbird（2013）**：从关键词匹配转向语义理解，索引阶段即开始评估内容相关性
