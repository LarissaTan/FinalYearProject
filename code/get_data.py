from web3 import Web3
import math
import hashlib
from store_data import *
from store_data_pulse import *
from arima import *
from datetime import datetime
#from hl7apy.core import Message

from cryptography.fernet import Fernet

key = b'SfMxJjQQBBZ1DrJZ0xZwiM0K1jvFAWB1c8pQL7W9mQs='
cipher_suite = Fernet(key)

account_address  = '0x46C3d6d846Ada43774999Fc066211BC961b19F70'
private_key = '0f52b49df6f1d8c737dad58969e6b66bc1ee53f8e2f314b19eb7a4cddd9e9000'

web3 = Web3(Web3.HTTPProvider('https://goerli.infura.io/v3/8600c337513c4cbc8e8d3d9f1f577598'))

conadress = "0x408449Ae12bF1f3154b422f56f9BEBB04B6B1b9d"
conabi = [
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "newMessage",
                "type": "string"
            }
        ],
        "name": "addMessage",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getAllMessages",
        "outputs": [
            {
                "internalType": "string[]",
                "name": "",
                "type": "string[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getLastMessage",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "index",
                "type": "uint256"
            }
        ],
        "name": "getMessage",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "index",
                "type": "uint256"
            },
            {
                "internalType": "string",
                "name": "newMessage",
                "type": "string"
            }
        ],
        "name": "setMessage",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

contra = web3.eth.contract(address=conadress, abi=conabi)

result = contra.functions.getLastMessage().call()

#print(result)

print(result)

# 解析字符串中的数据
data_start_index = result.find("['")
data_end_index = result.find("']")

if data_start_index != -1 and data_end_index != -1:
    data_string = result[data_start_index + 2: data_end_index]
    data_list = data_string.split("', '")
    
    # 输出每个元素
    for element in data_list:
        parts = element.split(', ')
        print(len(parts))
        time = parts[0][0:-1]
        
        print(parts)


        value1 = float(parts[1])
        value2 = int(parts[2])
        value3 = parts[3][1:]
        #value4 = parts[4]
        print("Time:", time)
        print("Value1:", value1)
        print("Value2:", value2)
        print("Value3:", value3)
        print(element)

        #开始走ISF
        #这里开始做forecast
        data_ecg_pre_set = read_data()
        data_ecg_pre_set = [float(x[1]) for x in data_ecg_pre_set]

        forecast_data_set = perform_arma_prediction(data_ecg_pre_set)
        forecast_data_set = [round(y,3) for y in forecast_data_set]

		# 计算均值
        data_combined_ecg = forecast_data_set + data_ecg_pre_set
        mean_ecg = round(sum(data_combined_ecg) / len(data_combined_ecg), 3)
        print(f"The combined average value is: {mean_ecg}")

        raw_ecg = round((value1 + mean_ecg),3) - float(5.0)
        print(f"The raw value is: {raw_ecg}")
        

        data_for_hash = time + str(raw_ecg) + str(value2)
        hash_vaule = hashlib.sha256(data_for_hash.encode()).hexdigest()

        print(data_for_hash)

        print(hash_vaule)
        print(value3)

        if(hash_vaule == value3):
            print("The hash value is correct")
        else:
            print("The hash value is not correct")
        

        time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        tmps = read_data()
        tmp_time = tmps[-1][0]
        tmp_time = datetime.strptime(tmp_time, "%Y-%m-%d %H:%M:%S")

        #忽略前面的数据，只输出和存的最新数据一样的数据
        '''
        if time == tmp_time:
            
            print(time)
            ecg = element[22:27]
            print(ecg)
            tmp = element[29]
            if (tmp == '-'):
                pulse = 'null'
            else:
                pulse = element[29:32]
            print(pulse)
        '''
            
        #比存的更新的数据

		
        if time > tmp_time:
            data_ecg_pre_set = read_data()
            data_ecg_pre_set = [float(x[1]) for x in data_ecg_pre_set]
            
            forecast_data_set = perform_arma_prediction(data_ecg_pre_set)
            forecast_data_set = [round(y,3) for y in forecast_data_set]
            data_combined_ecg = forecast_data_set + data_ecg_pre_set
            mean_ecg = round(sum(data_combined_ecg) / len(data_combined_ecg), 3)
            print(f"The combined average value is: {mean_ecg}")
            ecg_value = value1 + mean_ecg 


            tmp_write_data = element[0:19] + ";" + str(ecg_value)
            write_data(tmp_write_data)
            print("i dont why here is working")
            print(time, "----",tmp_time)
            tmp = element[29]
            if (value2 <= 0):
                pulse = 'null'
            else:
                print(value2)


#python3 -u "/Users/tanqianqian/Desktop/FinalYearProject/code/get_data.py"
