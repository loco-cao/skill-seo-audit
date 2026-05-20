# 完整 SEO 审计工作流

<purpose>
执行完整的 SEO 多专家审查工作流。
默认流程：跨 14 个维度分四批并行审查 → API 数据增强（可选）→ 加权汇总 → 报告生成
</purpose>

<required_reading>
@$HOME/.claude/seo-audit/references/api-integration-guide.md
@$HOME/.claude/seo-audit/shared/seo-audit.md
</required_reading>

<available_agent_types>
- seo-crawlability-expert — 爬取通道审查
- seo-indexability-expert — 索引管理审查
- seo-architecture-expert — 网站架构审查
- seo-meta-expert — Meta 标签审查
- seo-heading-expert — 标题层级审查
- seo-image-expert — 图片优化审查
- seo-content-expert — 内容质量审查
- seo-eeat-expert — E-E-A-T 信号审查
- seo-core-web-vitals-expert — Core Web Vitals 审查
- seo-resource-expert — 资源优化审查
- seo-schema-expert — 结构化数据审查
- seo-mobile-expert — 移动优化审查
- seo-security-expert — 安全审查
- seo-ux-expert — 用户体验审查
</available_agent_types>

<process>

## 1. 初始化

定义会话目录：

```bash
SESSION_DIR=".seo-audit/session-$(date +%Y%m%d-%H%M%S)"
```

无需手动创建子目录。Write 工具写入文件时会自动创建缺失的目录。

目录结构预期：
```
SESSION_DIR/
├── 01-crawlability/
├── 02-indexability/
├── 03-architecture/
├── 04-meta/
├── 05-heading/
├── 06-image/
├── 07-content/
├── 08-eeat/
├── 09-core-web-vitals/
├── 10-resource/
├── 11-schema/
├── 12-mobile/
├── 13-security/
├── 14-ux/
└── 99-summary/
```

## 2. 分四批并行审查

14 位专家分四批，每批内并行，批间串行。

**第一批（基础面）— 并行启动：**

| 专家 | 输出路径 |
|--------|-------------|
| @seo-crawlability-expert | 01-crawlability/report.json |
| @seo-indexability-expert | 02-indexability/report.json |
| @seo-architecture-expert | 03-architecture/report.json |
| @seo-meta-expert | 04-meta/report.json |

**第二批（元素与内容面）— 第一批完成后并行启动：**

| 专家 | 输出路径 |
|--------|-------------|
| @seo-heading-expert | 05-heading/report.json |
| @seo-image-expert | 06-image/report.json |
| @seo-content-expert | 07-content/report.json |
| @seo-eeat-expert | 08-eeat/report.json |

**第三批（技术与数据面）— 第二批完成后并行启动：**

| 专家 | 输出路径 |
|--------|-------------|
| @seo-core-web-vitals-expert | 09-core-web-vitals/report.json |
| @seo-resource-expert | 10-resource/report.json |
| @seo-schema-expert | 11-schema/report.json |
| @seo-mobile-expert | 12-mobile/report.json |

**第四批（安全与体验面）— 第三批完成后并行启动：**

| 专家 | 输出路径 |
|--------|-------------|
| @seo-security-expert | 13-security/report.json |
| @seo-ux-expert | 14-ux/report.json |

## 3. API 数据增强（可选）

若用户配置了 API，在批次执行期间或之后运行：

- **PageSpeed Insights**：`node scripts/pagespeed.js <url> <API_KEY>`
  - 结果保存到 `SESSION_DIR/api-pagespeed.json`
  - 供 `seo-core-web-vitals-expert` 参考

- **Google Search Console**：`node scripts/gsc.js --site <url> --all --days 28`
  - 结果保存到 `SESSION_DIR/api-gsc.json`
  - 供 `seo-crawlability-expert`、`seo-content-expert`、`seo-meta-expert` 参考

- **Google Analytics 4**：`node scripts/ga4.js --property <ID> --all --days 28`
  - 结果保存到 `SESSION_DIR/api-ga4.json`
  - 供 `seo-content-expert`、`seo-ux-expert`、`seo-eeat-expert` 参考

## 4. 等待完成

轮询直到全部 14 个 `report.json` 文件存在。如果有专家在重试一次后仍失败，记分为 0 并记录失败。

## 5. 分数汇总

读取所有报告。使用固定权重计算加权总分：

- crawlability: 15%
- indexability: 12%
- architecture: 10%
- meta: 7%
- heading: 5%
- image: 4%
- content: 12%
- eeat: 8%
- core-web-vitals: 7%
- resource: 4%
- schema: 5%
- mobile: 4%
- security: 4%
- ux: 3%

**否决规则：**
- crawlability < 50 → 最终等级强制不超过"待提升"
- indexability < 50 → 总分扣减 10 分

等级划分：优秀(≥95) · 待提升(90–94) · 基本满足(80–89) · 不合格(<80)

## 6. 生成交付物

在 `99-summary/` 中产出：

- `report-final.json` — 结构化数据
- `report-final.html` — 可视化仪表板（雷达图、等级徽章、逐维度明细、严重问题列表）
- `action-plan.md` — 按 Critical/High/Medium/Low 分组的行动计划

## 7. 终端输出

向用户终端输出简洁的分数摘要。

</process>
