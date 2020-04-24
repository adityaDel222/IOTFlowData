import pandas as pd
import hashlib
import socket
import base64
from Crypto.Cipher import AES
from Crypto import Random

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

	BLOCK_SIZE = 16
	pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
	unpad = lambda s: s[:-ord(s[len(s) - 1:])]

	password = str(1111) #Random password

	plaintext = row_info + "sha256"
	print()
	print("Plaintext:", plaintext)
	ciphertext = encrypt(plaintext, password)
	print("Ciphertext:", str(ciphertext)[2:-1])
	ciphertext_hash = hashlib.sha256((plaintext).encode('utf-8')).hexdigest()
	print("Hash:", ciphertext_hash)
	msg = str(ciphertext)[2:len(ciphertext)+2] + str(ciphertext_hash) + "sha256" + str(row) + str(len(str(row)))

	print()
	print('Generated message:', msg)
	print()

	s.send(msg.encode())
	reply = s.recv(1024)
	print(str(reply)[2:-1])