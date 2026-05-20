# SEO Audit — Agent 拆分设计思路

> 基于 `adsense-lint` 模式设计的 `seo-audit` 多专家审计系统。
> **原则：一个专家负责一个独立的面（主题/一类内容），不交叉、不重叠。**

---

## 一、adsense-lint 的结构模式（复用基准）

| 层级 | 文件 | 职责 |
|------|------|------|
| 协议层 | `ait.yaml` | skill 元数据、双平台安装映射、参数定义 |
| 入口层 | `claude/SKILL.md` + `codex/SYSTEM.md` | 平台适配：Claude 用 `Agent()` 并行调度，Codex 自行顺序执行 |
| 核心层 | `shared/seo-audit.md` | 平台无关的编排逻辑、批次策略、进度上报规范、汇总规则 |
| 工作流 | `workflows/full-audit.md` | 完整审计流程的声明式定义 |
| 专家层 | `claude/agents/*.md` | 14 位 expert 的独立能力定义（角色、评估维度、评分指南、输出格式） |
| 参考层 | `references/*.md` | 各 expert 专属参考资料、评分标准、报告模板 |

---

## 二、seo-audit 的 14 个 Expert 拆分方案

每个 expert 负责一个**独立的面**，职责边界清晰，不重叠。

| # | Expert | 负责的面 | 权重 | 批次 |
|---|--------|---------|------|------|
| 1 | `seo-crawlability-expert` | **爬取通道面** — robots.txt、重定向链、死链、抓取错误、HTTP 状态码 | 15% | 第一批 |
| 2 | `seo-indexability-expert` | **索引管理面** — canonical、noindex、hreflang、sitemap、重复内容 | 12% | 第一批 |
| 3 | `seo-architecture-expert` | **网站架构面** — URL 结构、层级、面包屑、内链、孤立页面、锚文本 | 10% | 第一批 |
| 4 | `seo-meta-expert` | **Meta 标签面** — title、meta description、OG、Twitter Cards、viewport、charset | 7% | 第一批 |
| 5 | `seo-heading-expert` | **标题层级面** — H1-H6 结构、层级逻辑、关键词分布 | 5% | 第二批 |
| 6 | `seo-image-expert` | **图片优化面** — alt 文本、文件名、格式、懒加载、尺寸声明、CLS 影响 | 4% | 第二批 |
| 7 | `seo-content-expert` | **内容质量面** — 原创性、深度、可读性、thin content、更新频率、意图匹配 | 12% | 第二批 |
| 8 | `seo-eeat-expert` | **E-E-A-T 面** — 作者署名、资质证明、引用来源、经验信号、YMYL 领域 | 8% | 第二批 |
| 9 | `seo-core-web-vitals-expert` | **Core Web Vitals 面** — LCP、INP、CLS、TTFB | 7% | 第三批 |
| 10 | `seo-resource-expert` | **资源优化面** — JS/CSS 压缩、缓存头、CDN、阻塞渲染资源 | 4% | 第三批 |
| 11 | `seo-schema-expert` | **结构化数据面** — JSON-LD、Schema.org、Rich Snippets、验证 | 5% | 第三批 |
| 12 | `seo-mobile-expert` | **移动优化面** — 响应式、viewport、触摸目标、移动可用性 | 4% | 第三批 |
| 13 | `seo-security-expert` | **安全面** — HTTPS、HSTS、安全头、混合内容 | 4% | 第四批 |
| 14 | `seo-ux-expert` | **用户体验面** — 导航、搜索、404、CTA、社交分享、布局 | 3% | 第四批 |

### 为什么拆成 14 个？

**信息架构面（3 个）**：SEO 的根基。把"能不能被抓到"和"能不能被索引"拆成两个独立面，加上"网站结构是否合理"，三个面互不重叠。

**页面元素面（3 个）**：Meta、Heading、Image 各自是独立的检查面，不需要放在一个"onpage"大杂烩里。

**内容质量面（2 个）**：Content 和 E-E-A-T 分开，前者是"内容本身好不好"，后者是"谁写的、可不可信"，评判标准完全不同。

**技术性能面（2 个）**：CWV 是 Google 明确的排名因素，资源优化是工程实践，关注点不同。

**数据标记 + 设备适配（2 个）**：Schema 和 Mobile 各自独立。

**安全 + 体验（2 个）**：Security 是硬门槛，UX 是软体验，分开更精准。

### 分批执行策略

14 个 expert 分 **四批**，每批内并行，批间串行：

- **第一批（基础面）**：crawlability → indexability → architecture → meta
- **第二批（元素与内容面）**：heading → image → content → eeat
- **第三批（技术与数据面）**：cwv → resource → schema → mobile
- **第四批（安全与体验面）**：security → ux

每批内 4 个 Agent 调用在同一轮 tool calls 中发出（Claude 并行模式）。

### 否决权规则

| Expert | 否决权类型 | 规则 |
|--------|-----------|------|
| `seo-crawlability-expert` | **一级否决** | 分数 < 50 → 最终等级强制不超过"待提升" |
| `seo-indexability-expert` | **二级否决** | 分数 < 50 → 总分扣减 10 分 |

---

## 三、每个 Expert 的内部结构

每个 `claude/agents/seo-xxx-expert.md` 遵循统一模板：

```markdown
---
name: seo-crawlability-expert
description: 爬取通道专家。检查 robots.txt、重定向链、死链、HTTP状态码和抓取错误。
tools:
  - Read
  - Write
  - WebFetch
  - Bash
  - Grep
color: blue
---

# seo-crawlability-expert

你是爬取通道专家。

## 角色
验证搜索引擎能否正确发现和访问网站页面。这是 SEO 审计的第一道关卡。

## 评估维度
（按该 expert 负责的面，列出具体检查项）

## 弹性与超时规则
（复用统一模式：WebFetch 15秒超时、curl --max-time 15、3次重试、60秒总超时写失败报告）

## 评分指南
- 90–100：优秀
- 70–89：良好
- 60–69：有风险
- 0–59：严重

## 输出
（复用统一 report.json 格式）
```

---

## 四、Claude vs Codex 的关键差异适配

| 平台 | 调度方式 | 入口文件职责 |
|------|---------|-------------|
| **Claude** | `Agent(subagent_type="seo-xxx-expert")` 并行/串行调度 | SKILL.md 是"编排器"：分四批启动 agent、探测并行度、汇总报告 |
| **Codex** | 无 Agent 子代理，**自行逐维度分析** | SYSTEM.md 是"执行者"：按顺序审完 14 个面，每面产出 report.json |

**Codex 的 SYSTEM.md**：不用写复杂的批次逻辑，按权重从高到低顺序执行 14 个面。每面审完后写 report.json，全部完成后汇总。

---

## 五、建议的文件结构

```
seo-audit/
├── ait.yaml
├── claude/
│   ├── SKILL.md                          # 入口编排（Agent 并行调度）
│   └── agents/
│       ├── seo-crawlability-expert.md    # 15%
│       ├── seo-indexability-expert.md    # 12%
│       ├── seo-architecture-expert.md    # 10%
│       ├── seo-meta-expert.md            # 7%
│       ├── seo-heading-expert.md         # 5%
│       ├── seo-image-expert.md           # 4%
│       ├── seo-content-expert.md         # 12%
│       ├── seo-eeat-expert.md            # 8%
│       ├── seo-core-web-vitals-expert.md # 7%
│       ├── seo-resource-expert.md        # 4%
│       ├── seo-schema-expert.md          # 5%
│       ├── seo-mobile-expert.md          # 4%
│       ├── seo-security-expert.md        # 4%
│       └── seo-ux-expert.md              # 3%
├── codex/
│   └── SYSTEM.md                         # 入口执行（逐维度顺序分析）
├── shared/
│   └── seo-audit.md                      # 核心审计逻辑（平台无关）
├── workflows/
│   └── full-audit.md                     # 完整工作流定义
├── references/
│   ├── crawlability-guide.md             # 爬取通道专家参考
│   ├── indexability-guide.md             # 索引管理专家参考
│   ├── architecture-guide.md             # 网站架构专家参考
│   ├── meta-guide.md                     # Meta标签专家参考
│   ├── heading-guide.md                  # 标题层级专家参考
│   ├── image-guide.md                    # 图片优化专家参考
│   ├── content-guide.md                  # 内容质量专家参考
│   ├── eeat-guide.md                     # E-E-A-T专家参考
│   ├── core-web-vitals-guide.md          # CWV专家参考
│   ├── resource-guide.md                 # 资源优化专家参考
│   ├── schema-guide.md                   # 结构化数据专家参考
│   ├── mobile-guide.md                   # 移动优化专家参考
│   ├── security-guide.md                 # 安全专家参考
│   ├── ux-guide.md                       # 用户体验专家参考
│   ├── scoring-rubric.md                 # 评分标准
│   └── report-template.md                # 报告模板
└── README.md
```

---

## 六、各 Expert 详细评估维度速查

### seo-crawlability-expert（15%）
- robots.txt 存在性与合法性
- 是否错误阻止 Googlebot
- 是否包含 Sitemap 引用
- 重定向链与循环检测
- 404/500 死链检测
- HTTP 状态码正确性
- 抓取错误类型统计

### seo-indexability-expert（12%）
- canonical 标签正确性
- noindex/nofollow 误用
- sitemap.xml 存在性与格式
- 重复内容检测
- hreflang 配置（多语言站点）
- 索引状态推断

### seo-architecture-expert（10%）
- URL 结构语义化
- URL 层级深度（建议 ≤3 层）
- 面包屑导航
- 内链架构完整性
- 孤立页面检测
- 锚文本描述性

### seo-meta-expert（7%）
- title tag：存在性、长度（50-60字符）、关键词前置
- meta description：存在性、长度（150-160字符）
- Open Graph 标签完整性
- Twitter Cards 配置
- viewport meta 正确性
- charset 声明

### seo-heading-expert（5%）
- H1 唯一性
- H1-H6 层级逻辑
- 关键词在标题中的分布
- 标题与内容匹配度

### seo-image-expert（4%）
- alt 文本存在性与描述性
- 文件名语义化
- 格式优化（WebP/AVIF）
- 懒加载实现
- 尺寸声明（防止 CLS）

### seo-content-expert（12%）
- 内容深度（每页 >300 词）
- 原创性与独特性
- 搜索意图匹配度
- 可读性（段落、句式、结构）
- Thin content 检测
- 更新频率与时效性

### seo-eeat-expert（8%）
- 作者署名存在性
- 作者资质证明
- 引用来源与外链质量
- 经验信号（第一手经验）
- YMYL 领域特殊要求
- 关于页面深度

### seo-core-web-vitals-expert（7%）
- LCP < 2.5s
- INP < 200ms
- CLS < 0.1
- TTFB < 600ms
- 各指标测量与推断

### seo-resource-expert（4%）
- JS/CSS 压缩与合并
- 渲染阻塞资源检测
- 缓存头配置
- CDN 使用
- 资源大小控制

### seo-schema-expert（5%）
- JSON-LD 存在性与格式
- Schema.org 类型正确性
- Rich Snippets 资格
- Open Graph / Twitter Cards（与 meta expert 协同）
- 结构化数据验证

### seo-mobile-expert（4%）
- viewport meta
- 响应式 CSS
- 移动端字体可读性
- 触摸目标大小（>48px）
- 移动可用性错误
- AMP 实现（如有）

### seo-security-expert（4%）
- HTTPS 强制与 HSTS
- 安全头配置（CSP、X-Frame-Options 等）
- 混合内容检测
- 可疑脚本与 iframe

### seo-ux-expert（3%）
- 导航结构清晰性
- 站内搜索功能
- 面包屑导航
- 404 页面友好性
- CTA 清晰度
- 社交分享按钮
- 页面布局逻辑性
