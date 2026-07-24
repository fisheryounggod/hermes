#!/usr/bin/env python3
"""
work-planning-v2.py — 每日工作规划生成器 v2
=============================================
数据来源:
  1. 飞书 Bitable 文献清单 (tenant_access_token, 无需 OAuth)
  2. 实时市场数据 (S&P 500 via yfinance, A股 via 东方财富)

核心逻辑:
  - 读取当前研究阶段和待读文献
  - 结合市场关注点智能推荐今日优先级
  - 自动生成时间块规划

OAuth 方案说明:
  - 飞书 Bitable: 使用 tenant_access_token (App凭证, 无需用户授权, 永久有效)
  - 飞书任务(Todo): 需要 user OAuth, refresh_token 已过期, 需重新授权
  - 作为替代: 用 Bitable 文献表管理研究任务, 同样可以实现任务追踪
"""

import json
import urllib.request
import datetime
from pathlib import Path

# =============================================================================
# 凭证配置 (来自 ~/.hermes/.env)
# =============================================================================
FEISHU_APP_ID = "cli_a92714e0d2b8dbc4"
FEISHU_APP_SECRET = "Yi9VZBPGWlB17KBO1ks5mfKE5FQOUIiV"
BASE_TOKEN = "O26ebCYPRa56Nvsy48icxkMXn6O"
文献清单_TABLE = "tblaWA2qpMhkw2Po"

# 输出目录
OUTPUT_DIR = Path.home() / "workspace" / "planning"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DATE_STR = datetime.datetime.now().strftime("%Y-%m-%d")
WEEKDAY_CN = {
    "Monday": "星期一", "Tuesday": "星期二", "Wednesday": "星期三",
    "Thursday": "星期四", "Friday": "星期五", "Saturday": "星期六", "Sunday": "星期日"
}.get(datetime.datetime.now().strftime("%A"), datetime.datetime.now().strftime("%A"))
OUTPUT_FILE = OUTPUT_DIR / f"{DATE_STR}.md"

# 市场缓存
CACHE_FILE = Path.home() / "workspace" / ".market_cache.json"

# =============================================================================
# 工具函数
# =============================================================================

def get_tenant_token():
    """获取飞书 tenant_access_token (App凭证, 无需 OAuth, 永久有效)"""
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data=json.dumps({"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())["tenant_access_token"]


def fs_get(path):
    """飞书 GET 请求 (tenant token)"""
    url = f"https://open.feishu.cn/open-apis{path}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {TENANT_TOKEN}"})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())


# =============================================================================
# 市场数据
# =============================================================================

def fetch_market_data():
    """获取今日市场数据 (S&P 500, A股) — 带缓存，过夜后自动刷新"""
    market_info = {"sp500": None, "ashare": None}
    today = datetime.date.today().isoformat()

    # 读取缓存
    cache = {}
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE) as f:
                cache = json.load(f)
        except Exception:
            pass

    # 如果有今日缓存，直接使用
    if cache.get("date") == today and (cache.get("sp500") or cache.get("ashare")):
        print(f"  [CACHE] Using cached market data from {cache['date']}")
        return {"sp500": cache.get("sp500"), "ashare": cache.get("ashare")}

    # 1. S&P 500 — yfinance
    try:
        import yfinance as yf
        ticker = yf.Ticker("^GSPC")
        hist = ticker.history(period="5d", timeout=10)
        if len(hist) >= 2:
            closes = hist["Close"].dropna()
            if len(closes) >= 2:
                current = float(closes.iloc[-1])
                prev = float(closes.iloc[-2])
                change = (current - prev) / prev * 100
                market_info["sp500"] = {
                    "value": round(current, 2),
                    "change": round(change, 2),
                    "direction": "📈" if change >= 0 else "📉"
                }
    except Exception as e:
        print(f"  [WARN] S&P 500 fetch failed: {e}")

    # 2. A股 — 东方财富上证指数
    try:
        ashare_url = "https://push2.eastmoney.com/api/qt/stock/get?secid=1.000001&fields=f43,f169,f170"
        req = urllib.request.Request(ashare_url, headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://eastmoney.com"
        })
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read())
        item = data["data"]
        current = item["f43"] / 100
        prev = item["f170"] / 100
        change = (current - prev) / prev * 100
        market_info["ashare"] = {
            "value": round(current, 2),
            "change": round(change, 2),
            "direction": "📈" if change >= 0 else "📉"
        }
    except Exception as e:
        print(f"  [WARN] A股 fetch failed: {e}")

    # 写入缓存
    if market_info["sp500"] or market_info["ashare"]:
        cache = {"date": today, **market_info}
        try:
            with open(CACHE_FILE, "w") as f:
                json.dump(cache, f)
        except Exception:
            pass

    return market_info


# =============================================================================
# 飞书文献数据
# =============================================================================

def fetch_literature_tasks():
    """从飞书 Bitable 文献清单读取研究任务"""
    tasks = {"in_progress": [], "todo": []}

    try:
        result = fs_get(f"/bitable/v1/apps/{BASE_TOKEN}/tables/{文献清单_TABLE}/records?page_size=50")
        if result.get("code") != 0:
            print(f"  [WARN] Bitable API error: {result.get('msg')}")
            return tasks

        for item in result["data"]["items"]:
            fields = item.get("fields", {})
            status = fields.get("状态", "")
            title = fields.get("文献标题", "(无标题)")
            author = fields.get("作者", "")
            stage = fields.get("阶段", "")
            hours = fields.get("预计时间（小时）", "")
            importance = fields.get("重要性", "")
            note = fields.get("备注", "")

            task_info = {
                "title": f"{author} — {title}" if author else title,
                "stage": stage,
                "hours": hours,
                "importance": importance,
                "note": note,
                "status": status
            }

            if "🟡 进行中" in status:
                tasks["in_progress"].append(task_info)
            elif "⏳ 待开始" in status:
                tasks["todo"].append(task_info)

    except Exception as e:
        print(f"  [WARN] Literature fetch error: {e}")

    return tasks


# =============================================================================
# 规划构建
# =============================================================================

def build_core_objectives(tasks, market_info):
    """根据文献阶段和市场数据构建今日核心目标"""
    objectives = []

    # 优先级1: 进行中文献
    if tasks["in_progress"]:
        obj = tasks["in_progress"][0]
        objectives.append(f"继续阅读: {obj['title']}")
        if obj.get('note'):
            objectives.append(f"  → {obj['note']}")

    # 优先级2: 待开始文献中重要性高的
    high_priority = [t for t in tasks["todo"] if "⭐⭐" in t.get("importance", "") or "⭐⭐⭐" in t.get("importance", "")]
    if high_priority and not tasks["in_progress"]:
        obj = high_priority[0]
        objectives.append(f"开始阅读: {obj['title']} ({obj.get('hours', '?')}h)")
        if len(high_priority) > 1:
            objectives.append(f"  备选: {high_priority[1]['title']}")

    # 优先级3: 市场相关文献
    market_keywords = ["monetary policy", "interest rate", "CBDC", "digital currency", "capital flow", "政策", "货币"]
    market_tasks = [t for t in tasks["todo"] if any(kw.lower() in t["title"].lower() for kw in market_keywords)]
    if market_tasks and len(objectives) < 2:
        obj = market_tasks[0]
        objectives.append(f"市场相关: {obj['title']}")

    # 如果什么都没有
    if not objectives:
        objectives.append("梳理研究框架，制定下一阶段阅读计划")

    return objectives


def build_time_blocks(tasks, market_info):
    """构建时间块规划"""
    blocks = []

    # 09:00-10:00 — 晨间准备 + 市场速览
    market_desc = ""
    if market_info["sp500"]:
        s = market_info["sp500"]
        market_desc = f"S&P 500: {s['value']} {s['direction']}{s['change']:+.2f}%"
    if market_info["ashare"]:
        a = market_info["ashare"]
        market_desc += f" | 上证: {a['value']} {a['direction']}{a['change']:+.2f}%"

    blocks.append({
        "time": "09:00-10:00",
        "name": "晨间准备 + 市场速览",
        "tasks": ["查看隔夜美股收盘", "A股开盘前情绪", "宏观新闻晨读"],
        "detail": market_desc if market_desc else "市场数据暂不可用",
        "status": ""
    })

    # 10:00-12:00 — 深度研究 (进行中文献)
    if tasks["in_progress"]:
        t = tasks["in_progress"][0]
        blocks.append({
            "time": "10:00-12:00",
            "name": "深度研究时段",
            "tasks": [f"精读: {t['title']}", f"阶段: {t['stage']}", "做阅读笔记 (ABC框架)"],
            "detail": f"预计耗时: {t.get('hours', '?')}小时 | 重要性: {t.get('importance', '')}",
            "status": ""
        })
    else:
        blocks.append({
            "time": "10:00-12:00",
            "name": "深度研究时段",
            "tasks": ["阅读待开始文献", "梳理文章结构", "记录关键科学问题"],
            "detail": "选择重要性最高的待读文献",
            "status": ""
        })

    # 12:00-14:00 — 午休
    blocks.append({
        "time": "12:00-14:00",
        "name": "午休",
        "tasks": [],
        "detail": "",
        "status": "⏸️ 休息"
    })

    # 14:00-16:00 — 第二研究时段
    if len(tasks["in_progress"]) > 1:
        t = tasks["in_progress"][1]
        blocks.append({
            "time": "14:00-16:00",
            "name": "辅助研究",
            "tasks": [f"阅读: {t['title']}", "补充笔记"],
            "detail": f"预计耗时: {t.get('hours', '?')}h",
            "status": ""
        })
    elif tasks["todo"]:
        t = tasks["todo"][0]
        blocks.append({
            "time": "14:00-16:00",
            "name": "文献阅读",
            "tasks": [f"开始: {t['title']}", "第一遍泛读", "确定精读重点"],
            "detail": f"预计耗时: {t.get('hours', '?')}h | {t.get('importance', '')}",
            "status": ""
        })
    else:
        blocks.append({
            "time": "14:00-16:00",
            "name": "研究整理",
            "tasks": ["整理阅读笔记", "更新飞书文献表"],
            "detail": "",
            "status": ""
        })

    # 16:00-18:00 — 投资分析 / 策略研究
    blocks.append({
        "time": "16:00-18:00",
        "name": "市场分析与策略",
        "tasks": ["分析当前市场主线", "跟踪 S&P 500 走势", "A股市场情绪"],
        "detail": "结合研究方向寻找市场与文献的交叉点",
        "status": ""
    })

    # 19:00-21:00 — 弹性时间
    blocks.append({
        "time": "19:00-21:00",
        "name": "弹性时间",
        "tasks": ["英语直播学习 (海外电商)", "或继续研究", "或休息娱乐"],
        "detail": "根据今日精力状况灵活安排",
        "status": ""
    })

    return blocks


def generate_markdown(tasks, market_info, objectives, time_blocks):
    """生成完整的 Markdown 规划文档"""

    # 市场数据摘要行
    market_lines = []
    if market_info["sp500"]:
        s = market_info["sp500"]
        market_lines.append(f"S&P 500: {s['value']} {s['direction']}{s['change']:+.2f}%")
    if market_info["ashare"]:
        a = market_info["ashare"]
        market_lines.append(f"上证: {a['value']} {a['direction']}{a['change']:+.2f}%")

    # 进行中文献
    in_progress_lines = []
    for t in tasks["in_progress"]:
        note_str = f" → {t['note']}" if t.get("note") else ""
        in_progress_lines.append(f"- {t['title']} | {t['stage']} | {t.get('hours','?')}h | {t.get('importance','')}{note_str}")

    # 待开始文献 (前8条)
    todo_lines = []
    for t in tasks["todo"][:8]:
        todo_lines.append(f"- {t['title']} | {t['stage']} | {t.get('hours','?')}h | {t.get('importance','')}")

    md = f"""# 工作规划 — {DATE_STR}（{WEEKDAY_CN}）

> 自动生成于 {datetime.datetime.now().strftime('%H:%M:%S')}
> 数据来源: 飞书 Bitable 文献清单 + 实时市场数据

---

## 📊 今日市场

{chr(10).join(market_lines) if market_lines else '_市场数据暂不可用_'}

---

## 🎯 今日核心目标

{chr(10).join(f'{i+1}. {obj}' for i, obj in enumerate(objectives))}

---

## 📋 研究进度

### 🔄 进行中
{in_progress_lines[0] if in_progress_lines else '- 无'}

### ⏳ 待开始（{len(tasks["todo"])} 条）
{chr(10).join(todo_lines) if todo_lines else '- 无'}

---

## ⏰ 时间块规划

| 时间段 | 事项 | 详情 | 状态 |
|--------|------|------|------|
"""
    for b in time_blocks:
        md += f"| {b['time']} | {b['name']} | {b['detail']} | {b['status']} |\n"

    md += f"""
---

## 📝 今日记录

_（晚间填写：完成情况、遇到的卡点、新想法）_

---

## 🔮 明日预判

- 继续当前文献 or 开始新文献:
- 市场关注点:
- 需要调整的时间块:

"""
    return md


# =============================================================================
# 主流程
# =============================================================================
if __name__ == "__main__":
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] 开始生成工作规划...")

    # 1. 获取 tenant token
    global TENANT_TOKEN
    TENANT_TOKEN = get_tenant_token()
    print(f"  ✓ Tenant token obtained")

    # 2. 读取研究任务
    print("  ⟳ 读取飞书文献清单...")
    tasks = fetch_literature_tasks()
    print(f"  ✓ 进行中: {len(tasks['in_progress'])} | 待开始: {len(tasks['todo'])}")

    # 3. 获取市场数据
    print("  ⟳ 读取市场数据...")
    market_info = fetch_market_data()
    if market_info["sp500"]:
        print(f"  ✓ S&P 500: {market_info['sp500']['value']} ({market_info['sp500']['change']:+.2f}%)")
    if market_info["ashare"]:
        print(f"  ✓ 上证: {market_info['ashare']['value']} ({market_info['ashare']['change']:+.2f}%)")

    # 4. 构建目标和时间块
    objectives = build_core_objectives(tasks, market_info)
    time_blocks = build_time_blocks(tasks, market_info)

    # 5. 生成 Markdown
    md = generate_markdown(tasks, market_info, objectives, time_blocks)

    # 6. 写入文件
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"\n✅ 规划已生成: {OUTPUT_FILE}")
    print(f"   核心目标: {len(objectives)} 项")
    print(f"   时间块: {len(time_blocks)} 个")

    # 7. 输出关键信息 (供 cron job 上报)
    print("\n--- SUMMARY ---")
    print(f"DATE: {DATE_STR}")
    print(f"TASKS_IN_PROGRESS: {len(tasks['in_progress'])}")
    print(f"TASKS_TODO: {len(tasks['todo'])}")
    if market_info["sp500"]:
        s = market_info["sp500"]
        print(f"SP500: {s['value']} ({'+' if s['change'] >= 0 else ''}{s['change']}%)")
    if market_info["ashare"]:
        a = market_info["ashare"]
        print(f"ASHARE: {a['value']} ({'+' if a['change'] >= 0 else ''}{a['change']}%)")
    for i, obj in enumerate(objectives):
        print(f"OBJECTIVE_{i+1}: {obj}")
