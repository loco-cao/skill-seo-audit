---
name: seo-audit
description: "SEO 多专家 AI 审计系统 — 14 位领域专家并行审计网站或本地项目"
argument-hint: "<url> [--local] [--auto] [--api-key KEY] [--gsc] [--ga4 PROPERTY_ID]"
allowed-tools:
  - Read
  - Write
  - Bash
  - AskUserQuestion
  - Agent
  - Grep
  - Glob
---

# SEO Audit Skill

你是 SEO 多专家 AI 审查系统的入口点。

## 启动

首先，读取核心审计指令：

```
Read: shared/seo-audit.md
```

该文件包含完整的审计流程：参数解析、模式判断、飞行前检查、会话设置、专家编排、API 数据增强、汇总规则和输出格式。按其中定义的逻辑执行。

## Claude-Specific 适配

以下是与 Claude Code 平台绑定的具体实现细节。

### 飞行前检查 — 文件验证

验证工作流和参考文件存在：

```bash
SKILL_DIR="$HOME/.claude/skills/seo-audit"
test -f "$SKILL_DIR/references/crawlability-guide.md" && echo "OK: crawlability" || echo "MISSING: crawlability"
test -f "$SKILL_DIR/references/indexability-guide.md" && echo "OK: indexability" || echo "MISSING: indexability"
test -f "$SKILL_DIR/references/api-integration-guide.md" && echo "OK: api-guide" || echo "MISSING: api-guide"
```

如有缺失：**立即停止**，提示用户运行 `ait install` 重新安装。

### 分四批并行启动 14 位专家

为避免单次并行过多导致 timeout，将 14 位专家分为四批，每批 4/4/4/2 个。每批完成后立即启动下一批。

**第一批（基础面）：**

| 专家 | subagent_type | 输出路径 |
|------|--------------|----------|
| Crawlability | `seo-crawlability-expert` | `<SESSION_DIR>/01-crawlability/report.json` |
| Indexability | `seo-indexability-expert` | `<SESSION_DIR>/02-indexability/report.json` |
| Architecture | `seo-architecture-expert` | `<SESSION_DIR>/03-architecture/report.json` |
| Meta | `seo-meta-expert` | `<SESSION_DIR>/04-meta/report.json` |

**第二批（元素与内容面）：**

| 专家 | subagent_type | 输出路径 |
|------|--------------|----------|
| Heading | `seo-heading-expert` | `<SESSION_DIR>/05-heading/report.json` |
| Image | `seo-image-expert` | `<SESSION_DIR>/06-image/report.json` |
| Content | `seo-content-expert` | `<SESSION_DIR>/07-content/report.json` |
| E-E-A-T | `seo-eeat-expert` | `<SESSION_DIR>/08-eeat/report.json` |

**第三批（技术与数据面）：**

| 专家 | subagent_type | 输出路径 |
|------|--------------|----------|
| Core Web Vitals | `seo-core-web-vitals-expert` | `<SESSION_DIR>/09-core-web-vitals/report.json` |
| Resource | `seo-resource-expert` | `<SESSION_DIR>/10-resource/report.json` |
| Schema | `seo-schema-expert` | `<SESSION_DIR>/11-schema/report.json` |
| Mobile | `seo-mobile-expert` | `<SESSION_DIR>/12-mobile/report.json` |

**第四批（安全与体验面）：**

| 专家 | subagent_type | 输出路径 |
|------|--------------|----------|
| Security | `seo-security-expert` | `<SESSION_DIR>/13-security/report.json` |
| UX | `seo-ux-expert` | `<SESSION_DIR>/14-ux/report.json` |

### API 数据增强触发

如果用户提供了 `--api-key`，在第一批启动后（或并行）执行：
```bash
node "$SKILL_DIR/scripts/pagespeed.js" <url> <api_key> > <SESSION_DIR>/api-pagespeed.json 2>/dev/null
```

如果启用了 `--gsc` 且 `scripts/config/gsc_service_account.json` 存在：
```bash
node "$SKILL_DIR/scripts/gsc.js" --site <url> --all --days 28 > <SESSION_DIR>/api-gsc.json 2>/dev/null
```

如果启用了 `--ga4` 且 `scripts/config/ga4_service_account.json` 存在：
```bash
node "$SKILL_DIR/scripts/ga4.js" --property <ga4_property> --all --days 28 > <SESSION_DIR>/api-ga4.json 2>/dev/null
```

**API 调用失败不阻塞审计。** 若失败，相关 expert 降级为纯页面扫描模式。

### 调用示例（远程模式）

```
Agent(subagent_type="seo-crawlability-expert", description="Crawlability audit",
  prompt="审查 <url>。将结果写入 <SESSION_DIR>/01-crawlability/report.json。评分 0-100。输出合法 JSON，字段：expert, score, maxScore, weight, status, findings[], summary。每个 finding 必须有 severity/category/title/description/evidence/recommendation。执行期间在关键步骤更新 <SESSION_DIR>/01-crawlability/status.json。")
```

### 调用示例（本地模式）

```
Agent(subagent_type="seo-crawlability-expert", description="Crawlability audit",
  prompt="你是爬取通道专家。这是本地代码审查——不要使用 WebFetch。使用 Read 和 Grep 扫描项目 <project_path> 中的 robots.txt、HTML/JSX/TSX/Vue 文件，检查重定向配置、死链、HTTP 状态码。将结果写入 <SESSION_DIR>/01-crawlability/report.json。评分 0-100。输出合法 JSON。")
```

**关键：每批 4 个 Agent 调用必须在同一轮中发出，利用并行 tool calls。批次间串行，等前一批全部完成后再发下一批。不得使用中介 agent 做编排。**

### 超时与重试

等待每批 Agent 返回结果：
- 若某位专家返回 **timeout** 或 **failed**，在发下一批之前单独对该专家**重试一次**。
- 重试时精简 prompt，仅保留核心审查指令和输出路径，避免重复说明背景规则。
- 若重试仍失败，汇总阶段为该专家写入备用 report.json：
  - `score: 0`, `status: "failed"`
  - 一条 critical 发现，标题 `审计执行失败`，描述说明超时或失败原因。
- **不要因为单个专家失败而阻塞整体审计。**

### 交互确认

远程模式下，如果未指定 `--auto`，使用 `AskUserQuestion` 向用户确认 URL 和审计范围。

### 汇总

参考 `shared/seo-audit.md` 中的评分公式和输出格式，生成 `report-final.json`、`report-final.html` 和 `action-plan.md`。