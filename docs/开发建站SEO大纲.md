# 开发建站SEO

## 模块一：SEO技术基础

### 1. 搜索引擎如何抓取页面
- 爬虫工作流程
- JS渲染风险
- 抓取预算概念
- 代码规范与爬取效率（语义化HTML、DOM深度控制、避免无效嵌套）

### 2. 渲染方式决策
- SSR适用场景
- SSG适用场景
- ISR适用场景
- CSR风险与规避

---

## 模块二：网站架构设计

### 2.5 建站前期决策
- 域名选择策略（含关键词、后缀、历史记录、品牌匹配度）
- 服务器选择（地理位置、性能配置、SSL支持、CDN、服务器兼容性）
- 建站程序选择（CMS vs 自定义开发/Next.js/WordPress等）
- 关键词部署灵活性评估（CMS的SEO自定义能力）

### 3. URL设计方法论
- 语义化URL规则
- 层级控制标准
- 关键词映射表
- URL禁止项

### 4. 网站结构与导航
- 关键模块布局（首屏内容/CTA/信任元素/Social Proof）
- 内链布局原则
- 面包屑实现
- HTML可抓取导航
- 点击深度控制

---

## 模块三：页面Head管理

### 5. Title标签规范
- 唯一性规则
- 长度标准
- 关键词前置原则
- Template机制与品牌名追加
- 全站管理方案

### 6. Meta Description规范
- 唯一性规则
- 长度标准
- 价值主张写作
- CTR导向优化

### 7. Canonical与Hreflang
- 自引用canonical规则
- 参数化URL处理
- 多语言hreflang配置

### 8. Open Graph与社交标签
- OG四要素
- OG图片尺寸规范（1200x630）
- OG图片自动化生成（Puppeteer脚本）
- Twitter Card配置

---

## 模块四：内容标记与结构化

### 9. H标签语义体系
- H1唯一性
- 层级连续性
- 禁止事项
- 全站排查方法

### 10. 图片优化与Alt文本
- 图片格式选择
- 压缩标准
- 懒加载规则
- CLS预防
- Alt文本规范
- 全站Alt检查方法

### 11. Schema结构化数据（上）
- 必用类型清单
- 页面类型对应表
- JSON-LD格式规范

### 12. Schema结构化数据（中）
- WebApplication Schema（首页）
- SoftwareApplication Schema（工具页）
- FAQPage Schema（FAQ页）
- HowTo Schema（使用指南页）
- BreadcrumbList Schema（面包屑）
- Organization Schema（关于/联系页）

### 13. Schema结构化数据（下）
- 多Schema共存（数组形式）
- Google富媒体测试
- Schema验证器
- HowTo的image字段要求
- 常见错误与排查

---

## 模块五：可抓取性配置

### 14. robots.txt配置
- Allow与Disallow规则
- 敏感内容处理方式
- 禁止用robots.txt阻止索引
- 常见错误

### 15. Sitemap策略
- 自动生成方案
- 规范URL过滤
- lastmod固定日期策略
- 多语言处理
- 大规模站点方案

### 16. 404页面SEO规范
- 完整布局（Header/Footer）
- 热门工具推荐（降低跳出率）
- noindex标签
- Organization Schema一致性

### 16.5 301重定向与错误页面处理
- 301/302/308状态码使用规范
- URL变更与站内链接架构的批量重定向配置
- 重定向链与循环检测
- 旧链接权重传递评估

---

## 模块六：性能优化

### 17. Core Web Vitals：LCP优化
- 首屏资源加载
- 图片优先级（priority属性）
- 字体优化（next/font）
- DNS Prefetch与Preconnect

### 18. Core Web Vitals：INP优化
- 长任务拆分
- 事件轻量化
- 第三方脚本延迟加载

### 19. Core Web Vitals：CLS优化
- 尺寸声明要求
- Next.js Image组件（width/height/fill）
- sizes属性配置
- 骨架屏方案
- 动态内容预留

### 20. 前端性能通用优化
- 代码分割
- Brotli压缩
- CDN部署
- 缓存策略
- 图片压缩（Sharp）
- 页面缓存与CDN集成高级策略
- HTTPS与数据加密传输优化

---

## 模块七：移动端、体验与兼容

### 20.5 代码兼容技术
- 浏览器兼容性策略与 polyfill 方案
- 响应式断点规范
- 跨设备测试清单
- CSS/JS 降级与渐进增强

### 21. 移动优先索引
- 响应式规范
- 触控目标尺寸
- 字体规范
- 弹窗禁令

### 22. PWA与图标配置
- Apple Touch Icon（180x180 PNG）
- PWA Manifest配置
- 图标尺寸规范（192/512）
- theme_color与background_color

### 23. 网站用户体验设计规范
- 页面加载感知优化（骨架屏/占位符）
- 交互反馈与操作流畅性
- 内容可读性标准（行高/段距/对比度）
- 转化路径与漏斗优化

### 23.5 AMP（加速移动页面）集成
- AMP适用场景与取舍
- AMP页面规范与开发限制
- AMP与非AMP版本的canonical与alternate设置
- Google AMP富媒体搜索结果

### 23.6 无障碍与WCAG AA
- 对比度合规（emerald-500/600→700）
- aria-label覆盖
- 链接underline标识
- Lighthouse无障碍评分

---

## 模块八：安全与合规

### 24. Security Headers配置
- X-Frame-Options
- X-Content-Type-Options
- Referrer-Policy
- Permissions-Policy
- vercel.json配置方法

### 25. 合规页面
- Privacy Policy
- Terms of Service
- Cookie Consent（GDPR）
- About/Contact（EEAT）

### 25.5 防垃圾内容与恶意攻击防护
- 评论/表单垃圾过滤机制（CAPTCHA/Akismet）
- 常见攻击类型与防护（XSS/SQL注入/暴力破解）
- WAF与Rate Limiting配置
- 内容更新安全审计流程

---

## 模块九：分析工具嵌入

### 26. GSC接入
- 域名验证流程
- Sitemap提交
- 关注报告类型

### 27. GA4埋码与事件追踪
- 基础埋码
- 自定义事件设计
- 事件参数传递
- 转化事件配置

---

## 模块十：上线检查与维护

### 28. 上线检查清单
- 部署前检查项（Meta/Schema/robots/sitemap/图片/CWV）
- 上线后48小时验证

### 29. 常见开发错误
- CSR输出核心内容
- 图片未声明尺寸
- robots.txt阻止CSS/JS
- 无意义参数URL
- 移动端隐藏内容
- 302替代301
- 客户端跳转过多
- Sitemap日期伪更新
