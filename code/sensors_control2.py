import time
from datetime import datetime
import LCD1602 as LCD
from pulsesensor import PulseSensor
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
from scipy import signal,stats
import pandas as pd
import hashlib
from store_data import *
from store_data_pulse import *
from arima import *

import time
import serial

import LCD1602 as LCD
import RPi.GPIO as GPIO

from web3 import Web3

from hl7apy.core import Message


key = b'SfMxJjQQBBZ1DrJZ0xZwiM0K1jvFAWB1c8pQL7W9mQs='

account_address  = '0x46C3d6d846Ada43774999Fc066211BC961b19F70'
private_key = '0f52b49df6f1d8c737dad58969e6b66bc1ee53f8e2f314b19eb7a4cddd9e9000'

web3 = Web3(Web3.HTTPProvider('https://goerli.infura.io/v3/8600c337513c4cbc8e8d3d9f1f577598'))

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)      # Ignore warning for now

#Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

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

if __name__ == '__main__':
	LCD.init_lcd()
	time.sleep(1)

	p = PulseSensor()
	p.startAsyncBPM()

    #value = mcp.read_adc(0)
    #print("value of ECG: " + str(value))
	contra = web3.eth.contract(address=conadress, abi=conabi)
	msglst = []
	while True:
		#get timestamp
		current_datetime = datetime.now()
		formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
		msglst.append(formatted_datetime)

		bpm = int(p.BPM)
		value = mcp.read_adc(0)
		voltage_ecg = (value / 1023.0) * 3.3
		amplitude_ecg = round(voltage_ecg * (3.0 / 3.3), 3)
		ecg_output = "E:" + str(amplitude_ecg)
		print("value of ECG: " + str(amplitude_ecg))
		print("value of ECG: " + str(value))

		#这里开始做forecast
		data_ecg_pre_set = read_data()
		data_ecg_pre_set = [float(x[1]) for x in data_ecg_pre_set]

		forecast_data_set = perform_arma_prediction(data_ecg_pre_set)
		forecast_data_set = [round(y,3) for y in forecast_data_set]

		# 计算均值
		data_combined_ecg = forecast_data_set + data_ecg_pre_set
		mean_ecg = round(sum(data_combined_ecg) / len(data_combined_ecg), 3)
		print(f"The combined average value is: {mean_ecg}")

		variance_ecg = amplitude_ecg - mean_ecg
		print("ecg:" + amplitude_ecg)
		print("mean:" + mean_ecg)
		print("variance_ecg:" + variance_ecg)
		msglst.append(variance_ecg)


		if(bpm-125) > 0:
            #GPIO.output(12, GPIO.HIGH)
			pulse_output = "P:" + str(bpm - 125)
			print("HIGH, " + str(bpm - 125))
			pulse_data = bpm - 125

			print(f"data lenth {len(msglst)}")
			#这里开始做forecast
			data_pulse_pre_set = read_data_pulse()
			data_pulse_pre_set = [float(x[1]) for x in data_pulse_pre_set]

			forecast_pulse_data_set = perform_arma_prediction(data_pulse_pre_set)
			forecast_pulse_data_set = [round(y,3) for y in forecast_pulse_data_set]

			# 计算均值
			data_combined_pulse = forecast_pulse_data_set + data_pulse_pre_set
			mean_pulse = sum(data_combined_pulse) / len(data_combined_pulse)
			print(f"The combined average value is: {mean_pulse}")

			variance_pulse = pulse_data - mean_pulse - 50
			msglst.append(variance_pulse)
			pulse_data = variance_pulse
                
		else:
			print("no heart beat")
			pulse_output = "No"
			pulse_data = -1
			msglst.append(pulse_data)

		LCD.print_lcd(1, 1, ecg_output + "|" + pulse_output)


		print('the vaule before hash:' + formatted_datetime + str(amplitude_ecg) + str(pulse_data))
		data_for_hash = formatted_datetime + str(amplitude_ecg) + str(pulse_data)
		msglst.append(hashlib.sha256(data_for_hash.encode()).hexdigest())
        
		msg = Message("ORU_R01")
		msg.msh.msh_9 = "ORU^R01"
		msg.add_segment("OBR")
		msg.obr.obr_4 = str(msglst)  # 假设您的时序数据作为一个字符串存储在此处
		msg_str = msg.to_er7()

		txn = contra.functions.addMessage(msg_str).build_transaction({
			'from': account_address,
            'nonce': web3.eth.get_transaction_count(account_address),
            'gas': 2000000,  # 设置足够的 Gas 上限
            'gasPrice': web3.eth.gas_price
        })
		
		signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)
		txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
		web3.eth.wait_for_transaction_receipt(txn_hash)


		print('----------------end----------------')
		time.sleep(1)
