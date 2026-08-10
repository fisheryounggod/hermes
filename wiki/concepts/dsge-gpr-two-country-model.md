---
type: concept
title: "两国 DSGE 模型引入 GPR 冲击：完整推导（Feng et al. 2023）"
created: 2026-08-10
source: "[[raw/notes/2026-05-01_dsge-gpr-two-country-model]]"
related:
  concepts: [gpr-theoretical-modeling]
  topics: []
tags: [gpr, dsge, two-country-model, capital-flow, emerging-markets, homeward-bias, safe-haven]
---

# 两国 DSGE 模型引入 GPR 冲击

来源: [[raw/notes/2026-05-01_dsge-gpr-two-country-model|DSGE引入GPR（Fisher IMA笔记，基于 Feng et al. 2023）]]

## 模型设定

两国框架：
- **本国（H）**：新兴市场（Emerging Market）
- **外国（F）**：发达国家（Advanced Economy）

通过贸易和国际资本流动相连，引入全球 GPR 指数（AR(1) 外生冲击）。

## 两个关键渠道

### 渠道 1：风险溢价渠道（家庭 SDF）

$$\beta_t = \bar{\beta} \cdot \exp(-\gamma_i Z_t), \quad \gamma_H > \gamma_F$$

GPR↑ → 两国 SDF↓ → 风险溢价↑，本国幅度更大（因 $\gamma_H > \gamma_F$）

### 渠道 2：资本效率渠道（企业端）

$$\omega_t = \bar{\omega} \cdot \exp(-\eta_i Z_t), \quad \eta_H > \eta_F$$

GPR↑ → 资本效率↓ → 预期 MPK↓ → 预期资本回报率↓，本国幅度更大

## 核心均衡条件

$$R_H^{adj} - R_F^{adj} = [MPK_H - (r + \gamma_H Z_t)] - [MPK_F - (r + \gamma_F Z_t)]$$

GPR↑ → 本国经风险调整后的回报率下降幅度 > 外国 → 国际资本向外国再配置

## 两大预测

- **回国效应（Homeward Bias Effect）**：GPR↑ → 跨境资本流动总体收缩，两国 OF 和 IF 均减少；新兴市场收缩幅度更大
- **安全港效应（Safe Haven Effect）**：GPR↑ → 本国 FDI 净流出增加（发达国家成为相对安全的投资目的地）

## 与 Feng et al. (2023) 的对应

| 实证发现 | 模型机制 |
|---|---|
| GPR↑ → 两国资本流动均减少 | 渠道 1：SDF↓，风险溢价↑ |
| 新兴市场收缩幅度更大 | $\gamma_H > \gamma_F$ |
| 新兴经济体 FDI 流入显著负向 | 渠道 2：本国资本效率↓幅度更大 |
| 发达经济体 FDI 流入正向/不显著 | 外国成为相对更吸引力的目的地 |

## 关联概念

- [[gpr-theoretical-modeling]] — GPR 建模的多种方法综述（方法 A1/A2/B1/B2）
