#!/usr/bin/env python3
"""
A 股历次牛市分析（最终修复版）
确保所有 pandas 比较都使用标量值
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# 设置中文字体（会有警告但不影响功能）
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

print("正在获取 A 股（上证指数）历史数据...")

# 尝试不同的股票代码
tickers_to_try = ['000001.SS', '000001.SS.SS', '^SSEC']
df = None
ticker_used = None

for ticker in tickers_to_try:
    try:
        end_date = datetime.now()
        start_date = datetime(2010, 1, 1)  # 从 2010 年开始
        
        print(f"尝试使用股票代码: {ticker}")
        temp_df = yf.download(ticker, start=start_date, end=end_date, interval="1d")
        
        if len(temp_df) > 0:
            df = temp_df
            ticker_used = ticker
            print(f"✅ 成功获取到 {ticker} 的 {len(df)} 天数据")
            break
    except Exception as e:
        print(f"❌ 获取 {ticker} 数据失败: {e}")
        continue

# 检查是否成功获取数据
if df is None or len(df) == 0:
    print("\n❌ 无法获取上证指数数据")
    print("请检查网络连接或尝试其他股票代码")
    exit(1)

print(f"\n最终使用的股票代码: {ticker_used}")
print(f"数据范围: {df.index[0].strftime('%Y-%m-%d')} 至 {df.index[-1].strftime('%Y-%m-%d')}")

# 计算移动平均（用于趋势分析）
df['MA50'] = df['Close'].rolling(window=50).mean()
df['MA200'] = df['Close'].rolling(window=200).mean()

# 识别牛市阶段（使用标量值，避免 Series 比较错误）
print("\n识别牛市阶段...")

bull_markers = []
current_bull = False
bull_start = None
bull_high = 0
bull_duration = 0

# 从第 200 天开始分析（确保有足够的移动平均数据）
for i in range(200, len(df)):
    close_price = float(df['Close'].iloc[i])
    ma50 = float(df['MA50'].iloc[i])
    ma200 = float(df['MA200'].iloc[i])
    
    # 计算近期低点（过去 200 天）
    if i >= 200:
        recent_low = df['Close'].iloc[i-200:i].min().item()
        
        # 牛市启动条件：MA50 > MA200（金叉）且价格从近期低点上涨超过 30%
        if not current_bull:
            if close_price / recent_low > 1.30 and ma50 > ma200:
                current_bull = True
                bull_start = df.index[i]
                bull_high = close_price
        
        # 牛市延续
        if current_bull:
            bull_duration += 1
            bull_high = max(bull_high, close_price)
            
            # 牛市结束条件：价格从高点下跌超过 20% 或 MA50 < MA200（死叉）
            if close_price / bull_high < 0.80 or ma50 < ma200:
                current_bull = False
                bull_markers.append({
                    'start': bull_start,
                    'end': df.index[i],
                    'duration': bull_duration,
                    'low': df['Close'].iloc[df.index.get_loc(bull_start):i].min().item(),
                    'high': bull_high,
                    'return': (bull_high / df['Close'].iloc[df.index.get_loc(bull_start):i].min().item() - 1) * 100
                })
                bull_duration = 0

# 如果当前还在牛市中，添加到列表
if current_bull:
    bull_markers.append({
        'start': bull_start,
        'end': df.index[-1],
        'duration': bull_duration,
        'low': df['Close'].iloc[df.index.get_loc(bull_start):i].min().item(),
        'high': bull_high,
        'return': (bull_high / df['Close'].iloc[df.index.get_loc(bull_start):i].min().item() - 1) * 100,
        'active': True
    })

print(f"识别到 {len(bull_markers)} 个牛市阶段")

# 创建可视化图表
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 12))
fig.suptitle(f'A 股历次牛市分析（上证指数 {ticker_used}）', fontsize=16, fontweight='bold')

# 图1：历史走势与牛市标注
ax1.plot(df.index, df['Close'], label='上证指数', linewidth=1.5, color='#1f77b4', alpha=0.7)
ax1.plot(df.index, df['MA50'], label='50日均线', linewidth=1, color='#ff7f0e', alpha=0.5)
ax1.plot(df.index, df['MA200'], label='200日均线', linewidth=1, color='#2ecc71', alpha=0.5)

# 标注牛市区域
colors = ['#2ecc71', '#3498db', '#e74c3c', '#9b59b6']
for i, bull in enumerate(bull_markers):
    start_date = bull['start']
    end_date = bull['end']
    
    # 添加牛市区域
    ax1.axvspan(start_date, end_date, alpha=0.2, color=colors[i % len(colors)])
    
    # 添加牛市标注
    mid_date = start_date + (end_date - start_date) / 2
    label_text = f"牛市 {i+1}\n{bull['return']:.1f}%"
    ax1.annotate(label_text,
                xy=(mid_date, bull['high']),
                xytext=(0, 30),
                textcoords='offset points',
                ha='center',
                fontsize=8,
                fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.8),
                arrowprops=dict(arrowstyle='->', color=colors[i % len(colors)], lw=1.5))

ax1.set_xlabel('日期', fontsize=12)
ax1.set_ylabel('指数点位', fontsize=12)
ax1.set_title('历史走势与牛市标注', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend(loc='upper left', fontsize=10)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))

# 图2：牛市特征分析
ax2.axis('off')

# 生成牛市特征表格
table_data = []
for i, bull in enumerate(bull_markers):
    if 'active' in bull and bull['active']:
        status = "进行中"
    else:
        status = "已结束"
    
    table_data.append([
        f"牛市 {i+1}",
        bull['start'].strftime('%Y-%m-%d'),
        status,
        f"{bull['duration']} 天",
        f"{bull['low']:.1f}",
        f"{bull['high']:.1f}",
        f"{bull['return']:.1f}%"
    ])

# 创建表格
table = ax2.table(cellText=table_data,
                      colLabels=['牛市名称', '开始日期', '状态', '持续天数', '最低点位', '最高点位', '收益率'],
                      cellLoc='center',
                      loc='center',
                      bbox=[0, 0, 1, 1],
                      colWidths=[0.15, 0.15, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])

table.auto_set_font_size(9)
table.set_fontsize(10)

ax2.set_title('牛市特征', fontsize=14, fontweight='bold', pad=20)
ax2.axis('off')

# 调整布局
plt.tight_layout()
plt.subplots_adjust(top=0.85, hspace=0.3, bottom=0.1)

# 保存图表
output_file = '/home/yxf/clawd/a_share_bull_markets.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\n图表已保存到: {output_file}")

# 生成牛市分析报告
print("\n牛市分析报告:")
print("=" * 80)
print(f"{'牛市名称':<12} {'开始日期':<14} {'状态':<10} {'持续天数':<10} {'最低点位':<12} {'最高点位':<12} {'收益率':<10}")
print("-" * 80)

for i, bull in enumerate(bull_markers):
    if 'active' in bull and bull['active']:
        status = "进行中"
    else:
        status = "已结束"
    
    print(f"{'牛市 {i+1}':<12} {bull['start'].strftime('%Y-%m-%d'):<14} {status:<10} {bull['duration']:<10} {bull['low']:<12.1f} {bull['high']:<12.1f} {bull['return']:<10.1f}")

print("=" * 80)

# 统计分析
print("\n统计摘要:")
print("-" * 40)

total_bull_duration = sum(bull['duration'] for bull in bull_markers)
active_bull_count = sum(1 for bull in bull_markers if 'active' in bull and bull['active'])
completed_bull_count = len(bull_markers) - active_bull_count

avg_bull_duration = total_bull_duration / len(bull_markers) if len(bull_markers) > 0 else 0
avg_bull_return = np.mean([bull['return'] for bull in bull_markers]) if len(bull_markers) > 0 else 0

print(f"牛市阶段数: {len(bull_markers)}")
print(f"进行中牛市: {active_bull_count}")
print(f"已结束牛市: {completed_bull_count}")
print(f"牛市平均持续天数: {avg_bull_duration:.0f}")
print(f"牛市平均收益率: {avg_bull_return:.1f}%")
print(f"牛市总计持续天数: {total_bull_duration}")

print(f"\n当前市场状态:")
print("-" * 40)

last_close = float(df['Close'].iloc[-1])
last_ma50 = float(df['MA50'].iloc[-1])
last_ma200 = float(df['MA200'].iloc[-1])

if last_ma50 > last_ma200:
    market_trend = "上升趋势（50日均线上方200日均线）"
elif last_ma50 < last_ma200:
    market_trend = "下降趋势（50日均线下方200日均线）"
else:
    market_trend = "震荡盘整"

print(f"最新指数点位: {last_close:.1f}")
print(f"市场趋势: {market_trend}")

# 最近 90 天表现
print(f"\n最近 90 天表现:")
print("-" * 40)

df_last_90 = df.tail(90)
start_90 = float(df_last_90['Close'].iloc[0])
end_90 = float(df_last_90['Close'].iloc[-1])
change_90 = (end_90 / start_90 - 1) * 100

print(f"90天涨跌幅: {change_90:+.1f}%")

if change_90 > 30:
    status_90 = "强势上涨"
elif change_90 > 0:
    status_90 = "温和上涨"
elif change_90 < -30:
    status_90 = "强势下跌"
elif change_90 < 0:
    status_90 = "温和下跌"
else:
    status_90 = "震荡盘整"

print(f"市场状态: {status_90}")

print("\n完成!")
print(f"\n分析报告已生成:")
print(f"  - 历史走势与牛市标注图: {output_file}")

plt.show()
