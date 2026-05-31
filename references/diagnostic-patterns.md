# SEO 诊断模式库

> 供审计入口点和 `seo-data-expert` 在汇总阶段快速匹配已知问题模式。
> 基于 SEO 352 黄金法则和实际审计经验积累。

---

## 模式 1：搜索流量骤降

### 症状识别

- 搜索流量在特定时间点突然下降 > 30%
- 排名位置明显下滑
- GSC 点击量/展示量曲线出现断崖

### 预检信号

| 信号 | 检查方式 | 阈值 |
|------|---------|------|
| GSC 展示量断崖 | `--gsc` 数据 | 7 天内下降 > 50% |
| 首页被去索引 | `site:domain.com` | 首页不在第 1 位 |
| 手动操作通知 | GSC 安全与手动操作 | 存在未处理通知 |
| 算法更新时间线 | 对照 Google 算法更新日历 | 下降时间与更新吻合 |

### 重点关注专家

| 优先级 | 专家 | 检查要点 |
|--------|------|---------|
| P0 | Crawlability | robots.txt 是否被误改？全站是否返回 5xx？ |
| P0 | Indexability | 是否有大量 noindex 标签？canonical 是否指向错误域名？ |
| P0 | Security | 是否被黑？是否收到手动操作通知？ |
| P1 | Content | 是否有大量内容被判定为 thin content？ |
| P1 | Backlink | 是否有 toxic 外链激增？是否被负面 SEO 攻击？ |

### 诊断决策树

```
流量骤降
├─ 全站性下降 → 检查 Crawlability + Security
│  ├─ robots.txt 误改 → P0 立即修复
│  ├─ 服务器 5xx → P0 运维排查
│  ├─ 被黑/挂马 → P0 安全团队介入
│  └─ 手动操作 → P0 提交复议
│
├─ 部分栏目下降 → 检查 Content + Indexability
│  ├─ noindex 误加 → P0 移除标签
│  ├─ 内容被判定低质 → P1 内容整改
│  └─ canonical 指向错误 → P1 修正指向
│
└─ 特定关键词下降 → 检查 Competitor + Content
   ├─ 竞品内容更新 → P2 内容升级
   └─ 搜索意图变化 → P2 调整内容策略
```

---

## 模式 2：网站收录异常

### 症状识别

- GSC 索引覆盖率 < 50%
- 新页面长期不被收录（> 2 周）
- URL 检查工具显示"未在 Google 索引中"

### 预检信号

| 信号 | 检查方式 | 阈值 |
|------|---------|------|
| 索引覆盖率 | GSC 覆盖率报告 | < 50% |
| 已抓取-未索引 | GSC 覆盖率报告 | 占总页面 > 30% |
| 发现-未抓取 | GSC 覆盖率报告 | 占总页面 > 20% |
| 抓取预算浪费 | 服务器日志分析 | 低质页面占比 > 60% |

### 重点关注专家

| 优先级 | 专家 | 检查要点 |
|--------|------|---------|
| P0 | Crawlability | robots.txt 是否阻止关键目录？Sitemap 是否正确提交？ |
| P0 | Indexability | 是否有 noindex meta？canonical 是否正确？ |
| P1 | Architecture | 内链结构是否导致深层页面无法被发现？ |
| P1 | Content | 是否有大量低质/重复页面消耗抓取预算？ |
| P2 | Meta | 是否有页面缺少 title/description？ |

### 诊断清单

```
□ robots.txt 是否阻止了 Googlebot？
□ robots.txt 是否包含 Sitemap 引用？
□ Sitemap 是否在 GSC 中提交？
□ Sitemap 中的 URL 是否返回 200？
□ 页面是否有 <meta name="robots" content="noindex"> ？
□ 页面是否有 X-Robots-Tag: noindex ？
□ canonical 是否指向自身？
□ 页面是否需要登录才能访问？
□ 页面内容是否 < 300 字？
□ 页面是否被判定为重复内容？
□ 服务器响应时间是否 > 2s？
```

---

## 模式 3：重复内容问题

### 症状识别

- 搜索结果中同一网站出现多个相似标题
- GSC 显示"重复页面没有规范标签"
- 同一内容有多个 URL 变体

### 常见场景

```
场景 1: URL 参数
  example.com/product?id=123
  example.com/product?id=123&color=red
  example.com/product?id=123&utm_source=fb

场景 2: 协议/域名混用
  http://example.com/page
  https://example.com/page
  http://www.example.com/page
  https://www.example.com/page

场景 3: 尾斜杠不一致
  example.com/page
  example.com/page/

场景 4: 分页与筛选
  example.com/blog?page=1
  example.com/blog?page=2
  example.com/blog?category=seo&page=1
```

### 重点关注专家

| 优先级 | 专家 | 检查要点 |
|--------|------|---------|
| P0 | Indexability | canonical 是否指向规范 URL？ |
| P1 | Architecture | URL 结构是否统一？是否有重定向规范？ |
| P1 | Meta | 重复页面是否有不同的 title/description？ |
| P2 | Crawlability | 参数化 URL 是否在 robots.txt 中处理？ |

### 修复方案

| 方案 | 场景 | 工作量 |
|------|------|--------|
| 301 重定向 | 域名/协议不统一 | 服务器配置，1 小时 |
| canonical 标签 | 参数化 URL | 代码修改，2 小时 |
| URL 参数处理 | 追踪参数 | GSC 配置，30 分钟 |
| noindex + canonical | 分页页面 | 模板修改，1 小时 |

---

## 模式 4：移动端排名落后

### 症状识别

- 移动端排名明显低于桌面端
- GSC 显示移动可用性问题
- Core Web Vitals 移动端评分显著低于桌面端

### 预检信号

| 信号 | 检查方式 | 阈值 |
|------|---------|------|
| 移动可用性问题 | GSC 移动可用性 | 存在错误页面 |
| 移动端 LCP | PageSpeed Insights | > 4s |
| 移动端 CLS | PageSpeed Insights | > 0.25 |
| 移动端 INP | PageSpeed Insights | > 200ms |

### 重点关注专家

| 优先级 | 专家 | 检查要点 |
|--------|------|---------|
| P0 | Mobile | viewport 是否正确？是否有弹窗遮挡？触控目标是否足够？ |
| P0 | Core Web Vitals | 移动端 LCP/INP/CLS 是否达标？ |
| P1 | Resource | 是否有阻塞渲染的 JS？CSS 是否过大？ |
| P1 | Image | 图片是否响应式？是否使用 srcset？ |
| P2 | UX | 移动端导航是否可用？转化路径是否顺畅？ |

### 诊断清单

```
移动友好性：
□ 是否使用 <meta name="viewport" content="width=device-width, initial-scale=1"> ？
□ 字体大小是否 ≥ 12px（推荐 16px）？
□ 点击元素间距是否 ≥ 8mm（推荐 48px × 48px）？
□ 是否有侵入式弹窗（Pop-up）？
□ 内容是否被截断或需要横向滚动？

移动性能：
□ 移动端 LCP 是否 < 2.5s？
□ 移动端 INP 是否 < 200ms？
□ 移动端 CLS 是否 < 0.1？
□ 是否使用了响应式图片（srcset）？
□ 是否延迟加载非首屏资源？
```

---

## 模式 5：结构化数据不生效

### 症状识别

- 实施了结构化数据但 Rich Snippet 不出现
- GSC 结构化数据报告显示错误
- Rich Results Test 显示问题

### 预检信号

| 信号 | 检查方式 | 阈值 |
|------|---------|------|
| 结构化数据错误 | GSC 增强功能 | 存在错误项 |
| 结构化数据警告 | GSC 增强功能 | 存在警告项 |
| 缺失必填字段 | Schema.org 验证 | 任一类型缺必填字段 |

### 重点关注专家

| 优先级 | 专家 | 检查要点 |
|--------|------|---------|
| P0 | Schema | JSON-LD 语法是否正确？必填属性是否完整？ |
| P1 | Indexability | 页面是否被索引？结构化数据所在页面是否可访问？ |
| P2 | Meta | 结构化数据中的信息是否与页面可见内容一致？ |

### 类型特定诊断

| 类型 | 常见问题 | 必填属性 |
|------|---------|---------|
| Product | 缺少 price / review | name, price, priceCurrency |
| Article | 缺少 author / datePublished | headline, datePublished, author |
| Recipe | 缺少 image / prepTime | name, image, recipeIngredient |
| FAQPage | 问题数量 < 2 | mainEntity (≥ 2 个 Question) |
| Event | 缺少 startDate / location | name, startDate, location |
| LocalBusiness | 缺少 address / phone | name, address, telephone |
| BreadcrumbList | 最后一项添加了 URL | itemListElement (≥ 2) |
| Review | 缺少 reviewRating 或 author | reviewRating, author |

### 验证流程

```
1. 用 Rich Results Test 测试单页
2. 检查 JSON-LD 是否在 <head> 中
3. 验证 @type 拼写正确
4. 验证必填属性完整
5. 验证属性值格式正确（日期 ISO 8601、价格数字）
6. 确认结构化数据内容与页面可见内容一致
7. 在 GSC 中提交验证修复
```

---

## 模式 6：页面速度不达标

### 症状识别

- PageSpeed Insights 评分 < 50
- 用户反馈加载缓慢
- GSC Core Web Vitals 报告显示大量"需要改进"或"欠佳"

### 严重程度判断

| 指标 | 良好 | 需要改进 | 欠佳 |
|------|------|---------|------|
| LCP | ≤ 2.5s | 2.5s – 4.0s | > 4.0s |
| INP | ≤ 200ms | 200ms – 500ms | > 500ms |
| CLS | ≤ 0.1 | 0.1 – 0.25 | > 0.25 |
| TTFB | ≤ 800ms | 800ms – 1.8s | > 1.8s |
| FCP | ≤ 1.8s | 1.8s – 3.0s | > 3.0s |

### 重点关注专家

| 优先级 | 专家 | 检查要点 |
|--------|------|---------|
| P0 | Core Web Vitals | 各指标是否达标？瓶颈在哪个环节？ |
| P0 | Resource | JS/CSS 是否压缩？是否启用缓存？是否使用 CDN？ |
| P1 | Image | 图片格式（WebP/AVIF）？是否有尺寸声明？是否懒加载？ |
| P2 | Mobile | 移动端性能是否额外优化？ |

### 优化优先级

```
P0（立即执行，预计提升最明显）：
□ 压缩图片（转换为 WebP/AVIF）
□ 启用文本压缩（Gzip/Brotli）
□ 设置合理的缓存头（Cache-Control）

P1（本周内）：
□ 移除未使用的 JS/CSS
□ 延迟加载非关键资源（lazy loading）
□ 优化服务器响应时间（TTFB）
□ 为图片/iframe 预留尺寸空间（防止 CLS）

P2（本月内）：
□ 实施代码分割（Code Splitting）
□ 使用 Service Worker 缓存
□ 优化第三方脚本加载（延迟/异步）
□ 升级到 HTTP/2 或 HTTP/3
```

---

## 模式 7：惩罚风险 — 黑帽信号

### 症状识别

- 发现疑似黑帽 SEO 手法
- 排名突然消失（非算法更新期间）
- 外链 profile 异常（大量低质外链）

### 黑帽信号清单

```
□ 购买链接（付费外链、链接交换过量）
□ PBN（Private Blog Network）参与
□ 关键词堆砌（keyword stuffing）
□ 隐藏文本/链接（与背景同色、font-size: 0、display: none）
□ Cloaking（对搜索引擎和用户展示不同内容）
□ 内容农场（大量低质自动生成内容）
□ 门页（Doorway Pages — 为搜索引擎创建的大量低质入口页）
□ 垃圾评论（UGC 中的垃圾外链）
□ 恶意重定向（用户点击后跳转至无关页面）
□ 结构化数据垃圾（标记内容与实际不符）
```

### 重点关注专家

| 优先级 | 专家 | 检查要点 |
|--------|------|---------|
| P0 | Security | 是否有隐藏文本/链接？是否有 cloaking？是否有恶意脚本？ |
| P0 | Backlink | 外链来源是否异常？锚文本是否过度优化？是否有 link farm？ |
| P0 | Content | 是否有大量低质/自动生成内容？是否有 doorway pages？ |
| P1 | Schema | 结构化数据是否与实际内容一致？ |
| P1 | UX | 是否有欺骗性导航/重定向？ |

### 风险评估矩阵

| 信号 | 风险等级 | 应对 |
|------|---------|------|
| 发现 1 个黑帽信号 | 中 | 立即排查，确认范围 |
| 发现 2-3 个黑帽信号 | 高 | 启动专项清理，审计所有页面 |
| 发现 3+ 个黑帽信号 | 严重 | 全站排查，考虑专业 SEO 安全团队介入 |
| 已收到手动操作通知 | 严重 | 立即全面清理，准备复议材料 |

**352 否决规则触发条件：** 一旦确认任一黑帽信号属实，总分最高 50 分，等级强制"不合格"。

---

## 诊断工具速查

| 工具 | 用途 | 适用模式 |
|------|------|---------|
| PageSpeed Insights API | CWV 真实数据 | `--api-key` |
| Google Search Console | 索引/流量/手动操作 | `--gsc` |
| Google Analytics 4 | 用户行为/转化 | `--ga4` |
| site:domain.com | 快速检查收录 | 远程模式 |
| Rich Results Test | 结构化数据验证 | 远程模式 |
| robots.txt 检查 | 爬取规则 | 远程/本地 |
| 源码扫描 | 标签/标记审查 | 本地模式 |

---

*最后更新: 2025-05-31*
*基于 SEO 352 黄金法则框架，结合 17 位专家审计经验积累*