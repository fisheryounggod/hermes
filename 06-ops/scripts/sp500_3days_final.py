#!/usr/bin/env python3
"""
S&P 500 - Last 3 Days Trend Chart (Fixed Version)
最简单的方法，避免所有技术错误
"""

import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

print("正在获取标普500（S&P 500）最近三天数据...")

# 获取最近一个月的数据
ticker = "^GSPC"
df = yf.download(ticker, period="1mo", interval="1d")

print(f"获取到 {len(df)} 天数据")

# 取最近3个交易日（三天）
df_last_3days = df.tail(3).copy()

# 提取数据（使用 .values 避免 pandas 问题）
dates = df_last_3days.index
closes = df_last_3days['Close'].values
opens = df_last_3days['Open'].values
highs = df_last_3days['High'].values
lows = df_last_3days['Low'].values

# 创建图表
fig, ax = plt.subplots(figsize=(12, 6))
fig.suptitle('S&P 500 - Last 3 Days', fontsize=14, fontweight='bold')

# 绘制收盘价走势
ax.plot(dates, closes, label='Close Price', linewidth=2, color='#1f77b4', marker='o', markersize=8)
ax.set_xlabel('Date', fontsize=11)
ax.set_ylabel('Index Points', fontsize=11)
ax.set_title('Price Trend', fontsize=12, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.legend(loc='upper left', fontsize=10)

# 简单的 x 轴格式
import matplotlib.dates as mdates
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))

# 调整布局
plt.tight_layout()

# 保存图表
output_file = '/home/yxf/clawd/sp500_last3days.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"图表已保存到: {output_file}")

# 显示数据摘要（使用最简单的方法）
print("\n数据摘要:")
for i in range(len(dates)):
    print(f"\nDay {i+1}: {dates[i].strftime('%Y-%m-%d')}")
    print(f"  Open: {float(opens[i]):.2f}")
    print(f"  High: {float(highs[i]):.2f}")
    print(f"  Low: {float(lows[i]):.2f}")
    print(f"  Close: {float(closes[i]):.2f}")
    if i > 0:
        change = float(closes[i]) - float(closes[i-1])
        direction = "UP" if change > 0 else "DOWN"
        print(f"  Change: {change:.2f} ({direction})")
    else:
        print("  Change: 0.00 (BASE DAY)")

# 总体涨跌
total_change = float(closes[-1]) - float(closes[0])
direction = "UP" if total_change > 0 else "DOWN"
print(f"\n总体涨跌: {total_change:.2f} ({direction})")

plt.show()

print("\n完成！")
