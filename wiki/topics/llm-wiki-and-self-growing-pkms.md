---
title: "LLM wiki 与自生长 PKMS"
type: topic
aliases:
  - LLM wiki 自生长个人知识库
tags:
  - topic
  - llm-wiki
  - pkm
  - ai-agent
sources:
  - "[[raw/articles/2026-08-09_canghe-codex-obsidian-llm-wiki|来源]]"
created: 2026-08-09
updated: 2026-08-09
---

# 主题：LLM wiki 与自生长 PKMS

## 综述

自生长个人知识管理系统（Personal Knowledge Management System, PKMS）正在从「人维护笔记 + AI 偶尔辅助」转向「**AI 作为长期 Agent 持续维护 vault**」。这一转变的工程范式代表是 Karpathy 提出的 **LLM wiki** —— 让 LLM 不再是临时问答工具，而是被赋予「持续维护一份 Markdown 知识库」的长期工作。

核心机制是三层架构：**Raw 层（不可篡改的原始资料）/ Wiki 层（AI 增量维护的派生知识）/ Schema 层（AGENTS.md 规则）**。三者形成闭环：Raw 提供事实锚点防止 LLM 幻觉；Wiki 沉淀结构化理解（概念、实体、主题）并通过双链建立关系网络；Schema 把工作流编码为机器可读的规约，让 AI 在无人在场时也能按规约推进。

与传统 PKM 方法论（卢曼卡片盒、PARA、双链笔记）的关键区别：**「自生长」不是方法的优雅，而是结果的累积**。每加入一份资料，AI 处理后 wiki 必须留下变化（补充、新建、暴露问题），这些变化累积起来才形成真正属于自己的知识体系 —— 而非每次提问都从零拼答案的 RAG。

中文社区 canghe 在 2026-08 发布的实战文章是这一范式的首批完整中文记录，验证了在 Codex/WorkBuddy + Obsidian 栈上的可落地性。

## 立场对比

| 立场 | 代表人物/来源 | 核心论点 | 强度 |
|---|---|---|---|
| **LLM wiki Agent 范式** | Karpathy (原始) / canghe (中文实战) | AI 长期维护 vault，自生长优于反复拼答 | 强 |
| **RAG + 临时综合** | NotebookLM / GPT 文件上传主流用法 | 上传资料 → 提问时召回 → 临时拼答 | 强（仍是当下主流） |
| **传统 PKM + AI 辅助** | PARA / Zettelkasten / 双链笔记社区 | 人是 curator，AI 只是写作/检索工具 | 中 |
| **Notion/Ima/NotebookLM 平台派** | 各 SaaS 厂商 | 平台封装好，开箱即用，工具锁定可接受 | 中 |

## 关键证据

### 证据 1：「LLM wiki 解决知识无积累问题」
> "现在主流的玩法……每次提问，模型都在从碎片里重新拼答案，答完就散。同样的问题问一百遍，它就重新拼一百遍，知识本身没有任何积累。"
> —— [[wiki/sources/2026-08-09_canghe-codex-obsidian-llm-wiki|来源 §什么是 LLM wiki]]

### 证据 2：「自生长的关键是必须留下变化」
> "AI 处理完资料后，知识库必须留下变化。它可能新增一个概念、补上一条关联，也可能暴露一个暂时没有答案的问题。"
> —— [[wiki/sources/2026-08-09_canghe-codex-obsidian-llm-wiki|来源]]

### 证据 3：「为什么是 Obsidian」
- 本地化 + 数据自主（私人资料不外流）
- 文件形态适合 Agent 读写（WorkBuddy / Codex 可直接操作）
- 工具可换 → 知识不搬家（Markdown 纯文本）
- Git 友好 → 全部变更可审计
> —— [[wiki/sources/2026-08-09_canghe-codex-obsidian-llm-wiki|来源 §为什么是 Obsidian]]

## 分歧与冲突

> 当前没有显著冲突（仅 1 份来源）。后续若加入 Karpathy 原始资料、NotebookLM 官方文档、PARA 创始人文章 等对立来源时，按 [[AGENTS#3.1]] 处理。

## 相关页面

### 涉及的概念
- [[wiki/concepts/llm-wiki]] — 范式定义
- [[wiki/concepts/raw-wiki-schema-architecture]] — 工程实现
- [[wiki/concepts/ai-agent-knowledge-curation]] — Agent 角色

### 涉及的实体
- [[wiki/entities/canghe]] — 中文社区实践者
- （待建）[[wiki/entities/karpathy]] — 范式提出者

### 引用的 source 摘要
- [[wiki/sources/2026-08-09_canghe-codex-obsidian-llm-wiki]]

## 来源

- [[raw/articles/2026-08-09_canghe-codex-obsidian-llm-wiki]]
- https://x.com/canghe/status/2086372334089462208

## 待核实问题

- [ ] Karpathy 原始 LLM wiki 出处（blog post 或 GitHub repo）
- [ ] 与 RAG / NotebookLM 的量化对比（准确率、复用率、维护成本）
- [ ] 失败案例：什么情况下 Agent 维护会失控？怎么回滚？
- [ ] 大规模 vault（>1000 页）下的性能与索引策略
- [ ] Agent 跨 session 的 memory 设计 —— 单纯靠 wiki 文件够吗？
