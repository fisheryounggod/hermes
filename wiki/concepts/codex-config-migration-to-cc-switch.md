---
title: "将 Codex 配置迁移到 cc-switch"
type: concept
aliases:
  - Codex 配置迁移
  - cc-switch Codex 接管
tags:
  - codex
  - cc-switch
  - configuration
  - windows
  - migration
sources:
  - "[[raw/articles/2026-08-09_canghe-codex-obsidian-llm-wiki|Codex 与本地知识库实践背景]]"
created: 2026-08-10
updated: 2026-08-10
---

# 将 Codex 配置迁移到 cc-switch

> [!warning] 来源说明
> 本文操作步骤来自 2026-08-10 Windows 本机迁移实测，不是上述 raw 文章的原文内容。raw 来源仅提供 Codex、本地文件与 Obsidian 协作的背景。cc-switch 的数据库表结构可能随版本变化，数据库操作部分应视为版本相关并在执行前备份。

## 目标

把现有 Codex 自定义提供商配置迁移到 cc-switch，让 cc-switch 统一管理：

- API Key；
- 上游 `base_url`；
- Responses API 格式；
- 当前提供商切换；
- 本地代理接管和请求日志；
- Codex 公共配置与项目配置。

迁移成功后的请求链路通常是：

```text
Codex
  -> http://127.0.0.1:15721/v1/responses
  -> cc-switch 当前 Codex 提供商
  -> https://example.com/codex/responses
```

这类本地配置管理属于 [[wiki/concepts/ai-agent-knowledge-curation|AI Agent 长期维护]] 的基础设施层，也适合记录在 [[wiki/concepts/raw-wiki-schema-architecture|Raw / Wiki / Schema 架构]] 的 Schema 侧。

## 适用环境

- Windows 10/11；
- Codex 配置目录：`C:\Users\<用户名>\.codex`；
- cc-switch 数据目录：`C:\Users\<用户名>\.cc-switch`；
- cc-switch 本地代理默认示例：`127.0.0.1:15721`；
- 自定义上游使用 OpenAI Responses API。

本文命令在 PowerShell 中执行。

## 迁移前必须理解的三份状态

### Codex 实时配置

主要文件：

```text
~\.codex\config.toml
~\.codex\auth.json
```

自定义提供商常见配置如下：

```toml
model = "gpt-5.x"
model_provider = "custom-provider"

[model_providers.custom-provider]
name = "custom-provider"
base_url = "https://example.com/codex"
wire_api = "responses"
env_key = "CODEX_API_KEY"
```

注意：上游地址通常写到服务根路径，不要手工重复追加 `/responses`。Codex 或 cc-switch 会根据 `wire_api = "responses"` 请求对应端点。

### 凭据来源

凭据可能同时出现在：

- 用户环境变量 `CODEX_API_KEY`；
- `.codex/auth.json` 的 `OPENAI_API_KEY`；
- `config.toml` 的 `experimental_bearer_token`；
- cc-switch 数据库 `providers.settings_config` 的认证对象。

迁移前先确认当前实际使用哪个值。不要把 `PROXY_MANAGED` 当作真实 API Key；它只是 cc-switch 代理接管时写入实时配置的占位标记。

检查用户级环境变量是否存在，不输出具体内容：

```powershell
$key = [Environment]::GetEnvironmentVariable('CODEX_API_KEY', 'User')
if ($key) {
    "CODEX_API_KEY 已设置，长度：$($key.Length)"
} else {
    'CODEX_API_KEY 未设置'
}
```

### cc-switch 持久配置和实时代理配置

cc-switch 会把提供商持久化到：

```text
~\.cc-switch\cc-switch.db
```

启用代理接管后，cc-switch 还会临时重写 `.codex/config.toml`：

```toml
base_url = "http://127.0.0.1:15721/v1"
experimental_bearer_token = "PROXY_MANAGED"
```

这是正常状态。真正的上游 URL 应保存在 cc-switch 的提供商记录中。

> [!danger] 防止代理循环
> 如果当前 `config.toml` 已经指向 `127.0.0.1:15721`，不要把它作为上游配置重新导入 cc-switch，否则可能形成“cc-switch 转发给自己”的循环。应先关闭代理接管并恢复 Live 配置，或从迁移前备份中读取原始上游地址。

## 推荐迁移方法：通过 cc-switch 界面

### 1. 记录现有配置

查看配置时先脱敏：

```powershell
$config = Get-Content -Raw "$env:USERPROFILE\.codex\config.toml"
$config `
    -replace '(?im)(api[_-]?key\s*=\s*["''])(.*?)(["''])', '$1***$3' `
    -replace '(?im)(experimental_bearer_token\s*=\s*").*?(")', '$1***$2'
```

至少记录以下字段：

- `model`；
- `model_reasoning_effort`；
- `model_provider`；
- `base_url`；
- `wire_api`；
- `env_key`；
- 自定义 HTTP Headers；
- 当前有效 API Key 的来源。

### 2. 备份 Codex 和 cc-switch

先从系统托盘正常退出 cc-switch，再备份：

```powershell
$stamp = Get-Date -Format 'yyyyMMdd_HHmmss'

Copy-Item `
    "$env:USERPROFILE\.codex\config.toml" `
    "$env:USERPROFILE\.codex\config.toml.backup.$stamp"

& sqlite3 `
    "$env:USERPROFILE\.cc-switch\cc-switch.db" `
    ".backup '$env:USERPROFILE/.cc-switch/backups/db_backup_before_codex_migration_$stamp.db'"
```

如果没有 `sqlite3`，至少在 cc-switch 完全退出后复制 `cc-switch.db`。应用运行时直接复制数据库可能遗漏 WAL 中尚未合并的数据。

### 3. 新建或编辑 Codex 提供商

在 cc-switch 的 Codex 页面新建或编辑提供商：

| 字段 | 建议值 |
|---|---|
| 应用 | Codex |
| 名称 | 自定义，例如 `GPT2EDU` |
| API 格式 | OpenAI Responses |
| Base URL | 原始上游，例如 `https://example.com/codex` |
| API Key | 当前真实有效的 Key |
| 当前提供商 | 开启 |
| 自动选择端点 | 按需要开启 |

提供商配置中保留模型、推理强度、插件和 feature 配置。API Key 应放在 cc-switch 的认证字段中，不要把真实 Key 明文写进教程、截图或公开仓库。

### 4. 检查端点

如果提供商曾经使用旧域名，必须同时修改“提供商配置”和“端点列表”。只改 `config.toml` 而不改 cc-switch 端点，代理仍可能继续请求旧地址。

典型故障表现：

```text
请求目标: https://old.example.com/codex/responses
请求超时: upstream request timeout
```

### 5. 启用本地代理接管

在 cc-switch 中：

1. 将新提供商设为当前 Codex 提供商；
2. 开启本地代理；
3. 开启 Codex 代理接管；
4. 确认监听地址和端口；
5. 让 cc-switch 保持运行。

接管后再次查看 `.codex/config.toml`，`base_url` 应指向本地代理，而不是上游地址。

## 高级方法：直接修复 cc-switch 数据库

只有在界面无法导入、提供商记录损坏或端点残留时才使用本节。先退出 cc-switch，并确保已经备份数据库。

### 查看表结构和 Codex 提供商

```powershell
$db = "$env:USERPROFILE\.cc-switch\cc-switch.db"

& sqlite3 $db '.schema providers'
& sqlite3 $db '.schema provider_endpoints'
& sqlite3 -header -column $db `
    "SELECT id, name, is_current FROM providers WHERE app_type='codex';"
```

不要直接打印完整 `settings_config`，其中可能包含 API Key。

### 更新已有提供商

下面脚本读取迁移前的 Codex 配置和用户级 `CODEX_API_KEY`，写入指定提供商。执行前必须替换 `$providerId` 和 `$upstreamUrl`。

```powershell
$ErrorActionPreference = 'Stop'

$providerId = '<provider-id>'
$upstreamUrl = 'https://example.com/codex'
$db = "$env:USERPROFILE\.cc-switch\cc-switch.db"
$configPath = "$env:USERPROFILE\.codex\config.toml"
$stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$backup = "$env:USERPROFILE\.cc-switch\backups\db_backup_before_codex_migration_$stamp.db"

$config = Get-Content -Raw $configPath
if ($config -match 'base_url\s*=\s*"http://127\.0\.0\.1:15721') {
    throw '当前是 cc-switch 代理配置，不能作为上游配置导入。'
}

$apiKey = [Environment]::GetEnvironmentVariable('CODEX_API_KEY', 'User')
if ([string]::IsNullOrWhiteSpace($apiKey)) {
    throw '用户级 CODEX_API_KEY 未设置。'
}

& sqlite3 $db ".backup '$($backup.Replace('\', '/'))'"
if ($LASTEXITCODE -ne 0) {
    throw '数据库备份失败。'
}

$settings = @{
    auth = @{ OPENAI_API_KEY = $apiKey }
    config = $config
} | ConvertTo-Json -Compress -Depth 5

$escapedSettings = $settings.Replace("'", "''")
$escapedProviderId = $providerId.Replace("'", "''")
$escapedUrl = $upstreamUrl.Replace("'", "''")
$now = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()

$sql = @"
BEGIN IMMEDIATE;
UPDATE providers
SET settings_config = '$escapedSettings', is_current = 1
WHERE id = '$escapedProviderId' AND app_type = 'codex';

UPDATE providers
SET is_current = 0
WHERE id <> '$escapedProviderId' AND app_type = 'codex';

UPDATE provider_endpoints
SET url = '$escapedUrl', added_at = $now
WHERE provider_id = '$escapedProviderId' AND app_type = 'codex';
COMMIT;
"@

& sqlite3 $db $sql
if ($LASTEXITCODE -ne 0) {
    throw '数据库更新失败，请使用备份回滚。'
}
```

> [!note]
> 不同 cc-switch 版本的 schema 可能不同。例如 `providers` 表未必存在 `updated_at`。先查看 `.schema`，不要凭经验添加不存在的列。

完成后重启 cc-switch：

```powershell
Start-Process `
    "$env:LOCALAPPDATA\Programs\CC Switch\cc-switch.exe" `
    -WindowStyle Hidden
```

## 验证迁移

### 数据库完整性

```powershell
& sqlite3 "$env:USERPROFILE\.cc-switch\cc-switch.db" 'PRAGMA quick_check;'
```

期望输出：

```text
ok
```

### 当前提供商和上游端点

```powershell
$db = "$env:USERPROFILE\.cc-switch\cc-switch.db"

& sqlite3 -header -column $db `
    "SELECT id, name, is_current FROM providers WHERE app_type='codex';"

& sqlite3 -header -column $db `
    "SELECT provider_id, url FROM provider_endpoints WHERE app_type='codex';"
```

应满足：

- 只有一个 Codex 提供商的 `is_current = 1`；
- `provider_endpoints.url` 是正确的上游地址；
- 上游地址不是 `127.0.0.1`。

### 本地代理端口

```powershell
Test-NetConnection `
    -ComputerName 127.0.0.1 `
    -Port 15721 `
    -InformationLevel Quiet
```

期望输出：`True`。

### 最小 Responses 请求

这一步会真实调用模型并产生少量用量：

```powershell
$headers = @{
    Authorization = 'Bearer PROXY_MANAGED'
    'Content-Type' = 'application/json'
}

$body = @{
    model = 'gpt-5.x'
    input = 'Reply with exactly OK.'
    store = $false
    max_output_tokens = 16
} | ConvertTo-Json -Compress

$response = Invoke-RestMethod `
    -Uri 'http://127.0.0.1:15721/v1/responses' `
    -Method Post `
    -Headers $headers `
    -Body $body `
    -TimeoutSec 90

$response.output.content.text
```

期望返回 `OK`。实际模型名应替换为提供商支持的模型。

### 检查转发日志

```powershell
Get-Content `
    "$env:USERPROFILE\.cc-switch\logs\cc-switch.log" `
    -Tail 50 |
    Select-String -Pattern '\[Codex\].*请求目标|请求失败'
```

日志中的目标应是新上游，例如：

```text
[Codex] >>> 请求目标: https://example.com/codex/responses
```

## 常见故障

| 症状 | 原因 | 处理 |
|---|---|---|
| 仍请求旧域名 | `provider_endpoints` 未同步 | 同时更新提供商配置和端点列表 |
| 请求发给 localhost 后循环 | 把代理 Live 配置当成上游导入 | 恢复迁移前配置，重新填写真实上游 |
| 401/403 | Key 来源错误或已失效 | 核对用户级 `CODEX_API_KEY` 和 cc-switch 认证字段 |
| Key 被写成 `PROXY_MANAGED` | 把代理占位符当成真实 Key | 从安全来源重新填写真实 Key |
| 修改 `config.toml` 后被覆盖 | cc-switch 正在代理接管 | 在 cc-switch 中修改持久配置，或先关闭接管 |
| cc-switch 重启后恢复旧配置 | 上次异常退出，Live backup 被恢复 | 正常退出后修改数据库，并检查启动日志 |
| 请求超时 | 上游地址、网络或域名失效 | 先检查日志中的最终请求目标，再检查网络 |
| SQL 报列不存在 | cc-switch 版本 schema 不同 | 先运行 `.schema providers`，按实际列调整 |

## 回滚

1. 从系统托盘正常退出 cc-switch；
2. 找到迁移前数据库备份；
3. 使用 SQLite 恢复；
4. 重启 cc-switch；
5. 检查 `.codex/config.toml` 是否恢复。

```powershell
$db = "$env:USERPROFILE\.cc-switch\cc-switch.db"
$backup = "$env:USERPROFILE\.cc-switch\backups\db_backup_before_codex_migration_YYYYMMDD_HHMMSS.db"

& sqlite3 $db ".restore '$($backup.Replace('\', '/'))'"

Start-Process `
    "$env:LOCALAPPDATA\Programs\CC Switch\cc-switch.exe" `
    -WindowStyle Hidden
```

如果 Codex 实时配置没有自动恢复，可将 `config.toml.backup.<时间戳>` 复制回 `.codex/config.toml`。

## 安全清单

- [ ] 教程、日志和截图中没有真实 API Key；
- [ ] 数据库备份保存在本机私有目录；
- [ ] 没有把 `.codex/auth.json` 或 `cc-switch.db` 提交到 Git；
- [ ] 没有把 `PROXY_MANAGED` 当成真实凭据；
- [ ] 上游 URL 与本地代理 URL 没有混淆；
- [ ] 迁移后完成了最小 Responses 请求验证；
- [ ] 确认 cc-switch 日志实际请求的是新上游。

## 相关页面

- [[wiki/concepts/ai-agent-knowledge-curation]]
- [[wiki/concepts/raw-wiki-schema-architecture]]
- [[wiki/concepts/llm-wiki]]
- [[wiki/topics/llm-wiki-and-self-growing-pkms]]

## 来源

- [[raw/articles/2026-08-09_canghe-codex-obsidian-llm-wiki]] — Codex、Obsidian 与本地 Markdown 协作背景
- 本机实测：`~\.codex\config.toml`、`~\.cc-switch\cc-switch.db`、`~\.cc-switch\logs\cc-switch.log`（2026-08-10，未写入凭据）

## 待核实问题

- [ ] cc-switch 后续版本是否提供稳定的“从 Live 配置重新导入”入口；
- [ ] 不同版本对 `experimental_bearer_token` 的写入策略是否一致；
- [ ] cc-switch 数据库 schema 升级后，`providers` 和 `provider_endpoints` 字段是否变化；
- [ ] 官方 OpenAI Docs 恢复可访问后，补充 Codex 最新配置字段链接。
