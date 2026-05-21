# 外链质量评估指南

## 外链六大基础指标

1. **外链类型**：dofollow传递权重，nofollow不传递但可带来流量与品牌曝光
2. **引用域（Referring Domains）**：指向本站的不同域名数量，比外链总数更重要
3. **锚文本类型**：品牌锚文本、裸URL、通用词、精确匹配、部分匹配、LSI关键词
4. **链接位置**：正文内链接 > 侧边栏 > 页脚 > 评论区
5. **获取速度**：新站每月5-10条，成熟站点每月20-50条，禁止爆发式增长
6. **生命周期**：高质量外链长期稳定，低质外链可能几个月后失效

## 高质量外链六大特征

1. 来源域名与目标站点主题相关
2. 链接位于正文内容中（编辑性链接）
3. 来源页面本身有自然搜索流量
4. 来源域名DR≥30（或行业基准中位数）
5. 锚文本自然描述目标页面内容
6. 链接周围内容质量高、原创、有阅读价值

## 锚文本分布健康标准

| 类型 | 占比 | 示例 |
|------|------|------|
| 品牌锚文本 | ≥50% | "YourBrand"、"YourBrand.com" |
| 裸URL | 10-20% | "https://yourbrand.com" |
| 通用词 | 10-15% | "点击这里"、"了解更多"、"官网" |
| 精确匹配 | ≤10% | "best seo tool" |
| 部分匹配/LSI | 15-20% | "seo optimization platform" |

## Toxic外链识别清单

- 来源域名DR<10且出站链接数量>100
- 同一IP/服务器上的大量相似站点互相链接（PBN特征）
- 外链获取速度在短时间内激增（如1周内+500条）
- 锚文本100%精确匹配关键词
- 来源网站已被Google deindexed或标记为unsafe
- 垃圾目录站、自动评论链接、链接农场
- 外语站点与目标市场无关的外链（如中文站大量俄文外链）

## 外链建设渠道清单

### 白帽渠道
- 工具目录：AlternativeTo、Product Hunt、Toolify、Capterra、G2
- 社交媒体资料外链：Twitter/X、LinkedIn、Facebook、YouTube
- GitHub开源项目（README中的链接）
- Reddit社区（参与讨论后自然提及，非spam）
- Product Hunt发布（需准备截图、描述、制造者评论）
- Hacker News Show HN（技术产品适用）
- Medium文章（带nofollow但可带来流量和品牌）
- 客座博客（Guest Posting，选择行业相关、DR≥30的站点）
- 工具评测请求（联系评测博主、YouTuber）
- 资源页外链（找到"best tools"列表页请求加入）
- Broken Link Building（找到死链提供替代内容）
- HARO / Help A B2B Writer（响应记者请求）

### 高风险渠道（需严格评估）
- 购买外链（Fiverr、论坛链接包）
- 链接交换（Reciprocal Links，过度会被惩罚）
- PBN网络（Private Blog Network，黑帽，高风险）
- 自动评论/论坛签名外链

## 品牌建设监测指标

- 品牌搜索量（Google Trends、GSC品牌词展现量）
- 品牌提及（非链接提及，可用Google Alerts、BrandMentions）
- 社交媒体粉丝增长与互动率
- 直接流量占比（GA4中Direct流量）

## Google外链惩罚

### 算法惩罚（Penguin）
- 特征：排名突然下降，尤其在精确匹配关键词上
- 触发：低质外链比例过高、锚文本过度优化
- 恢复：清理 toxic 外链 + 提交 Disavow + 等待算法重新评估

### 手动处罚（Unnatural Links）
- 特征：GSC收到手动操作通知
- 触发：购买链接、PBN、大规模链接交换
- 恢复：清理问题链接 → 提交重新审核请求

## Disavow文件规范

- 格式：`domain:spamdomain.com` 或 `https://spamdomain.com/bad-page.html`
- 仅在外链清理无效时使用
- 上传至GSC的Disavow Links Tool
- 保留原始文件备份
