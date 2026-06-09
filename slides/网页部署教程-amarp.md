---
marp: true
size: 16:9
theme: am_blue1
paginate: true
headingDivider: [2, 3]
header: "零基础网页部署保姆级教程"
footer: "泊舟 AI · 2026-06-08"
math: katex
---

<!-- _class: cover -->
<!-- _header: "" -->
<!-- _footer: "" -->
<!-- _paginate: false -->
# 零基础网页部署保姆级教程
## 搞定上线最后一公里

---

<!-- _class: toc_a -->
<!-- _header: "CONTENTS" -->
## 目录

1. 你卡在哪一步？
2. 什么叫部署？
3. 部署的常见方式
4. 最简路径：Vercel
5. 最简路径：Netlify Drop
6. 常见错误 & 避坑
7. 总结

---

<!-- _class: trans -->
## 01 · 你卡在哪一步？

---

## 你卡在哪一步？

AI 已经帮你把页面写好了

你自己电脑上也能打开

但你不知道 **怎么让别人通过一个链接访问它**

---

<!-- _class: trans -->
## 02 · 什么叫部署？

---

## 什么叫部署？

把网页上传到互联网服务器

让任何人都能通过 **URL** 访问

---

<!-- _class: trans -->
## 03 · 部署的常见方式

---

## 部署的常见方式

<!-- _class: cols2_ol_ci fglass -->
1. **免费静态托管**
   Vercel / Netlify / GitHub Pages
2. **拖拽上传**
   Cloudflare Pages、Netlify Drop
3. **命令行部署**
   一条命令完成上线

---

<!-- _class: trans -->
## 04 · 最简路径：Vercel

---

## 最简路径：Vercel

<!-- _class: cols-2 -->
<div class="ldiv">

**操作步骤**

1. 注册 vercel.com（GitHub 账号直登）
2. 把项目文件夹拖入 Dashboard
3. 自动检测框架，点击 Deploy
4. 获得永久 URL，即刻分享

</div>
<div class="rdiv">

![bg right:90%](https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600)

</div>

---

<!-- _class: trans -->
## 05 · 最简路径：Netlify Drop

---

## 最简路径：Netlify Drop

<!-- _class: bq-blue -->
> 无需 Git，无需命令行
> 直接把文件夹拖入页面
> **30 秒内获得在线链接**

---

<!-- _class: trans -->
## 06 · 常见错误 & 避坑

---

## 常见错误 & 避坑

<!-- _class: cols2_ul_ci -->
- **依赖没装完就打包**
  确保 `npm install` 已运行
- **路径大小写不匹配**
  Linux 服务器严格区分大小写
- **忘记配置环境变量**
  敏感信息不要写进代码
- **没有设置 `base` 路径**
  子目录部署需配置

---

<!-- _class: trans -->
## 07 · 总结

---

## 总结

- 部署 = 让网页可通过 URL 访问
- 免费平台：Vercel / Netlify / GitHub Pages
- 最快方式：Netlify Drop 拖拽上线
- 遇到问题看控制台报错，逐条解决

---

<!-- _class: lastpage -->
# 开始部署吧 🚀

