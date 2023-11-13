# -*- coding: utf-8 -*-
import pre_interface as pre
import pandas as pd

global ARMA_pre, data
data = [75, 72, 70, 68, 75, 80, 82, 78, 80, 76, 78, 75, 80, 85,
       88, 92, 88, 85, 78, 80, 85, 82, 78, 75, 80, 78, 85, 90,
       95, 92, 90, 88, 85, 82, 80, 78, 75, 80, 82, 88, 90, 92,
       95, 100, 98, 96, 92, 88, 85, 82, 80, 78, 75, 80, 78, 85,
       90, 95, 92, 90, 88, 85, 82, 80, 78, 75, 80, 82, 88, 90,
       92, 95, 100, 98, 96, 92, 88, 85, 82, 80, 78, 75, 80, 78,
       85, 90, 95, 92, 90, 88, 85, 82, 80, 78, 75, 80, 82, 88,
       90, 92, 95, 100, 98, 96, 92, 88, 85, 82, 80, 78, 75]


# 预测(dta,model,p,q=1,L=1,k=39)
print('the len of data:', len(data))
ARMA_pre, ARMA_pre_inv = pre.interface_pre(data, 3, 15, 1, 20)
print('predict data:', ARMA_pre)


#python3 -u "/Users/tanqianqian/Desktop/FinalYearProject/code/arma.py"