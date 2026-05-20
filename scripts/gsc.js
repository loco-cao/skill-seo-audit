#!/usr/bin/env node
/**
 * Google Search Console API Client — 零依赖 Node.js 版本
 *
 * 使用 Service Account（服务账号）JWT 认证，无需浏览器 OAuth。
 *
 * 前置步骤:
 *   1. Google Cloud Console → IAM → Service Accounts → 创建
 *   2. 下载 JSON 密钥，保存为 scripts/config/gsc_service_account.json
 *   3. 把 Service Account 的邮箱加入 GSC 的"用户和权限"
 *
 * 使用方法:
 *   node scripts/gsc.js --site https://example.com/ --queries --days 28
 *
 * 功能:
 *   --queries     搜索查询数据（展示、点击、CTR、排名）
 *   --links       外链数据
 *   --all         全部
 */

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const TOKEN_URL = "https://oauth2.googleapis.com/token";
const GSC_API = "https://www.googleapis.com/webmasters/v3";
const SA_FILE = path.join(__dirname, "config", "gsc_service_account.json");

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
    scope: "https://www.googleapis.com/auth/webmasters.readonly",
    aud: TOKEN_URL,
    iat: now,
    exp: now + 3600,
  });

  const signingInput = base64url(Buffer.from(header)) + "." + base64url(Buffer.from(claims));

  const sign = crypto.createSign("RSA-SHA256");
  sign.update(signingInput);
  const signature = sign.update(signingInput).sign(sa.private_key, "base64");

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

async function apiGet(token, path) {
  const res = await fetch(`${GSC_API}${path}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const data = await res.json();
  if (!res.ok) throw new Error(`GSC API ${res.status}: ${data.error?.message || JSON.stringify(data)}`);
  return data;
}

async function apiPost(token, path, body) {
  const res = await fetch(`${GSC_API}${path}`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(`GSC API ${res.status}: ${data.error?.message || JSON.stringify(data)}`);
  return data;
}

// ===================== 数据获取 =====================

async function getSearchQueries(token, siteUrl, days = 28) {
  const end = new Date().toISOString().split("T")[0];
  const start = new Date(Date.now() - days * 86400000).toISOString().split("T")[0];

  const body = {
    startDate: start,
    endDate: end,
    dimensions: ["query"],
    rowLimit: 100,
  };

  const data = await apiPost(token, `/sites/${encodeURIComponent(siteUrl)}/searchAnalytics/query`, body);

  return {
    period: `${start} to ${end}`,
    totalQueries: data.rows?.length || 0,
    queries: (data.rows || []).map(r => ({
      query: r.keys[0],
      clicks: r.clicks || 0,
      impressions: r.impressions || 0,
      ctr: r.ctr != null ? Math.round(r.ctr * 10000) / 100 : 0,
      position: r.position != null ? Math.round(r.position * 10) / 10 : 0,
    })),
  };
}

async function getLinks(token, siteUrl) {
  const data = await apiGet(token, `/sites/${encodeURIComponent(siteUrl)}/links`);
  const links = (data.externalLinks || []).slice(0, 100).map(l => ({
    sourceUrl: l.source?.url,
    targetUrl: l.target?.url,
    type: l.type,
  }));

  return {
    totalExternalLinks: data.externalLinks?.length || 0,
    sampleLinks: links,
  };
}

// ===================== CLI =====================

function parseArgs(argv) {
  const args = { site: "", days: 28, queries: false, links: false, all: false };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--site") args.site = argv[++i];
    else if (a === "--days") args.days = parseInt(argv[++i], 10);
    else if (a === "--queries") args.queries = true;
    else if (a === "--links") args.links = true;
    else if (a === "--all") args.all = true;
  }
  return args;
}

(async () => {
  const args = parseArgs(process.argv);

  if (!args.site) {
    console.error("Usage: node scripts/gsc.js --site https://example.com/ [--queries] [--links] [--all] [--days 28]");
    console.error("\n注意: 需要先将 Service Account JSON 保存到 scripts/config/gsc_service_account.json");
    process.exit(1);
  }

  try {
    const token = await getAccessToken();
    const result = { siteUrl: args.site };

    if (args.all || args.queries) {
      result.searchQueries = await getSearchQueries(token, args.site, args.days);
    }
    if (args.all || args.links) {
      result.links = await getLinks(token, args.site);
    }

    console.log(JSON.stringify(result, null, 2));
  } catch (e) {
    console.error("Error:", e.message);
    process.exit(1);
  }
})();
