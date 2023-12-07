from web3 import Web3

from hl7apy.core import Message

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

print(result)

print(cipher_suite.decrypt(bytes(result, 'utf-8')).split(b'|')[-1].decode('utf-8'))
