#!/usr/bin/env python3
"""
标普500与黄金价格最近一周走势图（极简版）
使用 yfinance 获取数据，用 matplotlib 绘制对比图
"""

import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# 设置中文字体（会有警告但不影响功能）
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

print("正在获取标普500和黄金数据...")

# 定义资产代码
tickers = ['^GSPC', 'GC=F']  # 标普500和黄金期货

# 获取最近一周的数据
end_date = datetime.now()
start_date = end_date - timedelta(days=7)

# 下载数据
data_dict = {}
for ticker in tickers:
    try:
        df = yf.download(ticker, start=start_date, end=end_date, interval="1d")
        if len(df) > 0:
            data_dict[ticker] = df
            print(f"获取到 {ticker} 的 {len(df)} 天数据")
    except Exception as e:
        print(f"获取 {ticker} 数据失败: {e}")

print(f"\n成功获取到 {len(data_dict)} 个资产数据")

# 创建图表（两个子图）
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
fig.suptitle('标普500与黄金价格最近一周走势对比', fontsize=16, fontweight='bold')

# 图1：标普500走势
if '^GSPC' in data_dict:
    df_sp500 = data_dict['^GSPC']
    ax1.plot(df_sp500.index, df_sp500['Close'], label='S&P 500', 
            linewidth=2.5, color='#1f77b4', marker='o', markersize=8)
    ax1.set_xlabel('日期', fontsize=12)
    ax1.set_ylabel('指数点位', fontsize=12)
    ax1.set_title('标普500走势', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='upper left', fontsize=11)

# 图2：黄金价格走势
if 'GC=F' in data_dict:
    df_gold = data_dict['GC=F']
    ax2.plot(df_gold.index, df_gold['Close'], label='Gold Price', 
            linewidth=2.5, color='#f39c12', marker='s', markersize=8)
    ax2.set_xlabel('日期', fontsize=12)
    ax2.set_ylabel('价格（美元/盎司）', fontsize=12)
    ax2.set_title('黄金价格走势', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc='upper left', fontsize=11)

# 调整布局
plt.tight_layout()
plt.subplots_adjust(top=0.9, hspace=0.3, bottom=0.1)

# 保存图表
output_file = '/home/yxf/clawd/sp500_gold_1week.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"图表已保存到: {output_file}")

# 数据摘要
print("\n数据摘要:")
print("=" * 80)

if '^GSPC' in data_dict:
    df_sp500 = data_dict['^GSPC']
    latest_sp500 = df_sp500['Close'].iloc[-1]
    high_sp500 = df_sp500['Close'].max()
    low_sp500 = df_sp500['Close'].min()
    change_sp500 = (latest_sp500 / df_sp500['Close'].iloc[0] - 1) * 100
    
    print("标普500 (S&P 500):")
    print(f"  最新点位: {latest_sp500:.2f}")
    print(f"  期间最高: {high_sp500:.2f}")
    print(f"  期间最低: {low_sp500:.2f}")
    print(f"  一周涨跌: {change_sp500:+.2f}%")

if 'GC=F' in data_dict:
    df_gold = data_dict['GC=F']
    latest_gold = df_gold['Close'].iloc[-1]
    high_gold = df_gold['Close'].max()
    low_gold = df_gold['Close'].min()
    change_gold = (latest_gold / df_gold['Close'].iloc[0] - 1) * 100
    
    print("\n黄金价格 (Gold):")
    print(f"  最新价格: ${latest_gold:.2f}")
    print(f"  期间最高: ${high_gold:.2f}")
    print(f"  期间最低: ${low_gold:.2f}")
    print(f"  一周涨跌: {change_gold:+.2f}%")

print("=" * 80)

# 相关性分析（如果都有数据）
print("\n相关性分析:")

if '^GSPC' in data_dict and 'GC=F' in data_dict:
    df_sp500 = data_dict['^GSPC']
    df_gold = data_dict['GC=F']
    
    # 对齐数据
    min_length = min(len(df_sp500), len(df_gold))
    df_sp500_aligned = df_sp500.tail(min_length)
    df_gold_aligned = df_gold.tail(min_length)
    
    # 计算日收益率
    sp500_returns = df_sp500_aligned['Close'].pct_change().dropna()
    gold_returns = df_gold_aligned['Close'].pct_change().dropna()
    
    # 计算相关性（手动计算，避免 Series 比较错误）
    min_len = min(len(sp500_returns), len(gold_returns))
    sp500_returns_trim = sp500_returns.values[-min_len:]
    gold_returns_trim = gold_returns.values[-min_len:]
    
    if min_len > 1:
        mean_sp500 = sum(sp500_returns_trim) / min_len
        mean_gold = sum(gold_returns_trim) / min_len
        
        cov = sum((x - mean_sp500) * (y - mean_gold) for x, y in zip(sp500_returns_trim, gold_returns_trim)) / (min_len - 1)
        var_sp500 = sum((x - mean_sp500) ** 2 for x in sp500_returns_trim) / (min_len - 1)
        var_gold = sum((y - mean_gold) ** 2 for y in gold_returns_trim) / (min_len - 1)
        
        if var_sp500 > 0 and var_gold > 0:
            correlation = cov / (var_sp500 ** 0.5 * var_gold ** 0.5)
        else:
            correlation = 0.0
        
        print(f"  相关系数: {correlation:.2f}")
        
        if abs(correlation) > 0.7:
            corr_type = "强相关"
        elif abs(correlation) > 0.4:
            corr_type = "中等相关"
        elif abs(correlation) > 0.1:
            corr_type = "弱相关"
        else:
            corr_type = "几乎不相关"
        
        print(f"  相关类型: {corr_type}")
    else:
        print("  数据不足，无法计算相关性")
else:
    print("  数据不足，无法计算相关性")

print("\n完成!")
print(f"\n图表已生成并保存到: {output_file}")

plt.show()
