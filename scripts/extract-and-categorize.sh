#!/bin/bash
# 将 raw 文件夹中的文章取出，添加 category 元数据标注文章类型

TEMP_DIR="temp/raw-with-category"
mkdir -p "$TEMP_DIR"

# 定义分类映射（去除序号）
declare -A CATEGORIES=(
    ["00-学术研究"]="学术研究"
    ["01-学习认知"]="学习认知"
    ["02-商业经济"]="商业经济"
    ["03-技术教程"]="技术教程"
    ["04-运动健康"]="运动健康"
    ["05-书课资源"]="书课资源"
    ["06-文章合集"]="文章合集"
    ["07-English"]="English"
    ["08-BOOKS"]="BOOKS"
    ["09-书签收藏"]="书签收藏"
    ["10-外刊新闻"]="外刊新闻"
    ["11-Papers"]="Papers"
)

# 处理每个文件夹
for folder in raw/*/; do
    folder_name=$(basename "$folder")
    category="${CATEGORIES[$folder_name]}"

    if [ -z "$category" ]; then
        echo "Skipping unknown folder: $folder_name"
        continue
    fi

    echo "Processing: $folder_name -> category: $category"

    # 创建对应的输出目录
    mkdir -p "$TEMP_DIR/$folder_name"

    # 处理文件夹中的所有文件
    for file in "$folder"*.md; do
        [ -f "$file" ] || continue

        filename=$(basename "$file")

        # 读取文件内容
        content=$(cat "$file")

        # 检查是否有 frontmatter
        if [[ "$content" == "---"* ]]; then
            # 已有 frontmatter，检查是否已有 category
            if grep -q "^category:" <<< "$content"; then
                # 已有 category，更新它
                content=$(sed "s/^category:.*/category: $category/" <<< "$content")
            else
                # 在第一个 --- 后插入 category
                content=$(sed "/^---$/a category: $category" <<< "$content")
            fi
        else
            # 没有 frontmatter，在开头添加
            content="---
category: $category
---

$content"
        fi

        # 保存到 temp 目录
        echo "$content" > "$TEMP_DIR/$folder_name/$filename"
    done
done

echo "Done! Files saved to $TEMP_DIR"
