# -*- coding: utf-8 -*-
import pre_interface as pre
import pandas as pd

def perform_arma_prediction(data):
    """
    Perform ARMA prediction on the given data.

    Parameters:
    - data (list): A list containing the time series data.
    - p (int): The order of the autoregressive (AR) component.
    - q (int): The order of the moving average (MA) component.
    - k (int): The number of steps to predict.

    Returns:
    - arma_prediction (list): The predicted values.
    """
    global ARMA_pre
    data = data

    # Perform ARMA prediction using the pre_interface module
    ARMA_pre, ARMA_pre_inv = pre.interface_pre(data, 3, 15, 1, 20)

    print('Predicted data:', ARMA_pre)
    
    return ARMA_pre

    # Example usage:
    # data = [75, 72, 70, 68, 75, 80, 82, 78, 80, 76]

'''
global ARMA_pre, data
data = [75, 72, 70, 68, 75, 80, 82, 78, 80, 76]


# 预测(dta,model,p,q=1,k=39)
print('the len of data:', len(data))
ARMA_pre, ARMA_pre_inv = pre.interface_pre(data, 3, 15, 1, 20)
print('predict data:', ARMA_pre)

'''

#python3 -u "/Users/tanqianqian/Desktop/FinalYearProject/code/arma.py"