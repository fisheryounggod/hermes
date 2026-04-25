#!/bin/bash
# 30天计划晨读提醒脚本
# 根据当前日期计算学习进度

PLAN_START="2026-04-24"
TODAY=$(date +%Y-%m-%d)
WEEKDAY=$(date +%A)
DATE_CN=$(date +"%Y年%m月%d日")

# 计算第几天
DAYS_SINCE_START=$((($(date +%s) - $(date -d "$PLAN_START" +%s)) / 86400 + 1))

# 如果还没开始或已过期
if [ $DAYS_SINCE_START -lt 1 ]; then
    echo "📅 计划尚未开始（第1天：$PLAN_START）"
    exit 0
fi

if [ $DAYS_SINCE_START -gt 30 ]; then
    echo "✅ 30天计划已完成！"
    exit 0
fi

CURRENT_DAY=$DAYS_SINCE_START

# 根据天数确定主题
case $CURRENT_DAY in
    1) THEME="直播开场与迎新"; WORDS="live stream, welcome, going live, join us, hit follow"; TASK="朗读5个黄金开场白各3遍，录音" ;;
    2) THEME="自我介绍与品牌建立"; WORDS="brand, creator, host, founder, specialize in, curated"; TASK="制作中英对照自我介绍卡，朗读录音" ;;
    3) THEME="产品介绍基础（FAB法）"; WORDS="feature, advantage, benefit, durable, user-friendly, versatile"; TASK="用FAB法写出产品介绍稿" ;;
    4) THEME="价格与价值传达"; WORDS="retail price, discount, save, value for money, worth every penny, flash sale"; TASK="写出价格话术（含原价/折扣/省钱金额）" ;;
    5) THEME="紧迫感与稀缺性营造"; WORDS="running low, almost gone, don't miss out, in stock, last few"; TASK="设计催单组合，录音练习" ;;
    6) THEME="直播收尾与感谢"; WORDS="wrap up, before you go, coming up next, see you next time"; TASK="写直播收尾语（中英对照）" ;;
    7) THEME="第1周复盘"; WORDS="第1周全部词汇复习"; TASK="完整5分钟模拟直播演练" ;;
    8) THEME="观众互动与Q&A开场"; WORDS="question, Q&A, drop in the chat, let me know, curious about"; TASK="预想3个观众问题，写出标准回答" ;;
    9) THEME="产品展示与演示话术"; WORDS="texture, fits true to size, lightweight, vibrant, hand-feel"; TASK="写出完整产品展示话术" ;;
    10) THEME="对比销售与竞品话术"; WORDS="compare to, versus, blows it out of the water, speaks for itself"; TASK="找竞品，写3句对比话术" ;;
    11) THEME="限量优惠码与福利发放"; WORDS="promo code, stackable, first-time buyer, free shipping"; TASK="设计3个优惠码及话术" ;;
    12) THEME="退货政策与信任建立"; WORDS="return, refund, money-back guarantee, worry-free, risk-free"; TASK="写出退货政策话术" ;;
    13) THEME="赠品与捆绑销售话术"; WORDS="bundle, kit, set, free gift, bonus item, value pack"; TASK="设计捆绑套餐，写完整话术" ;;
    14) THEME="第2周复盘"; WORDS="第2周全部词汇复习"; TASK="演练6大场景" ;;
    15) THEME="常见Q&A应对"; WORDS="runs true to size, shipping, tracking, color options"; TASK="准备5个Q&A标准回答" ;;
    16) THEME="价格异议处理"; WORDS="investment, break the bank, affordable, cost-effective, premium quality"; TASK="写出价格异议应对话术" ;;
    17) THEME="质量疑虑处理"; WORDS="warranty, guarantee, durability, tested, certified, authentic"; TASK="写出3个质量疑虑应对话术" ;;
    18) THEME="观众互动技巧"; WORDS="shoutout, in the house, loyal, way to show love, big up"; TASK="练习点名、感谢、激励话术" ;;
    19) THEME="节日促销话术"; WORDS="Black Friday, holiday special, gift guide, seasonal, Prime Day"; TASK="设计节日促销话术" ;;
    20) THEME="说服心理学话术"; WORDS="social proof, FOMO, scarcity, exclusivity, reciprocity, authority"; TASK="写出3类说服话术" ;;
    21) THEME="第3周复盘"; WORDS="第3周全部词汇复习"; TASK="10分钟综合演练" ;;
    22) THEME="全流程彩排·开场"; WORDS="冷场应对话术"; TASK="3分钟开场演练" ;;
    23) THEME="全流程彩排·产品+价格"; WORDS="全部产品介绍话术"; TASK="6分钟产品介绍演练" ;;
    24) THEME="全流程彩排·互动+收尾"; WORDS="Q&A+催单+收尾话术"; TASK="5分钟后半段演练" ;;
    25) THEME="完整直播模拟"; WORDS="15分钟全流程"; TASK="15分钟完整直播模拟" ;;
    26) THEME="薄弱环节突破"; WORDS="针对自评<3的环节"; TASK="重点练习最弱项" ;;
    27) THEME="语速与节奏训练"; WORDS="快/中/慢语速对比练习"; TASK="3段语速对比录音" ;;
    28) THEME="临场应变与即兴"; WORDS="即兴发挥训练"; TASK="2段即兴发挥录音" ;;
    29) THEME="话术手册整理"; WORDS="个性化金句"; TASK="整理专属话术手册" ;;
    30) THEME="毕业直播+总结"; WORDS="20分钟完整直播"; TASK="毕业直播+30天总结" ;;
esac

WEEK=$(( (CURRENT_DAY - 1) / 7 + 1 ))

cat << EOF
📅 $DATE_CN（$WEEKDAY）
📚 【海外电商英语 · 30天强化学习】

🌱 第${CURRENT_DAY}天 / 共30天 | 第${WEEK}周 | 主题：${THEME}

🎯 今日学习
核心词汇：$WORDS
实战任务：$TASK
⏱️ 建议时长：30-45分钟

📖 完整计划：~/workspace/learning/overseas-ecommerce-english-30day-plan.md

💡 核心理念：场景驱动、实战为主、每天有交付物
EOF
