import pandas as pd
import hashlib
import socket
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import ast
import random

HOST = '127.0.0.1'
PORT = 12345

FILE_PATH = 'C:/Python3/IOTFlowData/Resources/t.csv'
file = pd.read_csv(FILE_PATH)

def encrypt(raw, password):
	private_key = hashlib.sha256(password.encode("utf-8")).digest()
	raw = pad(raw)
	iv = b"ClZ\xb6\x92\xb5\xc3\xac\x87\x03x\x80t'\xfa#"
	cipher = AES.new(private_key, AES.MODE_CBC, iv)
	return base64.b64encode(iv + cipher.encrypt(raw))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	print('Connected to server.')

	row = int(input('Enter the row number: '))
	row_info = str(file.saddr[row]) + str(file.sport[row]) + str(file.daddr[row]) + str(file.dport[row])

	random_generator = Random.new().read
	key = RSA.generate(1024, random_generator)
	public_key = key.publickey()

	plaintext = row_info + "sha256" + str(random.randint(100,999))
	print("Plaintext:", plaintext)
	ciphertext = []
	for p in plaintext:
		c = str(public_key.encrypt(ord(p), 32))[1:-2]
		ciphertext.append(c)
	ciphertext = ''.join(ciphertext)
	ciphertext_length = len(ciphertext)
	print("Ciphertext length:", ciphertext_length)
	ciphertext_hash = hashlib.sha256((plaintext).encode('utf-8')).hexdigest()
	print("Hash:", ciphertext_hash)
	msg = str(ciphertext) + str(ciphertext_hash) + "sha256" + str(row) + str(len(str(row)))
	msg_length = len(msg)
	print('Generated message length:', msg_length)

	s.send(msg.encode())
	reply = s.recv(1024)
	print(str(reply)[2:-1])