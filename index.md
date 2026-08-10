---
type: navigation
title: "my-wiki 全局索引"
created: 2026-08-09
tags: [index, navigation, hub]
---

# my-wiki / 全局索引

> 这里是 **AI 定位知识的入口**。所有进入 `ai-wiki/` 的 AI 协作者，第一步读 [[AGENTS]]，第二步读本页。

## 一图看懂结构

```
my-wiki/                          ←  你在这里
├── AGENTS.md                     ←  ⛳ 必读！AI 工作说明书
├── index.md  ← 📍 你正在读这个
├── log.md                        ←  变更日志（只追加）
│
├── raw/  ← 🔒 只读层（Fisher 写，AI 不动）
│   ├── articles/  网页/公众号剪藏
│   ├── papers/    论文 + 报告
│   ├── books/     读书笔记 / 划线
│   ├── chats/     AI 对话回填
│   ├── notes/     灵感碎片
│   └── meetings/  会议纪要
│
└── wiki/  ← 🤖 AI 维护层
    ├── sources/   一份 raw → 一页摘要（带 source pointer）
    ├── concepts/  方法论 / 理论 / 模式 / 框架
    ├── entities/  人物 / 公司 / 产品 / 工具
    └── topics/    领域综述 / 立场对比 / 综合分析
```

## 快速导航

### 规范层（先读）
- [[AGENTS]] — **AI 工作说明书**（Schema 规范层）⛳
- [[log]] — 变更日志

### raw/（只读）
- 暂无内容 — 等待 Fisher 录入首批材料

### wiki/（AI 全权维护）
- [[wiki/sources/_index]] — 资料摘要总目录
- [[wiki/concepts/_index]] — 概念索引
- [[wiki/entities/_index]] — 实体索引
- [[wiki/topics/_index]] — 主题综述索引

## 模板（AI 写新页时复制）

> 模板已独立落地为 `_template.md` 文件，**直接复制比手敲更稳**：
>
> - 资料摘要 → [[wiki/sources/_template]]
> - 概念 → [[wiki/concepts/_template]]
> - 实体 → [[wiki/entities/_template]]
> - 主题综述 → [[wiki/topics/_template]]
>
> 复制后用 `YYYY-MM-DD_<slug>.md` 或 `<slug>.md` 命名，删掉 `_template_` 段填正文。
> 模板字段规约见 [[AGENTS#1.5]]。

## 下一步建议
1. 把现有散落的材料（剪藏、书摘、笔记）按类型搬到 `raw/` 对应子目录
2. 让 AI 从 `raw/` 首批材料里抽取 → 在 `wiki/sources/` 建摘要页
3. 累积到 3+ 个相关 source 后，让 AI 在 `wiki/topics/` 做综述
