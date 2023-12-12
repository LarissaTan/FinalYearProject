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
		msglst.append(amplitude_ecg)


		if(bpm-125) > 0:
            #GPIO.output(12, GPIO.HIGH)
			pulse_output = "P:" + str(bpm - 125)
			print("HIGH, " + str(bpm - 125))
			msglst.append((bpm - 125))

			print(f"data lenth {len(msglst)}")
                
		else:
			print("no heart beat")
			pulse_output = "No"
			msglst.append(-1)

		msglst.append(hash(formatted_datetime + str(amplitude_ecg) + str(bpm - 125)))
        
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
		print("txn_hash.hex()")

        #now = time.strftime('%m/%d %H:%M:%S', time.localtime(time.time()))
        #LCD.print_lcd(1, 1, 'Hello, world!')
		LCD.print_lcd(1, 1, ecg_output + "|" + pulse_output)
		time.sleep(1)
