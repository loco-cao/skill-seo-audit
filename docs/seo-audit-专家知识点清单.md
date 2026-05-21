# seo-audit 专家知识点清单（按专家类型分模块）

---

## seo-audit-framework（评估框架专家）

### 评分体系设计
- 采用100分制加权评分，总分由各专家分数×权重相加
- 五大模块权重分配：技术SEO 30%、On-Page 20%、内容质量 20%、外链 15%、用户体验 15%
- P0-P3四级优先级定义：
  - P0（Critical）：阻塞索引、安全风险、黑帽手法，24小时内必须修复
  - P1（High）：严重影响排名或体验，1周内修复
  - P2（Medium）：中等影响，1个月内修复
  - P3（Low）：优化项，按排期处理

### 352黄金法则评估框架
- 3大核心要素审计：
  - TDK设置合规性（唯一性、长度、关键词匹配）
  - 内容质量（原创度、深度、EEAT信号）
  - 外链健康度（质量、锚文本分布、毒性链接比例）
- 5维优化检查：
  - 技术（索引、速度、移动、安全、Schema）
  - On-Page（TDKU、H标签、图片Alt、内链）
  - 内容（原创度、搜索意图、新鲜度、关键词布局）
  - 外链（质量、数量趋势、锚文本多样性、品牌建设）
  - 用户体验（跳出率、停留时间、转化路径、可读性）
- 2条底线原则：
  - 白帽合规：无任何购买链接、PBN、关键词堆砌、隐藏文本
  - 用户价值优先：内容解决用户问题，非为搜索引擎而写

### 否决权规则
- Crawlability分数<50 → 最终等级强制不超过"待提升"
- Indexability分数<50 → 总分扣减10分
- 发现黑帽手法 → 一票否决，标记为高风险

---

## seo-crawlability-expert（爬取通道审查专家）

### robots.txt审查
- robots.txt必须位于网站根目录且可访问（200状态）
- 禁止Disallow: /（全站阻止）
- 禁止Disallow CSS/JS目录（影响Google渲染）
- 必须包含Sitemap引用（Sitemap: https://.../sitemap.xml）
- 敏感内容不得仅依赖robots.txt保护（应使用noindex或认证）
- 检查Allow/Disallow规则冲突与逻辑错误

### Sitemap审查
- Sitemap.xml必须可访问且返回200状态码
- 只包含规范URL（200状态、canonical自引用、非noindex）
- 无重复URL、无参数化URL污染
- lastmod日期真实反映页面修改时间
- URL数量符合站点规模，与GSC覆盖率报告差异≤10%
- 大规模站点使用Sitemap索引文件，单文件≤5万URL/50MB

### 死链与抓取错误
- 全站扫描识别4xx/5xx错误链接
- 内链中的死链必须标记为High优先级
- 外部链接死链超过一定比例需清理
- 检查重定向链长度，超过2跳标记为问题
- 检查无限循环重定向

### 抓取预算优化
- 低价值页面（搜索结果页、筛选页、标签页）应使用noindex或robots.txt限制
- 禁止大量相似参数化URL消耗抓取预算
- 核心页面应在Sitemap中且距首页点击深度≤3
- GSC覆盖率报告检查：已排除页面中是否存在应被索引的URL

### GSC覆盖率报告解读
- 有效页面数量趋势（上升/下降/稳定）
- 错误类型分类：服务器错误(5xx)、重定向错误(3xx)、 robots.txt阻止、404
- 已排除原因分析：被noindex、重复内容、软404、已抓取未索引
- 覆盖率骤降排查：技术变更（robots/sitemap）、服务器问题、批量URL失效

---

## seo-indexability-expert（索引管理审查专家）

### noindex使用规范
- noindex标签使用场景：感谢页、购物车、搜索结果页、低质筛选页
- 禁止在核心内容页使用noindex
- noindex页面不得出现在Sitemap中
- X-Robots-Tag与meta robots标签不得冲突

### Canonical审查
- 每页必须有自引用canonical（<link rel="canonical" href="...">）
- canonical目标必须返回200状态码
- 禁止canonical指向noindex页面
- 禁止全站canonical指向首页（常见CMS错误）
- 参数化URL必须canonical回主URL
- 分页canonical处理：第N页canonical指向自身或View All页

### 重复内容检测
- 同内容多URL访问检测（如带/不带www、http/https、尾斜杠）
- 参数化URL重复（?sort=price、?page=2等未canonical处理）
- 打印版/移动端/AMP版未canonical处理
- 跨域重复内容（ syndication 未canonical）
- 使用Siteliner/Copyscape或GSC覆盖报告定位重复内容

### Hreflang审查
- 多语言页面必须有hreflang标签或Sitemap声明
- x-default必须存在且指向默认语言/地域版本
- hreflang指向的URL必须返回200且自引用canonical
- 禁止hreflang与canonical冲突
- 所有语言变体互相标注（双向标注验证）

### JS渲染审查
- 禁用JS后核心内容是否仍在HTML中
- 关键meta标签（Title/Description/Canonical/OG）是否在服务端HTML中
- 检查Google渲染后的页面与用户体验页面是否一致
- 大型JS框架（React/Vue）检查是否使用SSR/SSG/动态渲染

---

## seo-architecture-expert（网站架构审查专家）

### URL层级审查
- URL层级深度≤4层，核心页面≤3层
- URL语义化，包含目标关键词
- 禁止使用无意义ID、Session参数
- 全站URL大小写统一（建议全小写）
- 尾斜杠统一策略

### 内链结构审查
- 重要页面内链数量≥3条（来自不同来源页面）
- 内链锚文本多样性：禁止100%精确匹配关键词
- 内链布局自然，禁止底部堆砌链接区块
- 孤立页面检测（无内链指向且未在Sitemap中的页面）
- 权重传递路径：首页→分类→内容页链路清晰

### 面包屑导航审查
- 面包屑必须可见且可点击
- 层级逻辑与URL结构一致
- 必须包含BreadcrumbList Schema
- 首页入口必须存在

### 关键模块布局评估
- 首屏必须包含H1、核心价值主张、主CTA
- 信任元素（安全徽章、用户评价、认证标志）位置合理
- Social Proof（用户数量、客户logo墙）在首屏或第二屏可见
- Footer包含关键分类链接、About/Contact/Privacy/Terms
- 导航菜单不超过7个主项（认知负荷原则）

### HTML可抓取导航
- 主导航使用<a href>，禁止纯button/div+JS跳转
- 分页导航使用<a href>而非JS加载更多（或同时提供a标签）
- 多级下拉菜单使用HTML嵌套，保证爬虫可遍历

---

## seo-meta-expert（Meta标签审查专家）

### Title审计
- 全站每页Title唯一性检查
- 长度检查：英文≤60字符，中文≤30字符（像素宽度限制600px）
- 关键词前置原则：核心词出现在前20字符
- 检查Template机制：品牌名追加格式统一（`| 品牌`或`- 品牌`）
- 禁止关键词堆砌（同一词出现>2次且无意义）
- 分页Title区分：`原标题 - 第2页`或`Page 2 | 品牌`
- 全站Title排查方法：抓取所有页面Title，按重复度分组统计

### Meta Description审计
- 全站每页Description唯一性
- 长度120-160字符，超出在SERP中截断
- 包含至少一个核心关键词（会被加粗显示）
- 包含明确的CTA或价值主张
- 禁止纯关键词列表，必须是完整句子
- 高展现低CTR页面优先修复（从GSC获取数据）

### OG与社交标签审计
- og:title、og:description、og:url、og:image四项齐全
- og:image尺寸1200x630，可正常访问（200状态）
- og:type正确（website/article/product）
- Twitter Card（summary_large_image或summary）配置
- viewport与charset声明存在

### TDKU一致性审计
- Title/Description/Keywords（如有）/URL 四要素与页面主题一致
- 全站TDKU策略统一，无混乱的命名风格
- 搜索意图匹配度：信息型/交易型/导航型意图与页面类型对应

---

## seo-heading-expert（标题层级审查专家）

### H1审计
- 每页必须有且仅有一个H1
- H1包含核心关键词（自然出现）
- H1不可与Title完全重复（应互为补充）
- 全站H1唯一性排查：抓取统计重复H1文本

### H1-H6层级审计
- 层级连续：H1→H2→H3，禁止跳级（H1后直接H3）
- 禁止用H标签控制字体大小（应使用CSS）
- H2作为章节标题，H3作为子章节，H4+谨慎使用
- 同一页面H2数量建议3-10个（过长内容可更多）

### 语义标记审查
- 主内容区使用<main>
- 文章使用<article>，章节使用<section>
- 避免全篇<div>堆砌（至少关键区域有语义标签）

### 关键词分布审查
- 关键词在H2/H3中自然分布（不强制每级都有）
- 长尾关键词变体在子标题中出现
- 禁止在标题中堆砌关键词

---

## seo-image-expert（图片优化审查专家）

### Alt文本审计
- 所有图片必须有alt属性（装饰性图片用alt=""）
- Alt描述图片内容，非堆砌关键词
- 含有关键词的alt必须自然（图片确实与关键词相关）
- 全站Alt检查：统计<img>无alt比例，目标=0%

### 图片格式与压缩
- 优先使用WebP/AVIF，JPEG回退
- 文件大小合理：首屏图片<200KB，其他<500KB
- 使用响应式图片（srcset/sizes）适配不同设备

### CLS预防审查
- 所有<img>声明width/height或使用CSS aspect-ratio
- Next.js Image组件检查sizes配置
- 懒加载图片首屏外使用，首屏图片priority加载
- 动态内容（广告、推荐）预留固定空间

### 图片SEO基础
- 图片文件名语义化（非IMG_1234.jpg）
- 图片URL路径简洁
- 考虑图片Sitemap（大规模图库站点）

---

## seo-content-expert（内容质量审查专家）

### 原创度检测
- 使用Copyscape/Siteliner检测重复内容
- 与TOP3竞品对比，确保有信息增益（额外价值）
- 禁止采集、机器翻译、低质量伪原创
- 内容新鲜度：核心页面最后更新时间，博客更新频率

### 搜索意图匹配
- 四类搜索意图识别：信息型(Informational)、导航型(Navigational)、交易型(Transactional)、商业调查型(Commercial Investigation)
- 页面类型与意图对应：
  - 博客/指南 → 信息型
  - 产品页 → 交易型
  - 对比页/评测 → 商业调查型
  - 品牌首页 → 导航型
- SERP分析法：搜索目标关键词，看Google倾向的页面类型和内容格式

### 内容深度评估
- 与排名首页竞品对比内容长度与覆盖度
- 信息增益判断：是否回答了用户后续问题
- 内容结构清晰：目录、分节、列表、表格、FAQ
- 关键词密度1-2%，TF-IDF语义相关性达标
- 同义词与LSI关键词自然嵌入（不刻意堆砌）

### Thin Content检测
- 页面字数<300字且无独特价值 → 标记为thin content
- 自动生成的 doorway pages（门页）检测
-  affiliate 页面必须有原创内容，非纯复制
- 标签页/分类页无独特内容应使用noindex

### 内容更新机制审计
- CMS发布机制是否支持定期更新
- 旧内容是否有维护计划（更新日期、内容翻新）
- 博客更新频率：目标≥每周1篇（竞争型行业）
- 核心页面每季度审查一次

### 出站链接质量
- 出站链接指向可信、权威来源
- 可疑/低质出站链接使用nofollow
- 出站链接打开方式一致（建议新标签页打开外部链接）

---

## seo-eeat-expert（E-E-A-T信号审查专家）

### Experience（经验）检查点
- 内容是否体现第一手的实际经验（作者使用过产品/服务）
- 是否有案例、数据、截图、过程描述
- YMYL领域（健康/金融/法律）内容是否由有实际经验者撰写

### Expertise（专业性）检查点
- 作者资质展示：署名、作者简介、专业背景
- YMYL内容必须有专家审核或资质证明
- 技术/专业内容深度是否达到行业平均水平以上
- 错误信息/过时信息检查

### Authoritativeness（权威性）检查点
- 品牌/网站在行业内的认知度
- 外部引用：是否被其他权威网站引用/链接
- 作者个人品牌（LinkedIn/Twitter/行业出版物）
- About页面展示团队资质、荣誉、媒体报道

### Trustworthiness（可信度）检查点
- 准确的联系信息（地址、电话、邮箱）
- 安全支付标识（如适用）
- 用户评论/评分真实可验证
- Privacy Policy与Terms of Service完整且合规
- 无误导性声明、无虚假承诺
- 内容引用来源标注

### YMYL特殊要求
- 健康/医疗内容必须有医学专业人士审核
- 金融/投资建议必须有资质声明和风险提示
- 法律内容必须有律师执业资质
- 儿童/安全相关内容需额外谨慎

---

## seo-schema-expert（结构化数据审查专家）

### 必用Schema类型检查
- 首页/产品站：WebSite + Organization 或 WebApplication/SoftwareApplication
- 工具/应用页：SoftwareApplication（含name/description/applicationCategory/operatingSystem/offers/aggregateRating）
- FAQ页：FAQPage（mainEntity数组，每个item含name+acceptedAnswer.text）
- 使用指南页：HowTo（tool/supply/step数组，每个step含name+text+image）
- 面包屑：BreadcrumbList（itemListElement数组）
- 联系/关于页：Organization（name/url/logo/contactPoint/sameAs）

### JSON-LD格式合规
- 使用<script type="application/ld+json">嵌入<head>
- @context必须为https://schema.org
- @type使用Schema.org标准类型名
- 多Schema共存时使用JSON数组
- 属性值符合Schema.org定义的数据类型

### 富媒体搜索结果验证
- 通过Google富媒体测试工具验证（Rich Results Test）
- 通过Schema.org验证器验证结构
- 无必填字段缺失
- 无类型错误（如将字符串放入数字字段）

### 常见错误排查
- FAQPage混入非问答内容 → 会被Google拒绝
- HowTo缺少image字段 → 无法获得富媒体展示
- SoftwareApplication缺少aggregateRating → 星级不显示
- Organization缺少sameAs → 知识面板关联失败
- BreadcrumbList层级与页面实际层级不符

---

## seo-core-web-vitals-expert（CWV审查专家）

### LCP审查
- LCP目标值：Good≤2.5s，Needs Improvement≤4.0s，Poor>4.0s
- LCP元素识别：首屏最大图片或文本块
- 检查LCP图片是否有priority/preload
- 检查字体是否阻塞渲染（font-display: swap）
- 检查服务器TTFB是否<600ms

### INP审查
- INP目标值：Good≤200ms，Needs Improvement≤500ms，Poor>500ms
- 检查长任务（Long Tasks >50ms）
- 检查第三方脚本加载时机（应延迟/异步）
- 检查事件处理函数复杂度

### CLS审查
- CLS目标值：Good≤0.1，Needs Improvement≤0.25，Poor>0.25
- 检查所有图片是否有width/height或aspect-ratio
- 检查动态内容（广告、推荐、弹窗）是否预留空间
- 检查Web字体加载是否引起布局偏移
- 检查骨架屏/占位符实现

### 移动端可用性
- 响应式适配检查（Google移动友好测试）
- 触控目标尺寸≥48x48dp
- 禁止插入式弹窗/插页广告（Google惩罚项）
- 字体大小可读（≥16px基准）

### HTTPS与安全性
- 全站HTTPS强制（301跳转HTTP→HTTPS）
- 无混合内容警告（HTTP资源在HTTPS页面中）
- HSTS Header已配置

### PSI实操
- 同时关注Lab Data和Field Data（CrUX）
- Field Data不足时以Lab Data为参考
- 关注机会(Opportunities)中的高影响力项
- 诊断(Diagnostics)中的建议按优先级排序

---

## seo-resource-expert（资源优化审查专家）

### JS/CSS优化
- JS文件压缩与Tree Shaking
- CSS提取与移除未使用样式（Coverage工具检查）
- 关键CSS内联（首屏所需）
- 非关键JS/CSS延迟加载（defer/async）

### 缓存策略
- 静态资源长期缓存（1年，文件名含content hash）
- HTML短期缓存（s-maxage策略）
- CDN缓存配置正确

### 图片与媒体资源
- 图片压缩率合理（WebP质量80-85）
- 响应式图片srcset配置
- 视频使用延迟加载或poster占位

---

## seo-mobile-expert（移动优化审查专家）

### 移动优先索引
- 移动端内容=桌面端内容（禁止移动端隐藏核心内容）
- 移动可用性测试通过（Google Search Console移动可用性报告）
- 视口meta正确配置

### 响应式设计
- 断点合理：mobile <768px、tablet 768-1024px、desktop >1024px
- 无水平滚动条（min-width导致）
- 文本无需缩放即可阅读

### PWA检查
- manifest.json存在且有效
- Service Worker注册（如实现PWA）
- 图标尺寸齐全（192x192、512x512）

---

## seo-security-expert（安全审查专家）

### HTTPS与加密
- 全站HTTPS，HTTP 301跳转HTTPS
- HSTS配置（max-age≥31536000，includeSubDomains）
- 无混合内容（Mixed Content）

### Security Headers
- X-Frame-Options: DENY/SAMEORIGIN
- X-Content-Type-Options: nosniff
- Referrer-Policy: strict-origin-when-cross-origin
- Content-Security-Policy（如适用）
- Permissions-Policy按需限制

### 恶意内容检测
- 隐藏文本/隐藏链接检测（CSS display:none/color匹配背景）
- 可疑脚本检测（未声明来源的第三方脚本）
- 被黑迹象检测（垃圾外链注入、奇怪重定向）

---

## seo-ux-expert（用户体验审查专家）

### 导航与交互
- 主导航在所有页面可访问且一致
- 站内搜索功能可用且结果相关
- 404页面有帮助性内容（热门链接、搜索框）
- CTA按钮可见且明确

### 社交分享
- OG标签完整（已在meta专家覆盖）
- 社交分享按钮功能正常

### 内容与布局
- 页面布局符合F型阅读习惯
- 内容密度适中，段落不超过5行
- 列表、表格、图片合理穿插

### UGC与评论
- 评论区有垃圾过滤机制
- UGC链接自动nofollow
- 无明显的虚假评论

---

## seo-backlink-expert（外链质量审查专家）

### 外链基础数据分析
- 外链总数量与引用域（Referring Domains）数量比值
- 引用域数量趋势（上升/下降/稳定）
- DR/DA评分查看（Ahrefs/Moz/SEMrush）
- 锚文本分布分析：品牌锚文本≥50%，精确匹配≤10%，自然混合其余

### 高质量外链特征识别
- 来源域名与目标站点主题相关
- 链接位于正文内容中（非页脚/侧边栏）
- 来源页面本身有流量和权重
- 链接是编辑性链接（非购买/交换）
- 来源域名DR≥30（或行业基准）
- 锚文本自然描述目标页面内容

### Toxic外链识别
- 来源域名DR<10且大量出站链接
- 明显的PBN网络特征（相似模板、同一IP、互相链接）
- 外链获取速度异常激增（短时间内数千条）
- 锚文本100%精确匹配关键词
- 来源网站已被Google惩罚或deindexed
- 垃圾目录站、自动生成的链接农场

### Nofollow与链接属性审计
- 赞助/广告链接必须使用rel="sponsored"
- UGC评论链接必须使用rel="nofollow ugc"
- 出站链接到不可信站点使用rel="nofollow"
- nofollow链接比例检查：健康站点通常有自然比例的nofollow

### 外链建设渠道审计
- 工具目录提交：AlternativeTo、Product Hunt、Toolify是否已提交
- 社交媒体个人资料外链完整性
- GitHub开源项目外链（如有开源）
- Reddit社区推广合规性（非spam，参与讨论后自然提及）
- Product Hunt发布历史与效果
- Medium/客座博客外链质量
- Broken Link Building执行记录
- HARO（Help A Reporter Out）响应记录

### 品牌建设监测
- 品牌搜索量（Google Trends/Keyword Planner）
- 品牌提及搜索（非链接提及）
- 社交媒体活跃度与粉丝增长
- 锚文本中品牌词占比≥50%

### 外链风险与合规
- 新站外链建设节奏：前3个月每月5-10条高质量外链，禁止爆发式增长
- 购买外链识别：Fiverr/黑帽论坛模式、精确匹配锚文本包、PBN链接包
- PBN识别：相似Whois、同一服务器IP、低质内容模板、高出站链接/低入站链接比
- Google外链惩罚类型：算法降级（Penguin）、手动处罚（Unnatural Links）
- 拒绝文件（Disavow）使用场景与正确格式

---

## seo-competitor-expert（竞品分析专家）

### 竞品筛选标准
- 目标关键词SERP前10中 recurring domains（多次出现的域名）
- 业务模型相似（直接或间接竞品）
- 域名权重与自身相当或略高（可追赶）
- 有值得学习的内容/技术/外链策略
- 筛选数量：3-5个核心竞品

### 六维对比框架
- 技术SEO（索引量、速度、移动适配）
- 内容覆盖（关键词覆盖数、内容深度、更新频率）
- 外链 profile（DR、引用域、锚文本分布）
- 用户体验（设计、交互、转化路径）
- 品牌信号（搜索量、社交存在、提及量）
- EEAT信号（作者资质、About页面、信任元素）

### 竞品数据提取
- 核心关键词排名对比（自身vs竞品）
- 流量估算对比（SimilarWeb/Ahrefs）
- Top页面识别（竞品流量最高的页面）
- 内容差距分析（竞品有排名而自身无覆盖的关键词）

### 机会识别
- 共同优势：多个竞品都做对的事（行业基准）
- 差异化空白：竞品未覆盖但搜索量存在的长尾词
- 可复制资源：竞品获取外链的渠道、内容格式、Schema类型
- 快速胜利（Quick Wins）：低竞争度、高价值的关键词/内容缺口

---

## seo-data-expert（数据解读与报告专家）

### 用户体验信号分析
- 跳出率标准：内容页40-60%，产品页20-40%，首页30-50%
- 停留时间标准：博客≥2分钟，产品页≥1分钟
- 页面深度（每次访问页数）≥2页为健康
- 转化事件检查：关键转化路径完整追踪
- 热力图分析：F型布局验证、首屏注意力分布

### GSC数据解读
- 展现量趋势：识别上升/下降的关键词群组
- 点击量趋势：与展现量联动分析
- 平均排名变化：核心词排名波动监控
- CTR分析：
  - 高展现低CTR（<3%）→ Title/Description优化
  - 高CTR低展现 → 排名提升潜力词
  - 品牌词CTR应≥30%
- 查询报告分析：发现新的长尾词机会

### 风险评估
- 惩罚风险清单：购买链接、关键词堆砌、隐藏内容、 doorway pages
- 手动处罚检查：GSC安全与手动操作报告
- 算法更新影响评估：排名骤降时间点与已知算法更新对应
- 黑帽手法识别：PBN、链接农场、内容采集、 Cloaking

### 报告撰写
- 报告结构：执行摘要→评分概览→逐模块详情→问题清单→行动计划
- 修复清单按P0-P3分级，含预估工作量
- 客户汇报话术：技术术语转化为业务影响
- 可视化：雷达图展示各维度得分，趋势图展示历史变化

### SEO项目管理
- P0-P3任务分级与排期
- 技术SEO地基优先原则：先修复索引/抓取问题，再优化内容
- 页面SEO与内容SEO阶段划分
- 执行跟踪表：任务/负责人/截止日期/状态/影响预估
- 核心指标追踪表：排名/流量/转化/索引量/CWV
- 每周检查：GSC覆盖率、排名波动、新错误
- 每月检查：流量趋势、内容表现、外链增长、竞品动态
- 策略调整方法：A/B测试Title、内容更新效果追踪
