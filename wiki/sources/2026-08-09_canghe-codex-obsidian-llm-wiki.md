---
title: "canghe：Codex + Obsidian 搭建自生长的 LLM wiki 实战"
type: source
aliases:
  - LLM wiki 实战 (canghe)
tags:
  - source
  - llm-wiki
  - obsidian
  - codex
  - karpathy
sources:
  - "[[raw/articles/2026-08-09_canghe-codex-obsidian-llm-wiki|原文]]"
created: 2026-08-09
updated: 2026-08-09
source_url: https://x.com/canghe/status/2086372334089462208
---

# 来源摘要：canghe — Codex + Obsidian LLM wiki 实战

## 元信息

| 字段 | 值 |
|---|---|
| 原始文件 | [[raw/articles/2026-08-09_canghe-codex-obsidian-llm-wiki]] |
| 作者 | 苍何 @canghe |
| 发布日期 | 2026-08-09 |
| 类型 | X 长文章（is_note_tweet: True） |
| 互动 | 👍 75 · 💬 9 |
| 提取方式 | syndication (封面图) + fxtwitter api + extract_x_article.py（完整正文） |
| 长度 | 8624 bytes 正文 + 1 张配图（89962 bytes） |

## 摘要（100-200 字）

苍何基于 Karpathy 公开的 LLM wiki 思路，实践了一套「Codex/WorkBuddy + Obsidian + Markdown」的自生长个人知识库。核心是三层架构：**Raw 层保存原始资料（不可篡改）/ Wiki 层沉淀 AI 整理出的概念-实体-主题 / Schema 层规定归档、更新、引用、冲突处理规则**。与本 vault (ai-wiki) 的设计高度同构。

## 核心内容

### 关键论点 1：LLM wiki 解决「知识无积累」问题
> "现在主流的玩法，不管是 RAG 系统，还是 NotebookLM、GPT 的文件上传，本质都是同一套流程：你先上传资料，提问时模型召回相关知识片段，再临时综合出一个答案。听着挺智能，但问题很明显。每次提问，模型都在从碎片里重新拼答案，答完就散。"
> —— [[raw/articles/2026-08-09_canghe-codex-obsidian-llm-wiki|原文 §什么是 LLM wiki]]

Karpathy 的解法是：**给 AI 安排一份长期工作：持续维护知识库**。每加入资料 → 先查现有页 → 补充或新建 → 冲突保留来源/时间/适用范围。

### 关键论点 2：自生长的关键是「必须留下变化」
> "AI 处理完资料后，知识库必须留下变化。它可能新增一个概念、补上一条关联，也可能暴露一个暂时没有答案的问题。一次次变化累积起来，才会形成真正属于自己的知识体系。"

### 关键论点 3：三层架构
> "为了让这个过程可控，整套系统分成三层：Raw 层保存文章、论文、聊天记录等原始资料；Wiki 层沉淀 AI 整理出的概念、实体和主题；Schema 层规定 AI 如何归档、更新、引用，以及怎么处理冲突。简单说，**Raw 保存证据，Wiki 记录理解，Schema 负责定规则**。"

### 关键论点 4：为什么是 Obsidian（而非 Notion/Ima/NBLM）
- **本地化 + 数据自主**：Vault = 普通文件夹，Markdown 纯文本
- **私人数据可控**：聊天记录、会议纪要可留在自己设备
- **文件形态适合 Agent**：Codex/WorkBuddy 可直接读写、Git 留痕
- **工具可换**：知识不用跟着搬家

### 关键论点 5：AI 处理资料的「分流」原则
（依据原文"已内容会被补充，新概念会单独建页；遇到不同观点，则把来源、时间和适用范围一起留下"）
- 已有内容 → 补充
- 新概念 → 单独建页
- 冲突 → **保留多版本**（不直接覆盖）

## 相关页面

### 上游（来源）
- [[raw/articles/2026-08-09_canghe-codex-obsidian-llm-wiki]] — 完整原文

### 横向（同类：LLM wiki 范式其他来源）
- （暂无 — 第一份）

### 下游（被引用的概念 / 实体 / 主题）
- [[wiki/concepts/llm-wiki]] — LLM wiki 范式定义
- [[wiki/concepts/raw-wiki-schema-architecture]] — 三层架构
- [[wiki/concepts/ai-agent-knowledge-curation]] — Agent 长期维护知识库
- [[wiki/entities/canghe]] — 作者苍何
- [[wiki/topics/llm-wiki-and-self-growing-pkms]] — 主题综述

## 来源

- [[raw/articles/2026-08-09_canghe-codex-obsidian-llm-wiki]]
- https://x.com/canghe/status/2086372334089462208

## 待核实问题

- [ ] canghe 在 WorkBuddy 项目里是什么角色？（文章里多次提到，但身份不明）
- [ ] "Karpathy 公开的 LLM wiki 知识库构建方法和架构" 的原始出处是哪一篇？（需溯源到 Karpathy 的 repository 或 blog post）
- [ ] 文章后半部分「实操步骤」还没读完 —— 待读完后补充更多关键论点
