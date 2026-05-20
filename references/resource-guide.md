# Resource Optimization Guide

> 供 `seo-resource-expert` 执行审计时参考。

---

## 角色定位

验证页面静态资源（JS、CSS、图片、字体等）是否经过合理优化，以最小化传输体积和渲染阻塞，提升页面加载速度。这是 Core Web Vitals 达标的基础工程工作。

---

## 排名因素关联

- **页面体验 / Core Web Vitals**（Tier 1，第 4 位）：资源优化直接影响 LCP、INP 等指标
- **页面加载速度**（Tier 3）：超出 CWV 的部分，资源优化仍有价值
- **图片优化**（Tier 3）：图片是大多数页面的最大资源

---

## 评估维度

### 1. JavaScript 优化

- 是否存在未使用的 JS 代码（Dead Code）
- 是否启用代码分割（Code Splitting）和懒加载（Lazy Loading）
- 是否压缩和混淆（Minify + Uglify）
- 是否使用 Tree Shaking 移除未使用模块
- 是否将非关键 JS 标记为 `defer` 或 `async`
- 是否存在阻塞渲染的同步 JS
- 第三方脚本（分析、广告、聊天）是否过多

### 2. CSS 优化

- 是否存在未使用的 CSS（Unused CSS）
- 是否压缩（Minify）
- 是否将关键 CSS 内联（Critical CSS Inline）
- 非关键 CSS 是否延迟加载
- 是否避免 `@import`（阻塞渲染）

### 3. 图片优化

- 是否使用现代格式（WebP、AVIF）
- 是否压缩（建议工具：Squoosh、ImageOptim）
- 是否使用响应式图片（srcset/sizes）
- 是否懒加载首屏以下图片
- 是否使用 SVG 替代简单图标

### 4. 字体优化

- 是否使用 `font-display: swap` 避免 FOIT
- 是否预加载关键字体（`<link rel="preload">`）
- 是否限制字体变体数量（weight/style）
- 是否使用子集化（Subset）减少字体文件大小

### 5. 缓存策略

- 静态资源是否有长期的 Cache-Control 头（如 `max-age=31536000`）
- 是否使用文件名哈希（Content Hash）实现长期缓存
- HTML 文档是否使用较短的缓存时间（如 `no-cache`）

### 6. CDN 使用

- 静态资源是否通过 CDN 分发
- CDN 节点是否覆盖目标用户地理区域
- 是否使用 HTTP/2 或 HTTP/3

---

## 评分指南

| 分数 | 等级 | 说明 |
|------|------|------|
| 90–100 | 优秀 | JS/CSS 充分优化压缩、使用代码分割、关键 CSS 内联、图片使用 WebP、CDN 配置完善 |
| 70–89 | 良好 | 轻微问题：部分未压缩资源、少量未使用代码、缺少关键 CSS 内联 |
| 60–69 | 有风险 | 大量未压缩 JS/CSS、未使用代码占比高、无代码分割、图片未优化 |
| 0–59 | 严重 | 资源完全未优化、大量阻塞渲染脚本、无 CDN、页面资源 > 5MB |
