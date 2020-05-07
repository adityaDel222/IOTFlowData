import pandas as pd
import hashlib
import socket
import sys
sys.path.append('../../Resources')
import file_path

HOST = '127.0.0.1'
PORT = 12345

file = pd.read_csv(file_path.FILE_PATH)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	print('Connected to server.')
	row = int(input('Enter the row number: '))
	row_info = str(file.saddr[row]) + str(file.sport[row]) + str(file.daddr[row]) + str(file.dport[row])
	msg = str(hashlib.sha512((row_info).encode('utf-8')).hexdigest()) + "sha512" + str(row) + str(len(str(row)))
	print('Generated message:', msg)
	s.send(msg.encode())
	reply = s.recv(1024)
	print(str(reply)[2:-1])