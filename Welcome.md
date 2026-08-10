---
type: welcome
title: "👋 欢迎来到 my-wiki"
created: 2026-08-09
tags: [welcome, start-here]
---

# 👋 欢迎来到 my-wiki — AI 协作知识库

> 这是一个 **两层结构** 的个人 wiki，专门为「AI 协作」设计：
>
> - `raw/` = 事实底座（🔒 AI 只读）
> - `wiki/` = 派生层（🤖 AI 全权维护）

## 🗺️ 5 秒看懂结构

```
my-wiki/
├── AGENTS.md      ← ⛳ 必读！AI 工作说明书（所有 AI 协作者的第一站）
├── index.md       ← 全局导航
├── log.md         ← 变更日志（只追加）
│
├── raw/           ← 🔒 原始资料（只读层）
│   ├── articles/  网页/公众号剪藏
│   ├── papers/    论文/报告
│   ├── books/     书摘/划线
│   ├── chats/     AI 对话回填
│   ├── notes/     灵感碎片
│   └── meetings/  会议纪要
│
└── wiki/          ← 🤖 AI 维护的派生层
    ├── sources/   一份 raw → 一页摘要
    ├── concepts/  方法论/理论/框架
    ├── entities/  人物/公司/产品/工具
    └── topics/    领域综述/立场对比
```

## 🚀 第一次使用 — 推荐流程

1. **读 [[AGENTS]]**（5 分钟） — 理解 AI 在这里该怎么工作
2. **打开 [[index]]** — 看模板和工作流
3. **录首批材料** — 把最近剪藏的 3-5 篇文章/笔记，按类型搬到 `raw/` 对应目录
4. **让 AI 摘要** — 跟我说："读 raw/articles/xxx，建一份 wiki/sources/ 摘要"
5. **让 AI 提炼** — 等攒到 ≥3 篇相关 source 后："综合 raw/articles/ 里关于 X 的内容，建一份 wiki/topics/ 综述"

## 🎯 这个 vault 解决什么问题

| 痛点 | 解决方式 |
|---|---|
| 散落在剪藏插件/微信收藏/便签的材料找不到 | 统一进 `raw/`，按类型归档 |
| AI 总结完不知道出处 | 强制 frontmatter `source:` 字段指回 raw |
| 概念和实体在多篇文章里反复出现 | `wiki/concepts/` 和 `wiki/entities/` 沉淀 |
| 想知道某个领域有几派观点 | `wiki/topics/` 做立场对比表 |
| 不知道 AI 改了哪里 | `log.md` 强制 append-only 记录 |

## 🛡️ 核心规约（务必遵守）

> **任何 AI 协作者进入这个 vault 第一件事就是读 [[AGENTS]]。**
> 违反 [[AGENTS#1]] 任何一条铁律 = 输出作废。

最重要的 3 条：
1. **`raw/` 只读** — AI 不能改/删原始材料
2. **写 wiki 必须有 raw 锚点** — 没源头不写
3. **`[[wikilink]]` 是义务** — 至少 3 个：来源 + 相关概念 + 相关主题

## 📍 下一步

- 如果你是 Fisher：开始往 `raw/` 录材料，或者告诉 AI「读 X，建一份 wiki/sources/」
- 如果你是 AI 协作者：先读 [[AGENTS]]，再读 [[index]]，再决定怎么动手
