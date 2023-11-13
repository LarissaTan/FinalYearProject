# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt 
import statsmodels.api as sm
import pandas as pd
import arma as hs
import arma_related_func  as fr
import pre_interface as pre_face

import matplotlib.dates as mdates

k = fr.diff_n  # 差分阶数

# 绘制样本图
fig, ax1 = plt.subplots(figsize=(7, 5))
dta_1 = pd.Series(hs.dta)
p1 = str(len(hs.dta))
dta_1.index = pd.Index(mdates.date2num(sm.tsa.datetools.dates_from_range('1', p1)))
dta_1.plot(ax=ax1)

# 手动设置日期格式
ax1.xaxis.set_major_locator(mdates.DayLocator())  # 设置主刻度为每天
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))  # 设置日期格式

# 绘制一阶差分图
fig, ax2 = plt.subplots(figsize=(7, 5))
dta_2 = pd.Series(pre_face.dta_diff)
p2 = str(len(hs.dta) - k)
dta_2.index = pd.Index(mdates.date2num(sm.tsa.datetools.dates_from_range('1', p2)))
dta_2.plot(ax=ax2)
ax2.grid(True, linestyle="-.", color="r", linewidth="1")

# 绘制预测图(还原差分)
fig, ax3 = plt.subplots(figsize=(7, 5))
dta_pre_inv = hs.ARMA_pre_inv[:]
dta_3 = pd.Series(dta_pre_inv)
p4 = str(len(hs.dta) + 7)
dta_3.index = pd.Index(mdates.date2num(sm.tsa.datetools.dates_from_range('1', p4)))
dta_3.plot(ax=ax3)
ax3.grid(True, linestyle="-.", color="r", linewidth="1")

plt.show()
#python3 -u "/Users/tanqianqian/Desktop/FinalYearProject/code/Visualization.py"
