#!/bin/bash
# Work Planning Script - 每天 09:00 执行
# 内容：读取飞书日历 + 待办 → 生成今日工作计划 → 写入本地文件

YEAR=$(date +%Y)
MONTH=$(date +%m)
DAY=$(date +%d)
WEEKDAY=$(date +%A)
DATE_STR=$(date +"%Y-%m-%d")
OUTPUT_DIR="$HOME/workspace/planning"
OUTPUT_FILE="$OUTPUT_DIR/${DATE_STR}.md"

mkdir -p "$OUTPUT_DIR"

# 从飞书读取今日日历（如有）
CALENDAR_CONTENT=""
if [ -f "$HOME/.hermes/feishu_todo_creds.json" ]; then
    # 尝试读取日历（如果配置了的话）
    CALENDAR_CONTENT="## 📅 今日日历\n\n_（如需配置日历，请设置 Google Calendar API 或飞书日历）_\n\n"
fi

# 读取待办（如有）
TODO_CONTENT=""
if [ -f "$HOME/.hermes/feishu_todo_creds.json" ]; then
    TODO_CONTENT="## ✅ 今日待办\n\n_（待办数据）_\n\n"
fi

# 生成计划文档
cat > "$OUTPUT_FILE" << EOF
# 工作规划 — ${DATE_STR}（${WEEKDAY}）

> 自动生成于 $(date +"%H:%M:%S")

---

## 🎯 今日核心目标

_（请根据以下信息填写今日最重要的 1-3 件事）_

1. 
2. 
3. 

---

## 📋 待处理任务

$TODO_CONTENT

---

## 📅 今日日程

$CALENDAR_CONTENT

---

## 🔮 洞见与反思

_（今日工作中发现的问题、新想法、学到的东西）_

---

## ⏰ 时间块规划

| 时间段 | 任务 | 状态 |
|--------|------|------|
| 09:00-10:00 |  |  |
| 10:00-11:00 |  |  |
| 11:00-12:00 |  |  |
| 14:00-16:00 |  |  |
| 16:00-18:00 |  |  |
| 19:00-21:00 |  |  |

EOF

echo "✅ 工作规划已生成：$OUTPUT_FILE"
