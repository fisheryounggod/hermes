---
title: "LLM wiki"
type: concept
aliases:
  - LLM wiki 范式
  - 自生长知识库
tags:
  - llm-wiki
  - knowledge-management
  - karpathy
  - ai-agent
sources:
  - "[[raw/articles/2026-08-09_canghe-codex-obsidian-llm-wiki|原文]]"
created: 2026-08-09
updated: 2026-08-09
---

# 概念：LLM wiki

## 一句话定义

**LLM wiki** 是 Karpathy 提出的范式：让 LLM 作为长期 Agent **持续维护** 一个 Markdown 知识库（wiki），每加入新资料 → 先查现有页 → 增量补充或新建页 → 冲突保留多版本 —— 区别于「每次提问临时拼答案」的 RAG。

## 核心要点

- **Agent 化**：LLM 不是「问答接口」，而是「长期工作」
- **写之前先读**：处理新资料 → 先搜旧页面 → 判断补充 vs 新建
- **冲突保留**：新旧不一致 → 同时记下来源/时间/适用范围，不覆盖
- **可追溯**：所有 wiki 页必须有 raw 锚点
- **自生长**：AI 处理完资料，wiki 必须留下变化（增/补/暴露问题）

## 出处与延伸

### 出处
- [[wiki/sources/2026-08-09_canghe-codex-obsidian-llm-wiki]] — canghe 的实战描述
- （待核实）Karpathy 原始 blog post / GitHub repo

### 延伸阅读
- [[wiki/concepts/raw-wiki-schema-architecture]] — LLM wiki 的三层架构实现
- [[wiki/concepts/ai-agent-knowledge-curation]] — Agent 长期维护的知识管理范式

## 相关页面

### 同类概念
- [[wiki/concepts/ai-agent-knowledge-curation]]（同源但侧重「Agent 角色」）

### 涉及这个概念的实体
- [[wiki/entities/canghe]]
- [[wiki/entities/karpathy|（待核实）]]

### 出现在哪些主题
- [[wiki/topics/llm-wiki-and-self-growing-pkms]]

## 来源

- [[raw/articles/2026-08-09_canghe-codex-obsidian-llm-wiki]]
- https://x.com/canghe/status/2086372334089462208

## 待核实问题

- [ ] Karpathy 原始 LLM wiki 是哪个 repo / blog post？需要找到 first-class 引用
- [ ] 「自生长」的精确定义是什么？canghe 转述 vs Karpathy 原义可能有差
- [ ] LLM wiki 与 RAG、NotebookLM、Zettelkasten 的边界在哪里？
