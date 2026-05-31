# Schema 结构化数据参考文档

> 来源：Google 官方结构化数据文档（from Google Search Central）
> 原始来源：https://github.com/zlbigger/Google-SEOs.skill (MIT License)
>
> 供 `seo-schema-expert` 执行审计时查阅具体 Schema 类型的必填属性和规范。

## 覆盖类型（36 种）

| 类型 | 文件 | 常用场景 |
|------|------|---------|
| Article | article.md | 文章/博客/新闻 |
| Breadcrumb | breadcrumb.md | 面包屑导航 |
| Carousel | carousel.md | 轮播内容 |
| Course | course.md | 在线课程 |
| Dataset | dataset.md | 数据集 |
| Discussion Forum | discussion-forum.md | 论坛/社区 |
| Education Q&A | education-qa.md | 教育问答 |
| Employer Rating | employer-rating.md | 雇主评分 |
| Event | event.md | 活动/演出 |
| FAQPage | faqpage.md | FAQ 页面 |
| Image License | image-license-metadata.md | 图片授权 |
| Job Posting | job-posting.md | 招聘信息 |
| Local Business | local-business.md | 本地商家 |
| Loyalty Program | loyalty-program.md | 会员计划 |
| Math Solvers | math-solvers.md | 数学求解器 |
| Merchant Listing | merchant-listing.md | 商家列表 |
| Movie | movie.md | 电影信息 |
| Organization | organization.md | 组织/品牌 |
| Paywalled Content | paywalled-content.md | 付费内容 |
| Practice Problems | practice-problems.md | 练习题 |
| Product | product.md | 产品信息 |
| Product Snippet | product-snippet.md | 产品摘要 |
| Product Variants | product-variants.md | 产品变体 |
| Profile Page | profile-page.md | 个人资料页 |
| QAPage | qapage.md | 问答页 |
| Recipe | recipe.md | 食谱 |
| Return Policy | return-policy.md | 退货政策 |
| Review Snippet | review-snippet.md | 评价摘要 |
| Shipping Policy | shipping-policy.md | 配送政策 |
| Software App | software-app.md | 软件应用 |
| Speakable | speakable.md | 语音可用 |
| Vacation Rental | vacation-rental.md | 度假租赁 |
| SD Policies | sd-policies.md | 结构化数据政策 |
| Search Gallery | search-gallery.md | 搜索展示库 |
| Generate SD with JS | generate-structured-data-with-javascript.md | JS 生成结构化数据 |
| Intro | intro-structured-data.md | 结构化数据入门 |

## 使用方式

`seo-schema-expert` 在审计时：

1. 先读取 `references/schema-guide.md` 了解审计框架和评分标准
2. 根据页面类型查阅对应的 `references/schema-docs/<type>.md` 获取必填属性清单
3. 在 finding 的 `reference` 字段中同时引用 `schema-guide` 和对应的 `schema-docs/<type>.md`