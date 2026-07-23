---
marp: true
size: 16:9
theme: am_blue1
paginate: true
footer: \ *泊舟AI* *2026-06-08*
---

<!-- _class: cover_a -->
<!-- _header: "" -->
<!-- _footer: "" -->
<!-- _paginate: false -->
# 零基础网页部署保姆级教程
###### 搞定上线最后一公里

---

<!-- _header: 目录<br>CONTENTS-->
<!-- _class: toc_b -->
<!-- _footer: "" -->
<!-- _paginate: false -->

- [你卡在哪一步？](#3)
- [什么叫部署？](#5)
- [部署的常见方式](#6)
- [最简路径：Vercel](#7)
- [最简路径：Netlify Drop](#8)
- [常见错误 & 避坑](#9)
- [总结](#10)

---

## 你卡在哪一步？

<!-- _class: trans -->
<!-- _footer: "" -->
<!-- _paginate: "" -->

---

AI 已经帮你把页面写好了

你自己电脑上也能打开

但你不知道 **怎么让别人通过一个链接访问它**

---

## 什么叫部署？

<!-- _class: trans -->
<!-- _footer: "" -->
<!-- _paginate: "" -->

---

把网页上传到互联网服务器

让任何人都能通过 **URL** 访问

---

## 部署的常见方式

<!-- _class: trans -->
<!-- _footer: "" -->
<!-- _paginate: "" -->

---

<!-- _class: cols2_ol_ci fglass -->

1. **免费静态托管**
   Vercel / Netlify / GitHub Pages
2. **拖拽上传**
   Cloudflare Pages、Netlify Drop
3. **命令行部署**
   一条命令完成上线

---

## 最简路径：Vercel

<!-- _class: trans -->
<!-- _footer: "" -->
<!-- _paginate: "" -->

---

<!-- _class: cols-2 -->

<div class=ldiv>

**操作步骤**

1. 注册 vercel.com（GitHub 账号直登）
2. 把项目文件夹拖入 Dashboard
3. 自动检测框架，点击 Deploy
4. 获得永久 URL，即刻分享

</div>

<div class=rdiv>

> **Vercel 优势**
> - 免费额度充足
> - 自动 HTTPS
> - 推送 Git 即自动部署

</div>

---

## 最简路径：Netlify Drop

<!-- _class: trans -->
<!-- _footer: "" -->
<!-- _paginate: "" -->

---

<!-- _class: bq-blue -->

> 无需 Git，无需命令行
> 直接把文件夹拖入页面
> **30 秒内获得在线链接**

---

## 常见错误 & 避坑

<!-- _class: trans -->
<!-- _footer: "" -->
<!-- _paginate: "" -->

---

<!-- _class: cols2_ul_ci fglass -->

- **依赖没装完就打包**
  确保 `npm install` 已运行
- **路径大小写不匹配**
  Linux 服务器严格区分大小写
- **忘记配置环境变量**
  敏感信息不要写进代码
- **没有设置 `base` 路径**
  子目录部署需配置

---

## 总结

<!-- _class: trans -->
<!-- _footer: "" -->
<!-- _paginate: "" -->

---

- 部署 = 让网页可通过 URL 访问
- 免费平台：Vercel / Netlify / GitHub Pages
- 最快方式：Netlify Drop 拖拽上线
- 遇到问题看控制台报错，逐条解决

---

<!-- _class: lastpage -->
<!-- _footer: "" -->
###### 感谢观看！
