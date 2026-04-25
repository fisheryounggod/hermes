# Hermes 文件中心 · 任务看板

> 最后更新：2026-04-25
> 状态文件：与 `/home/yxf/Downloads/TASK.md` 同步

---

## ✅ 已完成

- [x] **Hermes 仓库初始化** — `fisheryounggod/hermes` 已创建，GitHub Pages 已启用
- [x] **Downloads 分类整理** — 根目录干净，按 travel/cards/finance/system 分类
- [x] **GitHub Pages 索引页** — 全中文展示，图片厨窗+文件列表+文档区
- [x] **自动同步 Cron** — 每6小时执行，token 存于 `~/.profile` 环境变量
- [x] **归档检查机制** — 同步前自动将根目录杂散文件归档到对应分类
- [x] **杭州5日出行卡片** — 舒适档+手绘风，已上传至 `travel/`

---

## 🔄 进行中

- [ ] **历史文件归集** — 将散落于 `~/scripts/`、`~/reports/`、`~/workspace/` 的文件整理入库

| 任务 | 来源 | 状态 |
|------|------|------|
| 脚本归集（A股/货币/SP500/飞书Bot） | `~/scripts/` | 待整理 |
| SP500报告归档 | `~/reports/` | 待整理 |
| 学习资料归集 | `~/workspace/learning/` | 待整理 |
| 工作记录归档 | `~/workspace/planning/summary/` | 待整理 |
| feedgrab 项目源码 | `~/feedgrab_repo/` | 待决策 |
| ezbookkeeping 数据 | `~/ezbookkeeping/` | 待决策 |

---

## 📋 待办

- [ ] **Pages 页面增强** — TASK.md 内容实时同步至页面顶部（当前为静态）
- [ ] **文档区自动构建** — Markdown 文档上传后自动生成 list+summary 列表（按日期降序）
- [ ] **分类索引** — 每个分类目录下生成子 README.md（方便 GitHub 浏览）
- [ ] **feedgrab 内容库** — 将 `feedgrab_repo/` 纳入同步体系
- [ ] **Fine-Grained PAT** — 替换当前 Classic PAT，限制到 hermes 单一仓库
- [ ] **Git 历史** — 考虑是否从 flat 结构切换为 git subtree 保留修改历史

---

## 🔒 决策待确认

| 问题 | 选项 |
|------|------|
| ~/workspace/ 是否并入 Downloads？ | A: 并入（内容统一管理） / B: 保留（Hermes 工作目录） |
| 脚本去重策略？ | A: 只保留最新版本 / B: 全部归档 / C: 手工筛选 |
| feedgrab 项目同步？ | A: 同步源码 / B: 同步输出内容 / C: 不同步 |

---

## 📊 统计

```
文件总数：   8
分类目录：   4 (travel/cards/finance/system)
Cron：      每6小时 · 999次循环
Token：     ~/.profile (HERMES_GITHUB_TOKEN)
Pages：     https://fisheryounggod.github.io/hermes/
```
