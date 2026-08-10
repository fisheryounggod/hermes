---
title: "Raw / Wiki / Schema 三层架构"
type: concept
aliases:
  - 三层知识库架构
  - LLM wiki 三层架构
tags:
  - architecture
  - llm-wiki
  - knowledge-management
sources:
  - "[[raw/articles/2026-08-09_canghe-codex-obsidian-llm-wiki|原文]]"
created: 2026-08-09
updated: 2026-08-09
---

# 概念：Raw / Wiki / Schema 三层架构

## 一句话定义

LLM wiki 的工程实现约定把知识库拆成三层：**Raw（事实底座，只读）/ Wiki（派生层，AI 维护）/ Schema（规则层，AGENTS.md）** —— 简单说就是 **Raw 保存证据，Wiki 记录理解，Schema 负责定规则**。

## 核心要点

- **Raw 层**：原始资料（文章、论文、对话、笔记、会议纪要）—— **只读**，AI 不能改
  - 命名规约：`YYYY-MM-DD_<slug>.md` 或 `<slug>.md`
  - frontmatter `type: raw-article / raw-paper / raw-book / raw-chat / raw-note / raw-meeting`
- **Wiki 层**：AI 全权维护的派生层
  - `sources/`：一份 raw → 一页摘要
  - `concepts/`：概念、理论、方法论
  - `entities/`：人物、公司、产品、工具
  - `topics/`：主题综述（≥3 来源）
- **Schema 层**：根目录 `AGENTS.md` 规定 AI 工作流
  - 铁律：raw 只读、写 wiki 必有 raw 锚点、双链义务、冲突保留、增量更新、不擅自删除、暂停提问

## 出处与延伸

### 出处
- [[wiki/sources/2026-08-09_canghe-codex-obsidian-llm-wiki]] — canghe 原文「为了让这个过程可控，整套系统分成三层」

### 与本 vault (ai-wiki) 的对应关系
```
canghe 描述           ai-wiki/ 实际实现
─────────────────────────────────────────
Raw 层           →    raw/{articles,papers,books,chats,notes,meetings}/
Wiki 层          →    wiki/{sources,concepts,entities,topics}/
Schema 层        →    AGENTS.md (10 条铁律 + 4 个反模式 + 3 个配套小节)
```

## 相关页面

### 同类概念
- [[wiki/concepts/llm-wiki]] — 上位范式

### 涉及这个概念的实体
- [[wiki/entities/canghe]]

### 出现在哪些主题
- [[wiki/topics/llm-wiki-and-self-growing-pkms]]

## 来源

- [[raw/articles/2026-08-09_canghe-codex-obsidian-llm-wiki]]
- https://x.com/canghe/status/2086372334089462208

## 待核实问题

- [ ] Karpathy 原版是不是用完全相同的三层？还是这是 canghe 自己加的工程抽象？
- [ ] Schema 层除了 AGENTS.md，是否还需要其他文件（如 `conventions.md`、`conflict-rules.md`）？
