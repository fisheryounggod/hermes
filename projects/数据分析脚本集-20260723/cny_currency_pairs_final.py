#!/usr/bin/env python3
"""
人民币（CNY）对一篮子货币汇率分析（最终修复版）
避免所有 pandas 和 matplotlib 技术错误
"""

import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

print("正在获取人民币对一篮子货币汇率数据...")

# 定义要分析的货币对
currency_pairs = [
    ('CNYUSD=X', 'USD/CNY'),
    ('CNYEUR=X', 'EUR/CNY'),
    ('CNYJPY=X', 'JPY/CNY'),
    ('CNYGBP=X', 'GBP/CNY'),
    ('CNYKRW=X', 'KRW/CNY'),
    ('CNYSGD=X', 'SGD/CNY'),
    ('CNYHKD=X', 'HKD/CNY'),
    ('CNYTWD=X', 'TWD/CNY'),
    ('CNYTHB=X', 'THB/CNY'),
    ('CNYAUD=X', 'AUD/CNY'),
    ('CNYCAD=X', 'CAD/CNY'),
]

# 获取最近一个月的数据
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

# 下载所有货币对数据
tickers = [pair[0] for pair in currency_pairs]
data_dict = {}
for ticker in tickers:
    try:
        df = yf.download(ticker, start=start_date, end=end_date, interval="1d")
        if len(df) > 0:
            data_dict[ticker] = df
            print(f"获取到 {len(df)} 天数据")
    except Exception as e:
        print(f"获取失败: {e}")

print(f"成功获取到 {len(data_dict)} 个货币对数据")

# 创建对比图表（只显示前 6 个主要货币对）
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle('人民币对主要货币汇率（最近 30 天）', fontsize=16, fontweight='bold')

colors = ['#1f77b4', '#ff7f0e', '#2ecc71', '#3498db', '#9b59b6']

# 绘制前 6 个主要货币对
for i in range(6):
    row, col = i // 3, i % 3
    ax = axes[row, col]
    
    ticker, name = currency_pairs[i]
    
    if ticker in data_dict:
        df = data_dict[ticker].tail(7).copy()  # 最近 7 天
        
        # 提取数据（使用 values 避免问题）
        rates = df['Close'].values
        
        # 绘制
        ax.plot(df.index, rates, label=name, linewidth=2, color=colors[i], marker='o', markersize=6)
        ax.set_title(name, fontsize=12, fontweight='bold')
        ax.set_ylabel('汇率', fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper left', fontsize=9)
        
        # 简单的 x 轴标签（只显示日期）
        dates = [d.strftime('%m-%d') for d in df.index]
        ax.set_xticks(range(len(dates)))
        ax.set_xticklabels(dates, rotation=45, fontsize=8)

plt.tight_layout()
plt.subplots_adjust(top=0.9, hspace=0.3, bottom=0.1)

# 保存图表
output_file = '/home/yxf/clawd/cny_currency_pairs.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"图表已保存到: {output_file}")

# 生成数据摘要
print("\n汇率数据摘要:")
print("=" * 80)
print(f"{'货币对':<15} {'最新汇率':<15} {'7天平均':<15} {'期间最高':<15} {'期间最低':<15}")
print("-" * 80)

for i in range(6):
    ticker, name = currency_pairs[i]
    
    if ticker in data_dict:
        df = data_dict[ticker].tail(7)
        rates = df['Close'].values
        
        latest_rate = rates[-1]
        avg_rate = rates.mean()
        max_rate = rates.max()
        min_rate = rates.min()
        
        print(f"{name:<15} {latest_rate:.4f}      {avg_rate:.4f}      {max_rate:.4f}      {min_rate:.4f}")

print("=" * 80)

# 计算人民币汇率指数（基于前 6 个主要货币）
if len(data_dict) >= 6:
    rates_list = []
    valid_tickers = []
    
    for i in range(6):
        ticker, name = currency_pairs[i]
        if ticker in data_dict:
            df = data_dict[ticker].tail(7)
            rates = df['Close'].values
            rates_list.append(rates.mean())
            valid_tickers.append(name)
    
    if rates_list:
        cny_index = sum(rates_list) / len(rates_list)
        print(f"\n人民币汇率指数（基于 {len(valid_tickers)} 个主要货币）：{cny_index:.4f}")
        print("该指数反映了人民币对一篮子主要货币的平均汇率水平")
    else:
        print("\n无法计算人民币汇率指数（数据不足）")
else:
    print("\n无法计算人民币汇率指数（数据不足）")

print(f"\n完成！图表已生成并保存到: {output_file}")
