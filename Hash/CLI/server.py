import pandas as pd
import hashlib
import socket

HOST = '127.0.0.1'
PORT = 12345

file = pd.read_csv('C:/Python3/IOTFlowData/Resources/t.csv')

hash_list = []

for row in range(0, 100):
	row_info = str(file.saddr[row]) + str(file.sport[row]) + str(file.daddr[row]) + str(file.dport[row])
	row_info_hash = str(hashlib.sha256((row_info).encode('utf-8')).hexdigest())
	hash_list.append(row_info_hash)

print('Waiting for client...')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((HOST, PORT))
	s.listen()
	while True:
		conn, addr = s.accept()
		with conn:
			print("Connected with: ", addr)
			msg = conn.recv(1024)
			msg = msg.decode()
			row = int(input('Enter the row number: '))
			row_info_hash = hash_list[row] + "sha256" + str(row) + str(len(str(row)))
			print('Generated message:', row_info_hash)
			print('Received message:', msg)
			if(msg == row_info_hash):
				conn.send(b'Authenticated')
				print('Authenticated')
			else:
				conn.send(b'Not authenticated')
				print('Not authenticated')
				break