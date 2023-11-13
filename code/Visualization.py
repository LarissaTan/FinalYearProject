# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt 
import statsmodels.api as sm
import pandas as pd
import arma as hs
import arma_related_func  as fr
import pre_interface as pre_face

import matplotlib.dates as mdates
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))


k=fr.diff_n # 差分阶数
# 绘制样本图
fig = plt.figure(figsize=(7,5))
dta_1=pd.Series(hs.dta)
p1=str(len(hs.dta))
dta_1.index = pd.Index(sm.tsa.datetools.dates_from_range('1',p1))
dta_1.plot(figsize=(7,5))


# 绘制一阶差分图
fig = plt.figure(figsize=(7,5))
dta_2=pd.Series(pre_face.dta_diff)
p2=str(len(hs.dta)-k)
dta_2.index = pd.Index(sm.tsa.datetools.dates_from_range('1',p2))
dta_2.plot()
plt.grid(True, linestyle = "-.", color = "r", linewidth = "1")

# 绘制预测图(还原差分)
dta_pre_inv=hs.ARMA_pre_inv[:]
fig = plt.figure(figsize=(7,5))
dta_3=pd.Series(dta_pre_inv)
p4=str(len(hs.dta)+7)
dta_3.index = pd.Index(sm.tsa.datetools.dates_from_range('1',p4))
dta_3.plot()
plt.grid(True, linestyle = "-.", color = "r", linewidth = "1") 

#python3 -u "/Users/tanqianqian/Desktop/FinalYearProject/code/Visualization.py"