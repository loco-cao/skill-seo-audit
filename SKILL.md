---
name: seo-audit
description: "SEO 多专家 AI 审计系统 — 17 位领域专家分五批并行审计网站或本地项目，覆盖技术SEO、内容、外链、竞品与数据解读"
argument-hint: "<url> [--local] [--auto] [--api-key KEY] [--gsc] [--ga4 PROPERTY_ID] [--competitor DOMAIN1,DOMAIN2]"
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

你是 SEO 多专家 AI 审查系统的入口点。本系统基于 SEO 352 黄金法则，通过 17 位领域专家覆盖技术SEO、On-Page、内容质量、外链、竞品分析与数据解读六大维度。

## 启动

首先，读取核心审计指令：

```
Read: shared/seo-audit.md
```

该文件包含完整的审计流程：参数解析、模式判断、飞行前检查、会话设置、专家编排（五批并行）、API 数据增强、352框架汇总规则和输出格式。按其中定义的逻辑执行。

## Claude-Specific 适配

### 飞行前检查 — 文件验证

验证工作流和参考文件存在。使用 Read 工具依次检查以下文件（跨平台，不依赖 shell）：

| 文件路径 | 用途 |
|----------|------|
| `references/crawlability-guide.md` | 爬取通道审查指南 |
| `references/backlink-guide.md` | 外链质量审查指南 |
| `references/competitor-guide.md` | 竞品分析指南 |
| `references/seo-352-framework.md` | SEO 352 黄金法则框架 |
| `references/api-integration-guide.md` | API 集成指南 |

**检查方式**（二选一，根据平台自动选择）：

**macOS / Linux (Bash):**
```bash
SKILL_DIR="$HOME/.claude/skills/seo-audit"
for f in crawlability-guide backlink-guide competitor-guide seo-352-framework api-integration-guide; do
  if [ -f "$SKILL_DIR/references/$f.md" ]; then
    echo "OK: $f"
  else
    echo "MISSING: $f"
  fi
done
```

**Windows (PowerShell):**
```powershell
$SKILL_DIR = "$env:USERPROFILE\.claude\skills\seo-audit"
@("crawlability-guide","backlink-guide","competitor-guide","seo-352-framework","api-integration-guide") | ForEach-Object {
  if (Test-Path "$SKILL_DIR\references\$_.md") {
    Write-Output "OK: $_"
  } else {
    Write-Output "MISSING: $_"
  }
}
```

**注意：严禁混用语法！** Bash 中用 `&&`/`||`/`echo`，PowerShell 中用 `Test-Path`/`Write-Output`。在 Windows 上必须使用 PowerShell 版本，不要在 Bash 中使用 `Write-Output` 或 `-and`/`-or`。

如有缺失：**立即停止**，提示用户运行 `cct install` 重新安装。

### 分五批并行启动 17 位专家

将 17 位专家分为五批，每批内并行，批间串行。每批完成后立即启动下一批。

**第一批（基础面 — 4位）：**

| 专家 | subagent_type | 权重 | 输出路径 |
|------|--------------|------|----------|
| Crawlability | `seo-crawlability-expert` | 12% | `<SESSION_DIR>/01-crawlability/report.json` |
| Indexability | `seo-indexability-expert` | 10% | `<SESSION_DIR>/02-indexability/report.json` |
| Architecture | `seo-architecture-expert` | 8% | `<SESSION_DIR>/03-architecture/report.json` |
| Meta | `seo-meta-expert` | 6% | `<SESSION_DIR>/04-meta/report.json` |

**第二批（元素与内容面 — 4位）：**

| 专家 | subagent_type | 权重 | 输出路径 |
|------|--------------|------|----------|
| Heading | `seo-heading-expert` | 4% | `<SESSION_DIR>/05-heading/report.json` |
| Image | `seo-image-expert` | 3% | `<SESSION_DIR>/06-image/report.json` |
| Content | `seo-content-expert` | 10% | `<SESSION_DIR>/07-content/report.json` |
| E-E-A-T | `seo-eeat-expert` | 7% | `<SESSION_DIR>/08-eeat/report.json` |

**第三批（技术与数据面 — 4位）：**

| 专家 | subagent_type | 权重 | 输出路径 |
|------|--------------|------|----------|
| Core Web Vitals | `seo-core-web-vitals-expert` | 6% | `<SESSION_DIR>/09-core-web-vitals/report.json` |
| Resource | `seo-resource-expert` | 3% | `<SESSION_DIR>/10-resource/report.json` |
| Schema | `seo-schema-expert` | 4% | `<SESSION_DIR>/11-schema/report.json` |
| Mobile | `seo-mobile-expert` | 3% | `<SESSION_DIR>/12-mobile/report.json` |

**第四批（安全、体验与外链 — 3位）：**

| 专家 | subagent_type | 权重 | 输出路径 |
|------|--------------|------|----------|
| Security | `seo-security-expert` | 3% | `<SESSION_DIR>/13-security/report.json` |
| UX | `seo-ux-expert` | 3% | `<SESSION_DIR>/14-ux/report.json` |
| Backlink | `seo-backlink-expert` | 8% | `<SESSION_DIR>/15-backlink/report.json` |

**第五批（策略面 — 2位）：**

| 专家 | subagent_type | 权重 | 输出路径 |
|------|--------------|------|----------|
| Competitor | `seo-competitor-expert` | 5% | `<SESSION_DIR>/16-competitor/report.json` |
| Data | `seo-data-expert` | 5% | `<SESSION_DIR>/17-data/report.json` |

### API 数据增强触发

如果用户提供了 `--api-key`，在第一批启动后执行：
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

### 竞品数据增强

如果用户提供了 `--competitor`，将竞品域名列表传递给 `seo-competitor-expert` 和 `seo-data-expert`。

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

**关键：每批 Agent 调用必须在同一轮中发出，利用并行 tool calls。批次间串行，等前一批全部完成后再发下一批。不得使用中介 agent 做编排。**

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

参考 `shared/seo-audit.md` 中的 352 框架评分公式和输出格式，生成：
- `<SESSION_DIR>/99-summary/report-final.json`
- `<SESSION_DIR>/99-summary/report-final.html`
- `<SESSION_DIR>/99-summary/action-plan.md`
- `<SESSION_DIR>/99-summary/seo-352-report.md`（352框架专项报告）
