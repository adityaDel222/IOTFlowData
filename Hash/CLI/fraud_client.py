import pandas as pd
import hashlib
import socket
import random

HOST = '127.0.0.1'
PORT = 12345

file = pd.read_csv('C:/Python3/IOTFlowData/Resources/t.csv')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	print('Connected to server.')
	row = int(input('Enter the row number: '))
	row_info = str(file.saddr[row]) + str(file.sport[row]) + str(file.daddr[row]) + str(file.dport[row]) + str(random.randint(100,999))
	msg = str(hashlib.sha256((row_info).encode('utf-8')).hexdigest()) + "sha256" + str(row) + str(len(str(row)))
	print('Generated message:', msg)
	s.send(msg.encode())
	reply = s.recv(1024)
	print(str(reply)[2:-1])