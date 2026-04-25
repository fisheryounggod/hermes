#!/usr/bin/env python3
"""
S&P 500 - Last 5 Days Ultra Simple Chart
Most minimal and reliable approach
"""

import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

print("Getting S&P 500 data for last week...")

# Get data
end_date = datetime.now()
start_date = end_date - timedelta(days=10)

# Download S&P 500 data
ticker = "^GSPC"
df = yf.download(ticker, start=start_date, end=end_date, interval="1d")

print(f"Downloaded {len(df)} days")

# Take last 5 trading days
df_last_week = df.tail(5).copy()

# Simple extraction
dates = df_last_week.index
closes = df_last_week['Close'].values

# Calculate summary
current_price = closes[-1]
high_price = closes.max()
low_price = closes.min()
avg_price = closes.mean()

# Create chart
fig, ax = plt.subplots(figsize=(12, 6))
fig.suptitle('S&P 500 - Last 5 Days', fontsize=14, fontweight='bold')

# Plot closing price trend
ax.plot(dates, closes, label='Close Price', linewidth=2, color='#1f77b4', marker='o', markersize=6)
ax.set_xlabel('Date', fontsize=11)
ax.set_ylabel('Price ($)', fontsize=11)
ax.set_title('Price Trend', fontsize=12, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.legend(loc='upper left', fontsize=10)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))

# Adjust layout
plt.tight_layout()
plt.subplots_adjust(bottom=0.12)

# Save chart
output_file = '/home/yxf/clawd/sp500_5days_simple.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"Chart saved to: {output_file}")

# Simple data summary
print("\nData Summary:")
print("Current Price: " + str(round(current_price, 2)))
print("Week High: " + str(round(high_price, 2)))
print("Week Low: " + str(round(low_price, 2)))
print("Average Price: " + str(round(avg_price, 2)))

print(f"\nDone! Chart generated and saved.")
