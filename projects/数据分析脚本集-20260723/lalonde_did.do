use "/Users/mac/Library/Mobile Documents/iCloud~md~obsidian/Documents/oneinall/raw/05-书课资源/LSHTM Rmd/backupfiles/lalonde.dta", clear

* ============================================================
* Lalonde NSW Job Training Program - DID Analysis
* ============================================================

* Step 1: PSM倾向得分匹配
teffects psmatch (re78) (treat age educ black hispan married nodegree re74 re75), atet

* Step 2: DID回归 (OLS)
reg re78 treat age educ black hispan married nodegree, robust
estimates store did_naive

* Step 3: 带收入前定的DID
reg re78 treat age educ black hispan married nodegree re74 re75, robust
estimates store did_controls

* Step 4: 生成收入变化量 (准DID)
gen re_change = re78 - re74
gen re75_change = re75 - re74

* 收入变化的DID
reg re_change treat age educ black hispan married nodegree re74, robust
estimates store did_change

* 汇总表格
esttab did_naive did_controls did_change, star(* .1 ** .05 *** .01) ///
    title("Lalonde NSW - Treatment Effect Estimates") ///
    nonumber nogaps replace

* ============================================================
* 平行趋势检验 (安慰剂检验)
* ============================================================
* 使用1974年作为"伪处理后"年份
gen fake_treat = treat
reg re74 fake_treat age educ black hispan married nodegree, robust
di "Placebo test: coefficient on treat for pre-treatment period (re74)"
di "If parallel trends holds, this should be close to 0"

* 报告处理组和控制组的基本统计
bysort treat: summarize re74 re75 re78

esttab did_naive did_controls did_change using "/Users/mac/Library/Mobile Documents/iCloud~md~obsidian/Documents/oneinall/temp/lalonde_results.csv", csv replace
