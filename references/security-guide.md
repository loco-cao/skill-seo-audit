# Security Guide

> 供 `seo-security-expert` 执行审计时参考。

---

## 角色定位

验证网站是否满足基础安全标准。HTTPS 是 Google 的基础门槛，安全头配置和混合内容检测直接影响用户信任和搜索引擎评价。

---

## 排名因素关联

- **HTTPS 安全协议**（Tier 2，第 10 位）：基础门槛，未加密站点会被标记为不安全
- **页面体验 / Core Web Vitals**（Tier 1）：安全是页面体验的一部分

---

## 评估维度

### 1. HTTPS 与 HSTS

- 全站是否强制 HTTPS（HTTP 请求是否 301 重定向到 HTTPS）
- 是否启用 HSTS（HTTP Strict Transport Security）
- HSTS max-age 是否足够长（建议 ≥ 1 年）
- 是否存在 HTTPS 页面加载 HTTP 资源（混合内容）
- 证书是否有效（未过期、受信任 CA 签发、域名匹配）

### 2. 安全头配置

| 安全头 | 作用 | 推荐值 |
|--------|------|--------|
| **Content-Security-Policy (CSP)** | 限制资源加载来源，防止 XSS | `default-src 'self'` 为基础，按需扩展 |
| **X-Frame-Options** | 防止点击劫持 | `DENY` 或 `SAMEORIGIN` |
| **X-Content-Type-Options** | 防止 MIME 类型嗅探 | `nosniff` |
| **Referrer-Policy** | 控制 referrer 信息传递 | `strict-origin-when-cross-origin` |
| **Permissions-Policy** | 限制浏览器 API 权限 | 按需禁用不需要的 API |

### 3. 混合内容检测

- HTTPS 页面是否加载 HTTP 图片、JS、CSS、iframe
- 是否存在被动混合内容（图片、视频）
- 是否存在主动混合内容（JS、CSS、iframe）—— 更危险

### 4. 可疑脚本与安全风险

- 是否存在大量 eval() 或字符串转代码
- 是否存在已知恶意域名引用
- 是否存在意外的第三方 iframe
- 是否存在过时的库版本（如旧版 jQuery 含已知漏洞）

### 5. 隐藏文本与链接检测（黑帽手法）

- 是否存在文字颜色与背景颜色相同/相近（肉眼不可见但爬虫可读）
- 是否存在 CSS 隐藏文本（`display: none`、`visibility: hidden`、`opacity: 0`、`font-size: 0`）
- 是否存在将文字移出可视区域（`text-indent: -9999px` 等负值定位）
- 是否存在仅对搜索引擎可见的链接（如 1×1 像素链接）
- 是否存在 `z-index` 层叠隐藏的欺骗性内容
- 移动端和桌面端是否展示不同内容（Cloaking 风险）

### 6. 基础可访问性（与安全协同）

- 图片 alt 文本（与 image-expert 协同，此处做基础检查）
- 表单字段是否有 label 关联
- 颜色对比度是否足够（WCAG AA 标准：正文 4.5:1，大文字 3:1）
- 是否支持键盘导航（Tab 键可遍历所有交互元素）
- 焦点指示器是否可见

---

## 评分指南

| 分数 | 等级 | 说明 |
|------|------|------|
| 90–100 | 优秀 | 全站 HTTPS + HSTS、安全头完整、无混合内容、无可疑脚本、基础无障碍达标 |
| 70–89 | 良好 | 轻微问题：缺少 1-2 个安全头、少量被动混合内容、个别 alt 缺失 |
| 60–69 | 有风险 | 未启用 HSTS、缺少多个安全头、存在主动混合内容、部分颜色对比度不足 |
| 0–59 | 严重 | 无 HTTPS、证书无效、大量混合内容、存在可疑脚本、完全无障碍支持 |
