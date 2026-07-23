#!/usr/bin/env python3
"""Generate 9:16 sector fund flow comparison MP4."""
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from datetime import datetime
import os

# 22 sectors with colors (from skill v3.0.0)
sectors_info = [
    ('存储芯片','#FF4757'),('大科技','#FF7F50'),('先进制造','#FF9800'),
    ('半导体','#FFC107'),('半导体材料设备','#FFEB3B'),('油气资源','#C0E040'),
    ('商业航天','#8BC34A'),('人工智能','#4CAF50'),('电网设备','#009688'),
    ('云计算','#00BCD4'),('通信','#03A9F4'),('CPO','#2979FF'),
    ('消费电子','#5C6BC0'),('AI应用','#7E57C2'),('军工','#AB47BC'),
    ('医疗服务','#EC407A'),('医疗器械','#F06292'),('电力','#EF5350'),
    ('光伏','#FF7043'),('国产算力','#26A69A'),('有色金属','#78909C'),
    ('医药生物','#B0BEC5'),
]

DATA_DIR = '/Users/mac/hermes/sector-fund-flow/data/'
OUTPUT_DIR = '/Users/mac/hermes/sector-fund-flow/output/'
os.makedirs(OUTPUT_DIR, exist_ok=True)

today = datetime.now().strftime('%Y-%m-%d')
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'PingFang SC', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# Read CSVs (divide by 1e8 to convert to 亿)
dfs = {}
for n, _ in sectors_info:
    df = pd.read_csv(f'{DATA_DIR}{n}_fund_flow.csv')
    df['mainForce'] = df['mainForce'] / 1e8
    dfs[n] = df

times = dfs['存储芯片']['time'].tolist()
N = len(times)

# Sort by latest value (descending)
latest = {n: dfs[n]['mainForce'].iloc[-1] for n, _ in sectors_info}
sorted_sectors = sorted(sectors_info, key=lambda x: latest[x[0]], reverse=True)

all_vals = np.concatenate([dfs[n]['mainForce'].values for n, _ in sectors_info])
y_min, y_max = all_vals.min(), all_vals.max()
y_margin = (y_max - y_min) * 0.15

from matplotlib.ticker import FuncFormatter
def y_fmt(x, pos=None):
    return f'{int(x)}亿'
formatter = FuncFormatter(y_fmt)

W, H, DPI = 1080, 1920, 120
fig, ax = plt.subplots(figsize=(W/DPI, H/DPI), dpi=DPI)
fig.patch.set_facecolor('#0f0f23')
ax.set_facecolor('#0f0f23')

def update(frame):
    ax.cla()
    ax.set_xlim(0, N-1)
    ax.set_ylim(y_min - y_margin, y_max + y_margin)
    ax.yaxis.set_major_formatter(formatter)
    tick_step = max(1, N // 6)
    tick_labels = [times[i].split(' ')[1] if ' ' in times[i] else times[i] for i in range(0, N, tick_step)]
    ax.set_xticks(list(range(0, N, tick_step)))
    ax.set_xticklabels(tick_labels, fontsize=8, color='#aaa')
    ax.axhline(0, color='white', linewidth=0.8, alpha=0.4)
    ax.spines[:].set_color('#333')
    ax.tick_params(colors='white', labelsize=8)
    ax.grid(True, alpha=0.08, color='white', axis='y')

    # 15:00 golden dashed line
    target_idx = next((i for i, t in enumerate(times) if '15:00' in t), N-1)
    label_time = times[target_idx].split(' ')[1] if ' ' in times[target_idx] else times[target_idx]
    ax.axvline(x=target_idx, color='#FFD700', linewidth=1.2, linestyle='--', alpha=0.7)
    ax.text(target_idx, y_max + y_margin * 0.3, label_time, color='#FFD700', fontsize=9,
            ha='center', va='bottom', fontweight='bold')

    idx = min(frame, N-1)
    for name, color in sorted_sectors:
        df = dfs[name]
        mf_s = df['mainForce'].iloc[:idx+1].values
        ax.plot(np.arange(len(mf_s)), mf_s, color=color, linewidth=1.4, alpha=0.85)
        last_val = mf_s[-1]
        sign = '+' if last_val >= 0 else ''
        label_text = f'{name} {sign}{last_val:.1f}'
        ax.annotate(label_text,
                    xy=(len(mf_s)-1, last_val),
                    xytext=(len(mf_s)+1, last_val),
                    color='white', fontsize=8, va='center', fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor=color, alpha=0.85, edgecolor='none'),
                    arrowprops=dict(arrowstyle='->', color=color, alpha=0.6))

    ax.text(0.5, -0.06, '数据区间 09:31 ~ 15:00', transform=ax.transAxes,
            color='#888', fontsize=9, ha='center')
    # Title on figure
    fig.suptitle(f'主力资金板块分时流向对比  {today}', color='white',
                 fontsize=18, fontweight='bold', y=0.97)

# 3x speed: interval=67ms, fps=15
ani = animation.FuncAnimation(fig, update, frames=N, blit=False, interval=67)
save_path = f'{OUTPUT_DIR}{today}_主力资金分时对比.mp4'
print(f'Generating video → {save_path}')
ani.save(save_path, writer='ffmpeg', fps=15, dpi=DPI, codec='libx264',
         extra_args=['-pix_fmt', 'yuv420p'])
plt.close()
print(f'✅ Video generated: {save_path}')
print(f'   size: {os.path.getsize(save_path)/1024:.1f} KB')