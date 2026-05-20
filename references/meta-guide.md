# Meta Tags Guide

> 供 `seo-meta-expert` 执行审计时参考。

---

## 角色定位

验证页面头部的元数据标签是否完整、规范、利于搜索引擎理解和用户点击。Meta 标签是搜索结果页（SERP）中直接展示给用户的信息。

---

## 排名因素关联

- **关键词在 Title / H1 / URL 中的使用**（Tier 2，第 8 位）：**Title 仍是最重要的 on-page 信号**
- **Schema 结构化数据**（Tier 2，第 11 位）：虽不直接影响排名，但能获取富媒体摘要，提升 CTR
- **Meta Keywords**（Tier 4）：Google 已完全忽略，审计中可忽略

---

## 评估维度

### 1. Title Tag

- **存在性**：每页必须有 title 标签
- **长度**：50–60 个字符（超出会被截断）
- **关键词位置**：核心关键词建议前置
- **独特性**：全站各页 title 不应重复
- **品牌词**：是否包含品牌名（通常放末尾，用分隔符如 `|` 或 `-`）
- **可读性**：是否自然通顺，非关键词堆砌

### 2. Meta Description

- **存在性**：每页建议有 meta description（非强制，但有助 CTR）
- **长度**：150–160 个字符（超出会被截断）
- **号召性用语**：是否包含行动号召（如"了解详情"、"立即购买"）
- **关键词匹配**：是否包含目标关键词（不直接影响排名，但高亮显示提升 CTR）
- **独特性**：全站各页 description 不应重复

### 3. Open Graph 标签

- `og:title`：是否存在且与 title 一致或互补
- `og:description`：是否存在
- `og:image`：是否存在且尺寸符合推荐（1200×630px）
- `og:url`：是否为规范 URL
- `og:type`：是否正确（website、article 等）

### 4. Twitter Cards

- `twitter:card`：是否存在（summary、summary_large_image 等）
- `twitter:title` / `twitter:description` / `twitter:image`：是否配置

### 5. Viewport

- `<meta name="viewport" content="width=device-width, initial-scale=1">` 是否存在
- 配置是否正确（影响移动适配）

### 6. Charset

- `<meta charset="UTF-8">` 是否声明且位于 head 前 1024 字节内

---

## 评分指南

| 分数 | 等级 | 说明 |
|------|------|------|
| 90–100 | 优秀 | 所有页面 title/description 完整规范，OG/Twitter 配置齐全，viewport 正确 |
| 70–89 | 良好 | 轻微问题：少数页面 title 过长/过短、部分缺少 OG 标签、个别 description 重复 |
| 60–69 | 有风险 | 大量页面缺少 description、title 严重重复或堆砌、OG 标签大面积缺失 |
| 0–59 | 严重 | 大量页面无 title、viewport 缺失导致移动适配失败、meta 标签完全混乱 |
