---
type: concept
title: "地缘政治风险（GPR）理论建模方法论"
created: 2026-08-10
source: "[[raw/notes/2026-05-01_gpr-modeling-methods]]"
related:
  concepts: [dsge-gpr-two-country-model]
  topics: []
tags: [gpr, dsge, macroeconomics, investment, risk-premium]
---

# 地缘政治风险（GPR）理论建模方法论

来源: [[raw/notes/2026-05-01_gpr-modeling-methods|GPR建模方法论（Fisher IMA笔记）]]

## 核心思想

将 GPR 纳入理论模型的核心在于：将其建模为一个**外生的、持续性的随机冲击过程**，通过改变经济主体的预期和决策环境来影响其行为。

GPR 指数本身建模为外生 AR(1) 过程：

$$GPR_t = \rho GPR_{t-1} + \varepsilon_t, \quad \varepsilon_t \sim N(0, \sigma^2)$$

---

## 两大建模入口

### 方法 A：家庭部门效用函数

**A1. 时变折现因子（SDF）**

令主观折现因子 $\beta_t$ 随 GPR 变化：

$$\beta_t = \bar{\beta} \cdot \exp(-\phi Z_t)$$

机制：GPR↑ → $\beta_t$↓ → 家庭更偏当期消费 → 投资要求回报率↑ → 抑制投资

**A2. 时变风险规避系数**

$$\gamma_t = \bar{\gamma} + \psi GPR_t$$

机制：在 Epstein-Zin 偏好下，GPR↑ → $\gamma_t$↑ → 风险资产溢价↑ → 股票价格↓

### 方法 B：企业投资欧拉方程

**B1. 影响调整成本（实物期权渠道）**

$$\Phi_t = \Phi(I_t/K_t;\; GPR_t), \quad \Phi'_t \uparrow \text{ with } GPR_t$$

机制：GPR↑ → 调整成本↑ → "等待观望"期权价值↑ → 延迟不可逆投资

**B2. 影响资本回报波动率**

$$\sigma_{t+1}^K = \bar{\sigma} \cdot \exp(\kappa GPR_t)$$

机制：GPR↑ → 未来资本边际产出不确定性↑ → 投资风险溢价↑ → 抑制投资

---

## 与实证文献的对应

| 文献 | 适用模型方法 | 核心机制 |
|---|---|---|
| Wang et al. (2019) | 方法 B1 | 实物期权 / 等待观望 |
| Beirne (2025) | 方法 A1 | 时变折现率 / 风险溢价 |
| Agoraki et al. (2022) | 方法 A2 | 股票价格下跌 / 债券收益率上升 |
| Bouras et al. (2018) | 方法 A2 | 市场波动性上升 |
| Feng et al. (2023) | 方法 A1 + B1（两国模型） | 回国效应 + 安全港效应 |

---

## 关联概念

- [[dsge-gpr-two-country-model]] — 两国 DSGE 框架下的完整推导（Feng et al. 2023）
