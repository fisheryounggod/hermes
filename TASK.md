# Hermes 文件中心 · 任务看板

> 最后更新：2026-04-25
> 状态文件：`~/Downloads/TASK.md`，与 GitHub 同步

---

## ✅ 已完成

- [x] **Hermes 仓库初始化** — `fisheryounggod/hermes` 已创建，GitHub Pages 已启用
- [x] **Downloads 分类整理** — 根目录干净，按 8 分类存储
- [x] **GitHub Pages 索引页** — 全中文展示，任务看板置顶，图片厨窗+文件列表+文档区
- [x] **自动同步 Cron** — 每6小时执行，token 存于 `~/.profile` 环境变量
- [x] **归档检查机制** — 同步前自动将根目录杂散文件归档到对应分类
- [x] **杭州5日出行卡片** — 舒适档+手绘风，已上传至 `travel/`
- [x] **历史文件归集** — scripts(13)/reports(4)/work(3)/learning(1)/research(1) 已入库，共 23 文件

---

## 📋 待办

- [ ] **Pages 页面增强** — TASK.md 内容实时同步至页面顶部
- [ ] **文档区自动构建** — Markdown 文档上传后自动生成 list+summary 列表（按日期降序）
- [ ] **分类索引** — 每个分类目录下生成子 README.md（方便 GitHub 浏览）
- [ ] **feedgrab 内容库** — 将 `feedgrab_repo/output/` 纳入同步体系
- [ ] **Fine-Grained PAT** — 替换当前 Classic PAT，限制到 hermes 单一仓库

---

## 📁 当前文件结构

```
~/Downloads/
├── index.html          ← 索引页（页端展示）
├── TASK.md             ← 本任务看板
├── travel/             ← 出行卡片（5图）
├── cards/              ← 通用卡片（1图）
├── finance/            ← 金融指南（1图）
├── system/             ← 系统工程（1图）
├── scripts/            ← Python/Shell 脚本（13文件）
├── reports/            ← SP500 分析报告（4文件）
├── work/               ← 工作计划与总结（3文件）
├── learning/           ← 学习计划（1文件）
└── research/           ← 研究资料（1文件）
```

---

## 🔒 决策待确认

| 问题 | 状态 |
|------|------|
| feedgrab 项目同步？ | 待定（源码/输出/不同步） |
| Git 历史？ | flat 结构，无 git subtree |

---

## 📊 统计

```
总文件数：    25（含 TASK.md + index.html 不计）
分类目录：    8
Cron：       每6小时 · 999次循环
Token：      ~/.profile (HERMES_GITHUB_TOKEN)
Pages：      https://fisheryounggod.github.io/hermes/
最后同步：    2026-04-25
```
