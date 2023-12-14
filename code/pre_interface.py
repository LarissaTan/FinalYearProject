# -*- coding: utf-8 -*-
import arima_related_func  as fr

# AR(P)模型预测和(data,p,k)
def ar_pre(data,p,k):  
    # 得到AR模型
    fai_mao,sigma2_ar=fr.model_ar(p,fai)
    len_pre=data_len-1
    data_pre=data_diff[:] # data_pre的改变不会影响fr.data_diff原数据
    fai_sum=0
    for i in range(1,p+1):
        fai_sum=fai_sum+fai_mao[i]
    theta0_ARpre=mean_data*(1-fai_sum)
    for LL in range(1,2):
        z_k=0
        for pp in range(1,p+1):
            z_k=z_k+fai_mao[pp]*data_pre[len_pre+LL-pp] # 数据是从后往前的
        data_pre.extend([theta0_ARpre+z_k])
    # 逆差分处理(差分数据,原数据的前n阶个,差分阶数)
    AR_pre_inv=fr.difference_inv(data_pre,data[0:fr.diff_n],fr.diff_n)
    return AR_pre_inv[data_len+1:],AR_pre_inv

# ARMA(P,1)模型预测未来和(data,p,q,k)
def arma_pre(data,p,q,k):
    #global fai_mao,sigma2_ar
    fai_mao,sigma2_ar=fr.model_ar(p,fai)
    # 得到ARMA(P,1)模型
    theta1_ARMA=fr.model_arma(p,q,fai_mao)
    z=data_diff[:]
    len_z=data_len-1
    alpha=[0]
    mea=mean_data
    # 计算theta0初始值
    fai_sum=0
    for i in range(1,p+1):
        fai_sum=fai_sum+fai_mao[i]
    theta0_ARMApre=mean_data*(1-fai_sum)
    # 计算alpha_k
    for k in range(1,data_len):
        sum_fai=0
        for pp in range(1,p+1):
            if k-pp-1<0:               
                sum_fai=sum_fai+fai_mao[pp]*mea
            else:
                sum_fai=sum_fai+fai_mao[pp]*z[k-pp-1]
        alpha_tt=-theta0_ARMApre+z[k-1]-sum_fai+theta1_ARMA*alpha[k-1]
        alpha.extend([alpha_tt])
    sum_k1=0
    for pp in range(1,p+1):
        sum_k1=sum_k1+fai_mao[pp]*z[len_z+1-pp]
    z_k1=theta0_ARMApre+sum_k1-theta1_ARMA*alpha[-1]
    z.extend([z_k1])
    for LL in range(2,2):
        sum_pp=0
        for pp in range(1,pp+1):
            sum_pp=sum_pp+fai_mao[pp]*z[len_z+LL-pp]
        z.extend([theta0_ARMApre+sum_pp])
    # 逆差分处理(差分数据,原数据的前n阶个,差分阶数)
    ARMA_pre_inv=fr.difference_inv(z,data[0:fr.diff_n],fr.diff_n)
    return ARMA_pre_inv[data_len+1:],ARMA_pre_inv

# MA(1)模型预测预测未来和(data,q,k)
def ma_pre(data,q,k):
    # 得到MA(1)模型
    theta_1,sigma2_ma=fr.model_ma(rou,1)
    z=data_diff[:]
    tt=data_diff[0]-mean_data
    alpha=[0,tt]
    for t in range(2,fr.data_len):
        mm=data_diff[t-1]-mean_data+theta_1*alpha[t-1]
        alpha.extend([mm])
    z.extend([mean_data-theta_1*alpha[-1]])
    z.extend([mean_data])
    # 逆差分处理(差分数据,原数据的前n阶个,差分阶数)
    MA_pre_inv=fr.difference_inv(z,data[0:fr.diff_n],fr.diff_n)
    return MA_pre_inv[data_len+1:],MA_pre_inv

#预测接口 (data,model,p,q=1,k=39)
def interface_pre(data,model,p,q=1,k=20):
    global data_diff,data_len,gamma,mean_data,data_w,rou,fai_ex,fai,AR_pre_inv
    data_diff,data_len,gamma,mean_data,data_w,rou,fai_ex,fai=fr.func(data,k)
    if model==1:
        AR_pre,AR_pre_inv=ar_pre(data,p,k)
        return AR_pre,AR_pre_inv
    elif model==2:
        MA_pre,MA_pre_inv=ma_pre(data,q,k)
        return MA_pre,MA_pre_inv
    else:
        ARMA_pre,ARMA_pre_inv=arma_pre(data,p,q,k)
        return ARMA_pre,ARMA_pre_inv 
