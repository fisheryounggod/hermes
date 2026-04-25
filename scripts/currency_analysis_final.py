#!/usr/bin/env python3
"""
汇率趋势分析与货币相关性分析（最终修复版）
确保所有 numpy 操作的形状都正确
"""

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from datetime import datetime, timedelta

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

print("正在获取汇率数据...")

# 主要货币对
currency_pairs = [
    ('CNYUSD=X', 'USD/CNY (美元)'),
    ('CNYEUR=X', 'EUR/CNY (欧元)'),
    ('CNYJPY=X', 'JPY/CNY (日元)'),
    ('CNYGBP=X', 'GBP/CNY (英镑)'),
]

# 获取最近 3 个月的数据
end_date = datetime.now()
start_date = end_date - timedelta(days=90)

# 下载所有货币对
data_dict = {}
for ticker, name in currency_pairs:
    try:
        df = yf.download(ticker, start=start_date, end=end_date, interval="1d")
        if len(df) > 0:
            data_dict[ticker] = df
            print(f"获取到 {ticker} 的 {len(df)} 天数据")
    except Exception as e:
        print(f"获取 {ticker} 数据失败: {e}")

print(f"\n成功获取到 {len(data_dict)} 个货币对")

# 相关性分析（使用最近 60 天）
print("\n进行货币相关性分析...")

min_length = min([len(df) for df in data_dict.values()])
analysis_length = min(60, min_length)

# 准备数据
closes_dict = {}
for ticker, df in data_dict.items():
    closes = df['Close'].tail(analysis_length).values.astype(float)
    closes_dict[ticker] = closes

# 计算收益率（确保形状一致）
currencies = list(data_dict.keys())
n = len(currencies)

# 对齐数据
aligned_length = min([len(closes_dict[ticker]) for ticker in currencies])
aligned_closes = {}
for ticker in currencies:
    aligned_closes[ticker] = closes_dict[ticker][-aligned_length:]

# 计算收益率（使用对齐数据）
returns_arrays = {}
for ticker in currencies:
    closes = aligned_closes[ticker]
    # 计算收益率：(今日/昨日 - 1)
    returns = closes[1:] / closes[:-1] - 1
    returns_arrays[ticker] = returns

# 计算相关性矩阵
correlation_matrix = np.zeros((n, n))

for i in range(n):
    for j in range(n):
        returns1 = returns_arrays[currencies[i]]
        returns2 = returns_arrays[currencies[j]]
        
        # 确保长度一致
        min_len = min(len(returns1), len(returns2))
        returns1_trim = returns1[-min_len:]
        returns2_trim = returns2[-min_len:]
        
        # 计算相关性（纯 numpy）
        if min_len > 1:
            mean1 = np.mean(returns1_trim)
            mean2 = np.mean(returns2_trim)
            
            cov = np.mean((returns1_trim - mean1) * (returns2_trim - mean2))
            var1 = np.var(returns1_trim)
            var2 = np.var(returns2_trim)
            
            if var1 > 0 and var2 > 0:
                corr = cov / (np.sqrt(var1) * np.sqrt(var2))
            else:
                corr = 0.0
        else:
            corr = 0.0
        
        correlation_matrix[i, j] = corr

print("\n相关性矩阵:")
print(correlation_matrix)

# 绘制相关性热力图
fig, ax = plt.subplots(figsize=(10, 8))
fig.suptitle('货币对人民币汇率相关性矩阵', fontsize=16, fontweight='bold')

cmap = cm.RdYlBu_r
im = ax.imshow(correlation_matrix, interpolation='nearest', cmap=cmap, vmin=-1, vmax=1)

# 添加数值标注
for i in range(n):
    for j in range(n):
        text = ax.text(j, i, f"{correlation_matrix[i, j]:.2f}",
                       ha="center", va="center", color="black", fontsize=9)

# 设置坐标轴
ax.set_xticks(np.arange(n))
ax.set_yticks(np.arange(n))
ax.set_xticklabels(currencies, rotation=45, fontsize=10)
ax.set_yticklabels(currencies, fontsize=10)

# 添加颜色条
cbar = plt.colorbar(im, ax=ax)
cbar.set_label('相关性系数', rotation=270, labelpad=20, fontsize=12)

# 设置标题
ax.set_title('相关性系数 (日收益率)', fontsize=14, fontweight='bold', pad=20)

plt.tight_layout()

# 保存热力图
heatmap_file = '/home/yxf/clawd/currency_correlation_heatmap.png'
plt.savefig(heatmap_file, dpi=300, bbox_inches='tight')
print(f"\n相关性热力图已保存到: {heatmap_file}")

# 汇率趋势分析
print("\n进行汇率趋势分析...")

# 创建趋势图（归一化）
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('人民币对主要货币汇率趋势（最近 90 天）', fontsize=16, fontweight='bold')

axes = axes.flatten()
colors = ['#1f77b4', '#ff7f0e', '#2ecc71', '#e74c3c']

for i, (ticker, name) in enumerate(zip(currencies, [item[1] for item in currency_pairs])):
    ax = axes[i]
    df = data_dict[ticker].tail(90)
    closes = df['Close'].values.astype(float)
    
    # 归一化（起点为 100）
    base_price = closes[0]
    normalized = (closes / base_price) * 100
    
    # 绘制趋势
    ax.plot(df.index, normalized, label=ticker, linewidth=2, color=colors[i], alpha=0.8)
    ax.fill_between(df.index, normalized, color=colors[i], alpha=0.2)
    
    ax.set_title(name, fontsize=12, fontweight='bold')
    ax.set_xlabel('日期', fontsize=10)
    ax.set_ylabel('归一化汇率 (起点=100)', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper left', fontsize=9)
    
    # 简化的 x 轴标签
    date_indices = range(0, len(df), 15)
    ax.set_xticks(date_indices)
    ax.set_xticklabels([df.index[idx].strftime('%m-%d') for idx in date_indices], rotation=45, fontsize=8)

plt.tight_layout()
plt.subplots_adjust(top=0.9, hspace=0.3, bottom=0.1)

# 保存趋势图
trend_file = '/home/yxf/clawd/currency_trend_analysis.png'
plt.savefig(trend_file, dpi=300, bbox_inches='tight')
print(f"趋势图已保存到: {trend_file}")

# 数据摘要
print("\n数据摘要:")
print("=" * 80)
print(f"{'货币对':<20} {'最新汇率':<15} {'90天涨跌':<15} {'趋势':<15}")
print("-" * 80)

for ticker, name in zip(currencies, [item[1] for item in currency_pairs]):
    if ticker in data_dict:
        df = data_dict[ticker].tail(90)
        closes = df['Close'].values.astype(float)
        
        # 计算涨跌
        base_price = closes[0]
        current_price = closes[-1]
        total_change = (current_price / base_price - 1) * 100
        
        # 判断趋势
        if total_change > 10:
            trend = "强烈上升"
        elif total_change > 0:
            trend = "温和上升"
        elif total_change < -10:
            trend = "强烈下降"
        elif total_change < 0:
            trend = "温和下降"
        else:
            trend = "震荡盘整"
        
        print(f"{name:<20} {current_price:<15.4f} {total_change:+.2f}%      {trend:<15}")
    else:
        print(f"{name:<20} 无数据")

print("=" * 80)

# 相关性分析摘要
print("\n相关性分析摘要:")
print("-" * 40)

# 找出最相关的货币对
max_corr_indices = np.unravel_index(np.abs(correlation_matrix), np.argsort(np.abs(correlation_matrix), axis=None))[::-1]

print("最相关的货币对:")
count = 0
for idx in max_corr_indices:
    if count >= 3:
        break
    
    row, col = idx
    corr_val = correlation_matrix[row, col]
    name1 = currencies[row]
    name2 = currencies[col]
    
    print(f"  {count+1}. {name1} <-> {name2}: {corr_val:.2f}")
    count += 1

print("-" * 40)

# 相关性解读
print("相关性解读:")
print("相关系数范围: -1 (完全负相关) 到 1 (完全正相关)")
print("  0.7-1.0: 强相关")
print("  0.4-0.7: 中等相关")
print("  0.1-0.4: 弱相关")
print("  -0.1-0.1: 几乎不相关")

print("\n完成!")
print(f"\n分析报告已生成:")
print(f"  - 相关性热力图: {heatmap_file}")
print(f"  - 汇率趋势图: {trend_file}")

plt.show()
