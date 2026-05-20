#!/usr/bin/env node
/**
 * Google Analytics 4 Data API Client — 零依赖 Node.js 版本
 *
 * 使用 Service Account（服务账号）JWT 认证，无需浏览器 OAuth。
 *
 * 前置步骤:
 *   1. Google Cloud Console → IAM → Service Accounts → 创建
 *   2. 下载 JSON 密钥，保存为 scripts/config/ga4_service_account.json
 *   3. GA4 后台 → 管理 → 用户管理 → 添加 Service Account 邮箱（至少"查看者"权限）
 *
 * 使用方法:
 *   node scripts/ga4.js --property 123456789 --days 28
 *
 * 注意:
 *   GA4 Property ID 是纯数字，在 GA4 设置 → 媒体资源详情中查看。
 */

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const TOKEN_URL = "https://oauth2.googleapis.com/token";
const GA4_API = "https://analyticsdata.googleapis.com/v1beta";
const SA_FILE = path.join(__dirname, "config", "ga4_service_account.json");

// ===================== JWT + Service Account =====================

function base64url(source) {
  return source.toString("base64").replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

async function getAccessToken() {
  if (!fs.existsSync(SA_FILE)) {
    throw new Error(`Service Account 文件未找到: ${SA_FILE}\n请到 Google Cloud Console 创建并下载。`);
  }

  const sa = JSON.parse(fs.readFileSync(SA_FILE, "utf8"));
  const now = Math.floor(Date.now() / 1000);

  const header = JSON.stringify({ alg: "RS256", typ: "JWT" });
  const claims = JSON.stringify({
    iss: sa.client_email,
    scope: "https://www.googleapis.com/auth/analytics.readonly",
    aud: TOKEN_URL,
    iat: now,
    exp: now + 3600,
  });

  const signingInput = base64url(Buffer.from(header)) + "." + base64url(Buffer.from(claims));

  const sign = crypto.createSign("RSA-SHA256");
  sign.update(signingInput);
  const signature = sign.sign(sa.private_key, "base64");

  const jwt = signingInput + "." + base64url(Buffer.from(signature, "base64"));

  const res = await fetch(TOKEN_URL, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      grant_type: "urn:ietf:params:oauth:grant-type:jwt-bearer",
      assertion: jwt,
    }),
  });

  const data = await res.json();
  if (!res.ok) throw new Error(`Token 获取失败: ${data.error_description || data.error}`);
  return data.access_token;
}

// ===================== API 调用 =====================

async function runReport(token, propertyId, days = 28) {
  const end = new Date().toISOString().split("T")[0];
  const start = new Date(Date.now() - days * 86400000).toISOString().split("T")[0];

  const body = {
    dateRanges: [{ startDate: start, endDate: end }],
    dimensions: [{ name: "pageTitle" }, { name: "pagePath" }],
    metrics: [
      { name: "sessions" },
      { name: "engagementRate" },
      { name: "averageEngagementTimePerSession" },
      { name: "bounceRate" },
      { name: "newUsers" },
      { name: "screenPageViews" },
    ],
    limit: "100",
  };

  const res = await fetch(`${GA4_API}/properties/${propertyId}:runReport`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  const data = await res.json();
  if (!res.ok) throw new Error(`GA4 API ${res.status}: ${data.error?.message || JSON.stringify(data)}`);

  const dimensions = data.dimensionHeaders?.map(h => h.name) || [];
  const metrics = data.metricHeaders?.map(h => h.name) || [];

  const pages = (data.rows || []).map(row => {
    const obj = {};
    row.dimensionValues?.forEach((v, i) => { obj[dimensions[i]] = v.value; });
    row.metricValues?.forEach((v, i) => {
      const val = parseFloat(v.value);
      obj[metrics[i]] = metrics[i].includes("Rate") ? Math.round(val * 10000) / 100 : val;
    });
    return obj;
  });

  return {
    propertyId,
    period: `${start} to ${end}`,
    totalPages: pages.length,
    pages,
  };
}

async function getTrafficSources(token, propertyId, days = 28) {
  const end = new Date().toISOString().split("T")[0];
  const start = new Date(Date.now() - days * 86400000).toISOString().split("T")[0];

  const body = {
    dateRanges: [{ startDate: start, endDate: end }],
    dimensions: [{ name: "sessionDefaultChannelGroup" }],
    metrics: [{ name: "sessions" }, { name: "engagementRate" }],
  };

  const res = await fetch(`${GA4_API}/properties/${propertyId}:runReport`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  const data = await res.json();
  if (!res.ok) throw new Error(`GA4 API ${res.status}: ${data.error?.message || JSON.stringify(data)}`);

  const sources = (data.rows || []).map(row => ({
    channel: row.dimensionValues[0]?.value,
    sessions: parseInt(row.metricValues[0]?.value, 10),
    engagementRate: Math.round(parseFloat(row.metricValues[1]?.value) * 10000) / 100,
  }));

  return { period: `${start} to ${end}`, sources };
}

// ===================== CLI =====================

function parseArgs(argv) {
  const args = { property: "", days: 28, traffic: false, all: false };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--property") args.property = argv[++i];
    else if (a === "--days") args.days = parseInt(argv[++i], 10);
    else if (a === "--traffic") args.traffic = true;
    else if (a === "--all") args.all = true;
  }
  return args;
}

(async () => {
  const args = parseArgs(process.argv);

  if (!args.property) {
    console.error("Usage: node scripts/ga4.js --property 123456789 [--days 28] [--traffic] [--all]");
    console.error("\n注意: 需要先将 Service Account JSON 保存到 scripts/config/ga4_service_account.json");
    console.error("      并把 Service Account 邮箱加入 GA4 的用户权限。");
    process.exit(1);
  }

  try {
    const token = await getAccessToken();
    const result = { propertyId: args.property };

    if (args.all || !args.traffic) {
      result.pageMetrics = await runReport(token, args.property, args.days);
    }
    if (args.all || args.traffic) {
      result.trafficSources = await getTrafficSources(token, args.property, args.days);
    }

    console.log(JSON.stringify(result, null, 2));
  } catch (e) {
    console.error("Error:", e.message);
    process.exit(1);
  }
})();
