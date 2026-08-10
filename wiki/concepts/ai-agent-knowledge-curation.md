---
title: "AI Agent 长期维护知识库"
type: concept
aliases:
  - Agent as knowledge curator
  - AI 知识管家
tags:
  - ai-agent
  - knowledge-management
  - llm-wiki
sources:
  - "[[raw/articles/2026-08-09_canghe-codex-obsidian-llm-wiki|原文]]"
created: 2026-08-09
updated: 2026-08-09
---

# 概念：AI Agent 长期维护知识库

## 一句话定义

把 LLM 当成**长期工作的协作者**而非**问答接口**：每加入一份资料，Agent 按预设 Schema 主动「增量补充 / 新建页 / 保留冲突」，而不是被动「召回+综合」。

## 核心要点

- **从 RAG 到 Agent**：RAG 是「问→拼答」；LLM wiki Agent 是「问→维护→下次问更准」
- **持久化 state**：Agent 维护的不是会话窗口，而是 vault 上的 markdown 文件
- **可审计**：每次变动都有 log 记录、Git diff 可查
- **可接管**：人类可以在任何时刻介入（修正/标注/删除），不依赖某个平台
- **元能力**：Agent 维护 wiki 本身 → 也是在积累对「Agent 如何工作」的理解

## 出处与延伸

### 出处
- [[wiki/sources/2026-08-09_canghe-codex-obsidian-llm-wiki]] — canghe 原文「持续维护知识库」「每加入一份资料，Agent 都会先查看现有页面」

### 工具栈
- Codex / WorkBuddy / Claude Code —— Agent runtime
- Obsidian —— 知识库渲染层
- Git —— 审计层
- Markdown + frontmatter —— 数据格式

## 相关页面

### 同类概念
- [[wiki/concepts/llm-wiki]]

### 涉及这个概念的实体
- [[wiki/entities/canghe]]
- （Codex / WorkBuddy / Karpathy 实体页 — 待建）

### 出现在哪些主题
- [[wiki/topics/llm-wiki-and-self-growing-pkms]]

## 来源

- [[raw/articles/2026-08-09_canghe-codex-obsidian-llm-wiki]]
- https://x.com/canghe/status/2086372334089462208

## 待核实问题

- [ ] Codex / WorkBuddy / Claude Code 在「长期维护 wiki」这件事上的能力差异是什么？
- [ ] Agent 长期维护需要哪些基础设施（context、memory、tool use）？
