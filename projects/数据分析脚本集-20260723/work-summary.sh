#!/bin/bash
# Work Summary Script - 每天 22:00 执行
# 内容：生成今日工作总结 → 追加到月报 → 推送到飞书/Telegram

YEAR=$(date +%Y)
MONTH=$(date +%m)
DAY=$(date +%d)
WEEKDAY=$(date +%A)
DATE_STR=$(date +"%Y-%m-%d")
OUTPUT_DIR="$HOME/workspace/summary"
OUTPUT_FILE="$OUTPUT_DIR/${YEAR}-${MONTH}.md"
TEMP_FILE="$OUTPUT_DIR/temp_${DATE_STR}.md"

mkdir -p "$OUTPUT_DIR"

# 生成今日总结模板
cat > "$TEMP_FILE" << EOF
## ${DATE_STR}（${WEEKDAY}）

### ✅ 完成的工作
1. 

### 📝 学习与研究

### 🔧 遇到的问题与解决

### 💭 反思

### 🎯 明日计划
1. 

---
EOF

# 追加到月报
if [ -f "$OUTPUT_FILE" ]; then
    # 找到最后一个 "---" 分隔线，在其前插入
    # 简单策略：追加到文件末尾
    echo "" >> "$OUTPUT_FILE"
    cat "$TEMP_FILE" >> "$OUTPUT_FILE"
    echo "✅ 追加到月报：$OUTPUT_FILE"
else
    # 创建新月报
    cat > "$OUTPUT_FILE" << EOF
# 工作月报 — ${YEAR}年${MONTH}月

> 自动生成

---
EOF
    cat "$TEMP_FILE" >> "$OUTPUT_FILE"
    echo "✅ 创建新月报：$OUTPUT_FILE"
fi

# 清理临时文件
rm -f "$TEMP_FILE"

# 发送到 Telegram（通过 Hermes send_message）
echo "✅ 工作总结已生成：$OUTPUT_FILE"
