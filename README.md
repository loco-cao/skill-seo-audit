# SEO Audit — 多专家 AI 审计系统

基于 **SEO 352 黄金法则** 的 17 位领域专家并行审计系统。支持远程网站和本地项目两种模式，覆盖技术SEO、On-Page、内容质量、外链、竞品分析与数据解读六大维度。

## 架构概览

```
skill-seo-audit/
├── SKILL.md                          # Claude Code 入口点
├── cct.yaml                          # Skill 元数据与安装配置
├── README.md                         # 本文档
├── shared/
│   └── seo-audit.md                  # 平台无关的核心审计逻辑
├── agents/                           # 17 位领域专家 Agent
│   ├── seo-crawlability-expert.md    #   爬取通道
│   ├── seo-indexability-expert.md    #   索引管理
│   ├── seo-architecture-expert.md    #   网站架构
│   ├── seo-meta-expert.md            #   Meta 标签与 TDKU
│   ├── seo-heading-expert.md         #   标题层级
│   ├── seo-image-expert.md           #   图片优化
│   ├── seo-content-expert.md         #   内容质量
│   ├── seo-eeat-expert.md            #   E-E-A-T 信号
│   ├── seo-core-web-vitals-expert.md #   Core Web Vitals
│   ├── seo-resource-expert.md        #   资源优化
│   ├── seo-schema-expert.md          #   结构化数据
│   ├── seo-mobile-expert.md          #   移动优化
│   ├── seo-security-expert.md        #   安全合规
│   ├── seo-ux-expert.md              #   用户体验
│   ├── seo-backlink-expert.md        #   外链质量
│   ├── seo-competitor-expert.md      #   竞品分析
│   └── seo-data-expert.md            #   数据解读与报告
├── references/                       # 20 份参考指南
│   ├── crawlability-guide.md         #   爬取通道审查指南
│   ├── indexability-guide.md         #   索引管理审查指南
│   ├── architecture-guide.md         #   网站架构审查指南
│   ├── meta-guide.md                 #   Meta 标签审查指南
│   ├── heading-guide.md              #   标题层级审查指南
│   ├── image-guide.md               #   图片优化审查指南
│   ├── content-guide.md             #   内容质量审查指南
│   ├── eeat-guide.md                #   E-E-A-T 评估指南
│   ├── core-web-vitals-guide.md     #   CWV 审查指南
│   ├── resource-guide.md            #   资源优化审查指南
│   ├── schema-guide.md              #   结构化数据审查指南
│   ├── mobile-guide.md              #   移动优化审查指南
│   ├── security-guide.md            #   安全合规审查指南
│   ├── ux-guide.md                  #   用户体验审查指南
│   ├── backlink-guide.md            #   外链质量评估指南
│   ├── competitor-guide.md          #   竞品分析指南
│   ├── report-guide.md              #   报告撰写与项目管理指南
│   ├── tdku-audit-framework.md      #   TDKU 审计框架
│   ├── seo-352-framework.md         #   352 黄金法则评估框架
│   └── api-integration-guide.md     #   API 集成指南
├── workflows/
│   └── full-audit.md                 # 完整审计工作流定义
├── scripts/                          # API 数据增强脚本
│   ├── pagespeed.js / pagespeed.py   #   PageSpeed Insights
│   ├── gsc.js / gsc.py              #   Google Search Console
│   ├── ga4.js / ga4.py              #   Google Analytics 4
│   └── trends.py                     #   Google Trends
└── docs/
    ├── SEO评估大纲.md                # 原始评估大纲
    └── seo-audit-专家知识点清单.md    # 17 位专家知识点清单
```

## 17 位专家体系

### 分五批并行执行

| 批次 | 专家 | 权重 | 核心职责 |
|------|------|------|----------|
| **1** | Crawlability | 12% | robots.txt、Sitemap、死链、重定向链、抓取预算 |
| **1** | Indexability | 10% | canonical、noindex、重复内容、hreflang、JS渲染 |
| **1** | Architecture | 8% | URL层级、内链、面包屑、关键模块布局、可抓取导航 |
| **1** | Meta | 6% | Title、Meta Description、OG、Twitter Cards、TDKU一致性 |
| **2** | Heading | 4% | H1唯一性、H1-H6层级、语义标记、关键词分布 |
| **2** | Image | 3% | Alt文本、图片格式、懒加载、尺寸声明、CLS预防 |
| **2** | Content | 10% | 原创度、搜索意图、内容深度、thin content、关键词布局 |
| **2** | E-E-A-T | 7% | Experience、Expertise、Authoritativeness、Trustworthiness |
| **3** | Core Web Vitals | 6% | LCP ≤2.5s、INP ≤200ms、CLS ≤0.1、HTTPS、PSI |
| **3** | Resource | 3% | JS/CSS压缩、缓存策略、CDN、阻塞渲染资源 |
| **3** | Schema | 4% | JSON-LD、必用Schema类型、富媒体资格、常见错误 |
| **3** | Mobile | 3% | 移动优先、响应式、触控目标、弹窗禁令、PWA |
| **4** | Security | 3% | HTTPS、HSTS、Security Headers、隐藏文本/链接检测 |
| **4** | UX | 3% | 导航、404处理、CTA、F型布局、UGC管理、转化路径 |
| **4** | Backlink | 8% | 外链质量、Toxic识别、锚文本分布、品牌建设、风险规避 |
| **5** | Competitor | 5% | 六维对比、内容差距、技术差距、机会识别、快速胜利 |
| **5** | Data | 5% | UX信号、GSC/GA4解读、风险评估、P0-P3分级、项目管理 |

**权重总和：100%**

## 评分体系

### 加权总分

总分为 17 位专家分数的加权求和：

```
total = crawlability×0.12 + indexability×0.10 + architecture×0.08 + meta×0.06
      + heading×0.04 + image×0.03 + content×0.10 + eeat×0.07
      + cwv×0.06 + resource×0.03 + schema×0.04 + mobile×0.03
      + security×0.03 + ux×0.03 + backlink×0.08
      + competitor×0.05 + data×0.05
```

### 等级划分

| 分数 | 等级 | 含义 |
|------|------|------|
| ≥90 | 优秀 | 维护为主，关注竞品动态 |
| 80–89 | 待提升 | 有明确优化空间 |
| 70–79 | 基本满足 | 存在明显问题需修复 |
| <70 | 不合格 | 需全面整改 |

### 否决规则

- 发现黑帽手法（购买链接、PBN、关键词堆砌、隐藏文本、Cloaking）→ **总分≤50**，强制不合格
- Crawlability < 50 → 最终等级不超过"待提升"
- Indexability < 50 → 总分扣减 10 分

### 352 框架评分

除加权总分外，系统同时输出 **352 黄金法则** 双维度评分：

**3大核心要素**：TDK合规性(30%) + 内容质量(40%) + 外链健康度(30%)

**5维优化检查**：技术SEO(30%) + On-Page(20%) + 内容(25%) + 外链(15%) + 体验(10%)

## 使用方式

### 远程模式 — 审计线上网站

```bash
# 基础审计
/seo-audit https://example.com

# 自动模式（跳过确认）
/seo-audit https://example.com --auto

# 启用 API 数据增强
/seo-audit https://example.com --api-key AIza... --gsc --ga4 123456789

# 含竞品分析
/seo-audit https://example.com --competitor competitor1.com,competitor2.com

# 完整增强模式
/seo-audit https://example.com --auto --api-key AIza... --gsc --ga4 123456789 --competitor rival.com
```

### 本地模式 — 审计开发中项目

```bash
# 在项目目录中运行
/seo-audit --local

# 自动模式
/seo-audit --local --auto
```

### 参数说明

| 参数 | 说明 | 要求 |
|------|------|------|
| `<url>` | 目标网站 URL | 必须 http/https 开头 |
| `--local` | 审计当前项目源代码 | 需在项目目录中 |
| `--auto` | 跳过交互确认 | — |
| `--api-key KEY` | PageSpeed Insights API Key | 免费，Google Cloud Console 创建 |
| `--gsc` | 启用 GSC 数据 | 需配置 Service Account |
| `--ga4 PROPERTY_ID` | 启用 GA4 数据 | 需配置 Service Account |
| `--competitor D1,D2` | 竞品域名列表 | 逗号分隔 |

## 交付物

每次审计在 `.seo-audit/session-<timestamp>/` 下生成：

| 文件 | 内容 |
|------|------|
| `01-17-*/report.json` | 各专家结构化评分报告 |
| `01-17-*/status.json` | 各专家执行进度 |
| `99-summary/report-final.json` | 汇总结构化数据（17维度 + 352框架） |
| `99-summary/report-final.html` | 可视化仪表板（雷达图、等级徽章、问题清单） |
| `99-summary/action-plan.md` | P0/P1/P2/P3 分级行动计划 |
| `99-summary/seo-352-report.md` | 352 黄金法则专项报告 |
| `api-pagespeed.json` | PSI 数据（如启用） |
| `api-gsc.json` | GSC 数据（如启用） |
| `api-ga4.json` | GA4 数据（如启用） |

## API 集成

支持 4 种免费 API 增强审计数据（**总成本：$0/月**）：

| API | 数据 | 增强的专家 |
|-----|------|-----------|
| PageSpeed Insights | 真实用户 CWV | Core Web Vitals |
| Google Search Console | 搜索查询、外链、索引状态 | Crawlability、Content、Meta、Backlink、Data |
| Google Analytics 4 | 互动率、停留时间、流量来源 | Content、UX、E-E-A-T、Data |
| Google Trends | 品牌搜索热度趋势 | E-E-A-T、Competitor |

API 调用失败不阻塞审计，相关专家降级为纯页面扫描模式。

详细配置见 `references/api-integration-guide.md`。

## 超时与容错

- 每批 Agent 等待完成后启动下一批
- 单 Agent 超时/失败 → 自动重试一次
- 重试仍失败 → 写入 score: 0、status: "failed" 备用报告
- **单个专家失败不阻塞整体审计**

## 安装

```bash
ait install seo-audit
```

## 版本

- **v0.2.0** — 17 位专家，五批并行，352 框架双轨评分
- v0.1.0 — 14 位专家，四批并行，单一加权评分

## 相关资源

- [SEO 352 黄金法则评估框架](references/seo-352-framework.md)
- [TDKU 审计框架](references/tdku-audit-framework.md)
- [专家知识点清单](docs/seo-audit-专家知识点清单.md)
- [API 集成指南](references/api-integration-guide.md)