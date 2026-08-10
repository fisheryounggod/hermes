---
type: schema-spec
version: 1.0
created: 2026-08-09
audience: AI agents (Hermes / Claude / Cursor / Codex / 任何 LLM)
---

# AGENTS.md — AI 工作说明书（Schema 规范层）

> 这是给 **任何 AI 协作者** 的总规约。先读这一页，再读 [[index]]，再动笔。

## 0. 这个 vault 是干什么的

`my-wiki/` 是一个 **两层结构** 的个人知识库：

- **`raw/`** —— 原始资料层。**AI 只读、不写、不删**。所有入站材料（剪藏、论文、书摘、对话、灵感、会议纪要）落在这里，作为不可篡改的事实底座。
- **`wiki/`** —— AI 全权维护的派生层。所有 `[[wikilink]]`、摘要、概念页、主题综述都建在这里。AI 可以在 `wiki/` 内自由创建/编辑/重组，但**写之前必须先在 `raw/` 找到事实源头**。

## 1. 铁律（违反任意一条 = 错误输出）

### 1.1 来源不可篡改
- ❌ 不得在 `raw/` 下创建、修改、删除任何文件。
- ❌ 不得「为了整洁」把 `raw/articles/foo.md` 改名或搬到 `wiki/sources/` —— `wiki/sources/` 是**派生页**，原始文件名要保留在 frontmatter 里作 source pointer。
- ✅ 例外：用户（Fisher）显式说「删掉 raw/xxx」才动。

### 1.2 写 wiki 之前必须有 raw 锚点
每一条非平凡的事实/引用，在 `wiki/` 写出来时必须用以下任一方式指回 `raw/`：

```markdown
来源: [[raw/articles/2026-08-09_some-article|原文标题]]  §段落关键词
```

如果找不到 `raw/` 锚点 → **不要编**。要么先帮用户在 `raw/` 里建文件，要么标注 `⚠ unverified`。

### 1.3 双链是义务，不是装饰
- 任何 wiki 页面至少要有 **3 个 `[[wikilink]]**：1 个指向来源（raw）、1 个指向相关概念/实体、1 个指向相关主题。
- 任何实体页（`wiki/entities/`）必须在 frontmatter 用 `related:` 字段链接至少 1 个概念页和 1 个主题页。

### 1.4 命名规约
- 文件名一律 `kebab-case` 或 `YYYY-MM-DD_topic-slug.md`，禁止中文文件名（避免编码问题 & Git 友好）。
- 单字大写用 `B2B` / `CBDC` / `EU` 这类行业惯例，**不要** `B-2-B`。
- raw 文件保留原始来源的元信息（URL、作者、ISBN）在 frontmatter 里。

### 1.5 frontmatter 必填字段
**所有** markdown 文件必须有 frontmatter，最少包含：

```yaml
---
type: source | concept | entity | topic | raw-article | raw-paper | raw-book | raw-chat | raw-note | raw-meeting
title: "完整可读标题"
created: YYYY-MM-DD
tags: [english-pref-lowercase, hyphenated]   # 至少 1 个
source: "[[raw/...]]"        # 仅 wiki/ 页必填
---
```

## 2. 目录语义

| 目录 | 谁来写 | 放什么 | frontmatter type |
|---|---|---|---|
| `raw/articles/` | Fisher（手工）/ 剪藏插件 | 网页剪藏、公众号转载、博客 | `raw-article` |
| `raw/papers/` | Fisher / Zotero | 论文 PDF + 提取的 markdown | `raw-paper` |
| `raw/books/` | Fisher / Readwise / Weread | 书摘、划线、章节笔记 | `raw-book` |
| `raw/chats/` | AI 会话回填 | 有价值的 AI 对话（File Back / Hermes export） | `raw-chat` |
| `raw/notes/` | Fisher | 灵感碎片、便签、随手记 | `raw-note` |
| `raw/meetings/` | Fisher / 飞书妙记 | 会议转写、纪要 | `raw-meeting` |
| `wiki/sources/` | AI | **一份 raw 资料 → 一页摘要**（source pointer + 关键论点 + 引用块） | `source` |
| `wiki/concepts/` | AI | 方法论、理论、模式、框架的解释页 | `concept` |
| `wiki/entities/` | AI | 人物、公司、产品、工具的事实页 | `entity` |
| `wiki/topics/` | AI | 某个领域的综合对比 / 综述 / 立场地图 | `topic` |

## 3. AI 工作流（标准动作链）

当用户给我一个任务，按这个顺序决定怎么动：

```
1. 先在 wiki/ 搜旧页面  →  相关已存在 → 判断「补充」还是「新建」
                        →  不存在 → 在合适目录新建
2. 读 raw/ 是否有相关材料  →  没有 → 先建议建 raw/，不要直接写 wiki/
3. 读 wiki/concepts/ wiki/entities/ 是否有相关派生页  →  有 → 用 patch 增量更新
                                                   →  没有 → 新建
4. 写 wiki/ 时强制带 [[wikilink]]，强制带 raw 锚点
5. 完成后在 log.md 追加一行（不改旧行）
6. 如果动了 wiki/concepts/ 或 wiki/topics/，回头检查 wiki/entities/ 的 related: 是否要补
```

**搜索旧页面的标准动作：**
- 用 `search_files` 在 vault 全域搜关键词（文件名 + 正文）
- 候选页列表出来后，逐个 `read_file` 看是否真的相关
- 如果只是**部分相关** → 用 `patch` 增量补充新章节，不重建
- 如果是**同一主题新视角** → 考虑新建关联页（如 `topic-x-from-perspective-y`），并用 wikilink 双向链接

## 3.1 冲突处理（新资料 vs 旧资料）

当新 raw 资料与 wiki/ 里既有结论**不一致**时：

1. **不直接覆盖旧结论**。在相关 wiki 页加新章节 `## 分歧与冲突`，记录：
   - 旧说法（来源、时间、原文段落）
   - 新说法（来源、时间、原文段落）
   - 适用范围差异（如：旧说法适用美国 2010-2015，新说法适用中国 2020+）
2. 如果冲突无法调和 → 在 wiki/ 相关页和 log.md 同时标注 `⚠ 待人工确认`
3. 仅当 Fisher 显式说「旧结论作废」时，才能 patch 移除旧说法，并在 log.md 记 `## ⚙️ CONFLICT RESOLVED`

## 4. 反模式（看到就这样改）

- ❌ 「AI 在 raw/ 下写『我整理过的笔记』」 → 把这页搬到 `wiki/sources/`，raw 保持原样
- ❌ 「一篇文章里塞了 5 个不同话题，所有 wiki 都没建」 → 拆，每个话题一个 wiki/concepts/ 页 + 1 个 wiki/topics/ 综述页
- ❌ 「wikilink 全是死链」 → 至少创建占位页（type: stub）或者删除链接
- ❌ 「topic 综述页没有 sources/citations 字段」 → 必填，参见 [[index#模板]]

## 4.1 log.md 字段规约（规则 8 配套）

每次变更 log.md 追加记录时，**必须**包含以下字段：

```
## YYYY-MM-DD HH:MM · <分类> · <执行者>

**动作**：<一句话>
**对象**：<文件路径 / 目录>
**原因**：<为什么改>
**保留**：<哪些旧文件被保留、未改动>        ← 可选但推荐
**受影响双链**：<本次动到哪些 wikilink>      ← 可选但推荐
**待人工确认**：<需要 Fisher 拍板的事项>     ← 可选但推荐
```

分类枚举：
- `CREATE` — 新建
- `UPDATE` — 修改（注明 section）
- `MOVE` — 移动 / 重命名
- `DELETE` — 删除（仅 raw/ 且 Fisher 显式授权）
- `INGEST` — 批量导入 raw 材料
- `SYNTH` — 在 wiki/ 做综合
- `SCHEMA` — 修改 AGENTS.md 或 index.md 模板
- `CONFLICT RESOLVED` — Fisher 裁定旧结论作废

## 4.2 不擅自删除（规则 9 配套）

- ❌ **不得擅自删除任何文件**，包括 wiki/ 派生页、log.md 旧行、AGENTS.md 旧规则
- ✅ **同名文件已存在**：先 `read_file` 读旧内容，判断是否合并 → 用 `patch` 增量补充，绝不 `write_file` 覆盖
- ✅ **要删 raw/ 文件**：必须 Fisher 显式说「删掉 raw/xxx」才动，并在 log.md 记 `## ⚠ DELETE`
- ✅ **要合并两个 wiki/ 页**：保留旧页 + 新建「已合并到 X」指 page + wikilink 反向链接，旧页加 `> ⚠ 本页已合并到 [[新页]]` 头部标注（不删）

## 4.3 信息不足时暂停提问（规则 10 配套）

以下情况必须用 `clarify` 工具暂停，**不要硬猜**：

1. **raw/ 资料缺失**：用户让我写 wiki/ 主题页，但 raw/ 里只有 1-2 份相关材料 → 问「要不要先补 raw？」
2. **冲突无法调和**：新旧资料分歧，且搜不到决定性证据 → 列两派说法，问 Fisher 倾向
3. **结构影响整体**：要新建 wiki/topics/ 子类、要重命名核心目录、要改 AGENTS.md 任何铁律 → 必须先问
4. **wikilink 全是死链**：要建 ≥ 5 个占位页时 → 问「先建占位 stub 还是先等你录 raw？」
5. **判断影响 ≥ 3 个文件**：一次动作会动 ≥ 3 个 wiki 页 + log + index → 先列计划等确认

**暂停模板**：
> "⚠ 我暂停一下，因为 [具体原因]。可选方向：
> 1) ...
> 2) ...
> 3) ...（其他）"

不暂停的代价：错一次 → 整套 wiki 双链断裂 + log 污染 + Fisher 信任折损。

## 5. 版本与变更

- 本文件是 **schema 规范**，改动它 = 改动整个 vault 的工作方式。要改之前先想清楚。
- 任何对 `AGENTS.md` 的修改 → 必须在 `log.md` 用 `## ⚙️ SCHEMA CHANGE` 标题单独记录，含 before / after / 原因。

## 6. 适用的 AI 协作者

本规约面向所有进入此 vault 的 AI：
- Hermes Agent（我）
- Claude / Codex / Cursor 等 IDE AI
- 用户自己手搓的脚本（用 frontmatter type 做路由）

**只要进入 `ai-wiki/`，就视同已读 AGENTS.md。**
