import pandas as pd
import socket
import hashlib
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import ast
from tkinter import *
from functools import partial
import sys
sys.path.append('../../Resources')
import file_path

HOST = '127.0.0.1'
PORT = 12345

file = pd.read_csv(file_path.FILE_PATH)

BG = "lavender"
BG_top = "powder blue"

def sysExit():
	sys.exit("Server terminated.")

def verifyClient(client_msg):
	row = int(row_num.get())
	row_info = str(file.saddr[row]) + str(file.sport[row]) + str(file.daddr[row]) + str(file.dport[row])

	random_generator = Random.new().read
	key = RSA.generate(1024, random_generator)
	public_key = key.publickey()

	plaintext = row_info + "sha256"

	ciphertext = []
	for p in plaintext:
		c = str(public_key.encrypt(ord(p), 32))[1:-2]
		ciphertext.append(c)
	ciphertext = ''.join(ciphertext)
	ciphertext_length = len(ciphertext)

	server_hash = hashlib.sha256((plaintext).encode('utf-8')).hexdigest()

	client_hash = client_msg[-72:-8]

	server_msg = str(ciphertext) + str(server_hash) + "sha256" + str(row) + str(len(str(row)))
	server_msg_length = len(server_msg)

	top = Tk()
	top.title('IOT Flow Data with Hash - Server') 
	top.attributes('-topmost', 1)
	top.attributes('-topmost', 0)
	w, h = top.winfo_screenwidth(), top.winfo_screenheight()
	w1, h1 = w / 2 - 20, h - 300
	sw, sh = 5, 125
	top.geometry("%dx%d+%d+%d" % (w1, h1, sw, sh))
	top.resizable(0, 0)
	top.configure(bg = BG)

	Label(top, text = 'Plaintext:', font = ('Arial Bold', 10), bg = BG_top).place(x = 0, y = 40, width = w1, height = 20)
	Label(top, text = plaintext, font = ('Courier', 8), bg = BG).place(x = 0, y = 70, width = w1, height = 15)
	Label(top, text = 'Ciphertext:', font = ('Arial Bold', 10), bg = BG_top).place(x = 0, y = 95, width = w1, height = 20)
	Label(top, text = ciphertext[:78] + ciphertext[-50:], wraplength = 450, font = ('Courier', 8), bg = BG).place(x = 0, y = 125, width = w1, height = 30)
	Label(top, text = 'Generated Hash:', font = ('Arial Bold', 10), bg = BG_top).place(x = 0, y = 165, width = w1, height = 20)
	Label(top, text = server_hash, font = ('Courier', 8), bg = BG).place(x = 0, y = 195, width = w1, height = 15)
	Label(top, text = 'Received Hash:', font = ('Arial Bold', 10), bg = BG_top).place(x = 0, y = 220, width = w1, height = 20)
	Label(top, text = client_hash, font = ('Courier', 8), bg = BG).place(x = 0, y = 250, width = w1, height = 15)

	if(server_hash == client_hash):
		conn.send(b'Authenticated')
		lbltxt = 'Authenticated'
		lblfg = 'green'
	else:
		conn.send(b'Not authenticated')
		lbltxt = 'Not Authenticated'
		lblfg = 'red'

	Label(top, text = lbltxt, font = ('Segoe UI', 15), fg = lblfg, bg = BG).place(x = 0, y = 350, width = w1, height = 30)
	Button(top, text = 'Close', command = top.destroy, bg = BG, fg = "red", font = ("Segoe UI Light", 12)).place(x = w1 / 2 - 100, y = 400, width = 200, height = 30)

	top.mainloop()

print('Waiting for client...')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((HOST, PORT))
	s.listen()
	while True:
		conn, addr = s.accept()
		with conn:
			root = Tk()
			root.title('IOT Flow Data with Hash - Server') 
			root.attributes('-topmost', 1)
			root.attributes('-topmost', 0)
			w, h = root.winfo_screenwidth(), root.winfo_screenheight()
			w1, h1 = w / 2 - 10, h - 250
			sw, sh = 0, 100
			root.geometry("%dx%d+%d+%d" % (w1, h1, sw, sh))
			root.resizable(0, 0)
			root.configure(bg = BG)

			Label(root, text = "Authentication of IoT Flow Records", font = ("Verdana Bold", 24), bg = "white", fg = "gray25").place(x = 0, y = 0, width = w1, height = 90)
			Label(root, text = "Secured with RSA and Hash", font = ("Courier", 12), bg = "white", fg = "gray25").place(x = 0, y = 60, width = w1, height = 40)
			Label(root, text = "Welcome host!", font = ("Arial Bold", 12), bg = BG).place(x = 120, y = 120, width = 120, height = 20)

			Label(root, text = "Connected to client", font = ("Arial Bold", 12), bg = BG).place(x = 0, y = 150, width = w1, height = 20)
			Label(root, text = "Client IP Address", font = ("Arial", 12), justify = "right", bg = BG).place(x = w1 / 2 - 145, y = 205, width = 125, height = 20)
			Label(root, text = ":", font = ("Arial", 12), justify = "center", bg = BG).place(x = w1 / 2, y = 205, width = 10, height = 20)
			Label(root, text = str(addr[0]), font = ("Courier", 12), justify = "left", bg = BG).place(x = w1 / 2 + 25, y = 205, width = 100, height = 20)
			Label(root, text = "Port Number", font = ("Arial", 12), justify = "right", bg = BG).place(x = w1 / 2 - 120, y = 230, width = 100, height = 20)
			Label(root, text = ":", font = ("Arial", 12), justify = "center", bg = BG).place(x = w1 / 2, y = 230, width = 10, height = 20)
			Label(root, text = str(addr[1]), font = ("Courier", 12), justify = "left", bg = BG).place(x = w1 / 2 + 25, y = 230, width = 60, height = 20)

			Label(root, text = "File Read", font = ("Arial", 12), justify = "right", bg = BG).place(x = w1 / 2 - 100, y = 260, width = 80, height = 20)
			Label(root, text = ":", font = ("Arial", 12), justify = "center", bg = BG).place(x = w1 / 2, y = 260, width = 10, height = 20)
			Label(root, text = file_path.FILE_PATH, font = ("Courier", 10), justify = "left", bg = BG).place(x = w1 / 2 + 30, y = 260, width = 205, height = 20)

			client_msg = conn.recv(12750)
			client_msg = client_msg.decode()

			Label(root, text = "Select row number", font = ("Arial", 12), bg = BG).place(x = w1 / 2 - 160, y = 320, width = 145, height = 20)
			Label(root, text = ":", font = ("Arial", 12), justify = "center", bg = BG).place(x = w1 / 2, y = 320, width = 10, height = 20)
			row_num = Spinbox(root, from_ = 0, to = len(file) - 1, font = ("Arial", 12), justify = "center")
			row_num.place(x = w1 / 2 + 30, y = 315, width = 50, height = 30)	# Seperate grid() to be able to collect value in variable
			btn = Button(root, text = 'VERIFY', command = partial(verifyClient, client_msg), bg = "gray25", fg = "white", font = ("Segoe UI Light", 15))
			btn.place(x = w1 / 2 - 50, y = 380, width = 100, height = 40)
			btn = Button(root, text = 'Terminate Server', command = sysExit, bg = BG, fg = "red", font = ("Segoe UI Light", 12))
			btn.place(x = w1 / 2 - 100, y = 440, width = 200, height = 30)

			root.mainloop()