# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt 
import statsmodels.api as sm
import pandas as pd
import arimia_test as hs
import arima_related_func as fr
import pre_interface as pre_face

import matplotlib.dates as mdates

k = fr.diff_n  # 差分阶数

# 绘制样本图
fig, ax1 = plt.subplots(figsize=(7, 5))
'''
dta_1 = pd.Series(hs.data)
p1 = str(len(hs.data))
ax1.plot(pd.to_datetime(pd.date_range(start='20000101', periods=int(p1), freq='D')), dta_1, label='Sample Data')
'''
# 绘制一阶差分图
dta_2 = pd.Series(pre_face.data_diff)
p2 = str(len(hs.data) - k)
ax1.plot(pd.to_datetime(pd.date_range(start='20000101', periods=int(p2), freq='D')), dta_2, label='First Difference')
ax1.set_title('Sample and First Difference Plots')
ax1.set_xlabel('Date')
ax1.set_ylabel('Data')
ax1.legend()
ax1.grid(True, linestyle="-.", color="r", linewidth="1")
'''
# 绘制预测图(还原差分)
ax2 = ax1.twinx()
dta_pre_inv = hs.ARMA_pre_inv[:]
p4 = str(len(hs.data) + 7)
ax2.plot(pd.to_datetime(pd.date_range(start='20000101', periods=int(p4), freq='D'))[:len(dta_pre_inv)], dta_pre_inv, label='Forecast')
ax2.set_ylabel('Forecast Data')
ax2.legend()
'''
plt.show()


#python3 -u "/Users/tanqianqian/Desktop/FinalYearProject/code/Visualization.py"