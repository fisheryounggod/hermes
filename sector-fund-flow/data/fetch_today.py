#!/usr/bin/env python3
"""Pull today's 22-sector main-force flow data from Eastmoney."""
import urllib.request, ssl, json, pandas as pd, os, sys, time
from datetime import datetime

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

SECTORS = {
    '存储芯片':'90.BK1137','电网设备':'90.BK0457','云计算':'90.BK0579',
    '人工智能':'90.BK0800','半导体材料设备':'90.BK1326','消费电子':'90.BK1037',
    'CPO':'90.BK1128','通信':'90.BK1215','半导体':'90.BK1036',
    '电力':'90.BK0428','大科技':'90.BK0891','光伏':'90.BK1031',
    '国产算力':'90.BK1134','先进制造':'90.BK1237','军工':'90.BK0490',
    '商业航天':'90.BK0963','AI应用':'90.BK1629','油气资源':'90.BK1649',
    '有色金属':'90.BK0478','医疗器械':'90.BK1045','医疗服务':'90.BK1044',
    '医药生物':'90.BK1043'
}

# Write to user-specified path
DATA_DIR = '/Users/mac/hermes/sector-fund-flow/data/'
os.makedirs(DATA_DIR, exist_ok=True)

# Also mirror to the skill's canonical location so future runs find it
CANONICAL = '/Users/mac/Downloads/Data/sector_data/'
os.makedirs(CANONICAL, exist_ok=True)

success = 0
for name, secid in SECTORS.items():
    url = (f'https://push2delay.eastmoney.com/api/qt/stock/fflow/kline/get'
           f'?lmt=0&klt=1&secid={secid}'
           f'&fields1=f1,f2,f3,f7'
           f'&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63')
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://data.eastmoney.com/'
    })
    try:
        resp = urllib.request.urlopen(req, context=ctx, timeout=20)
        data = json.loads(resp.read())
        klines = data.get('data', {}).get('klines', [])
        if klines:
            rows = []
            for k in klines:
                parts = k.split(',')
                rows.append({
                    'time': parts[0],
                    'sector': name,
                    'mainForce': float(parts[1]),
                    'small': float(parts[2]),
                    'medium': float(parts[3]),
                    'large': float(parts[4]),
                    'superLarge': float(parts[5]),
                })
            df = pd.DataFrame(rows)
            df.to_csv(f'{DATA_DIR}{name}_fund_flow.csv', index=False, encoding='utf-8-sig')
            df.to_csv(f'{CANONICAL}{name}_fund_flow.csv', index=False, encoding='utf-8-sig')
            success += 1
            last_t = rows[-1]['time']
            last_v = rows[-1]['mainForce'] / 1e8
            print(f'  ✅ {name}: {len(rows)} ticks, last={last_t} ({last_v:+.2f}亿)')
        else:
            print(f'  ⚠️  {name}: empty klines')
    except Exception as e:
        print(f'  ❌ {name}: {e}')
        time.sleep(0.5)

print(f'\n{success}/{len(SECTORS)} sectors fetched.')
print(f'Saved to: {DATA_DIR}')