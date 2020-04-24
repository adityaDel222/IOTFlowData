import pandas as pd
import socket
import hashlib
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import ast

HOST = '127.0.0.1'
PORT = 12345

FILE_PATH = 'C:/Python3/IOTFlowData/Resources/t.csv'
file = pd.read_csv(FILE_PATH)

print('Waiting for client...')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((HOST, PORT))
	s.listen()
	while True:
		conn, addr = s.accept()
		with conn:
			print("Connected with: ", addr)
			client_msg = conn.recv(12750)
			client_msg = client_msg.decode()
			client_hash = client_msg[-72:-8]
			print('Received hash:', client_hash)

			row = int(input('Enter the row number: '))
			row_info = str(file.saddr[row]) + str(file.sport[row]) + str(file.daddr[row]) + str(file.dport[row])

			random_generator = Random.new().read
			key = RSA.generate(1024, random_generator)
			public_key = key.publickey()

			plaintext = row_info + "sha256"
			print("Plaintext:", plaintext)
			ciphertext = []
			for p in plaintext:
				c = str(public_key.encrypt(ord(p), 32))[1:-2]
				ciphertext.append(c)
			ciphertext = ''.join(ciphertext)
			ciphertext_length = len(ciphertext)
			print("Ciphertext length:", ciphertext_length)
			server_hash = hashlib.sha256((plaintext).encode('utf-8')).hexdigest()
			print("Hash:", server_hash)
			server_msg = str(ciphertext) + str(server_hash) + "sha256" + str(row) + str(len(str(row)))
			server_msg_length = len(server_msg)
			print('Generated message length:', server_msg_length)

			if(server_hash == client_hash):
				conn.send(b'Authenticated')
				print('Authenticated')
			else:
				conn.send(b'Not authenticated')
				print('Not authenticated')
				break