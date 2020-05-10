import pandas as pd
import hashlib
import socket
from tkinter import *
from functools import partial
import sys
sys.path.append('../../Resources')
import file_path

HOST = '127.0.0.1'
PORT = 12345

file = pd.read_csv(file_path.FILE_PATH)

BG = "lavender"

hash_list = []

for row in range(0, 100):
	row_info = str(file.saddr[row]) + str(file.sport[row]) + str(file.daddr[row]) + str(file.dport[row])
	row_info_hash = str(hashlib.sha512((row_info).encode('utf-8')).hexdigest())
	hash_list.append(row_info_hash)

print('Waiting for client...')

def sysExit():
	sys.exit("Server terminated.")

def verifyClient(msg):
	row = int(row_num.get())
	row_info_hash = hash_list[row] + "sha512" + str(row) + str(len(str(row)))

	top = Toplevel()
	top.title('IOT Flow Data with Hash - Server')
	top.attributes('-topmost', 1)
	top.attributes('-topmost', 0)
	w, h = top.winfo_screenwidth(), top.winfo_screenheight()
	w1, h1 = w / 2 - 100, h - 550
	sw, sh = 50, 230
	top.geometry("%dx%d+%d+%d" % (w1, h1, sw, sh))
	top.resizable(0, 0)
	top.configure(bg = BG)

	Label(top, text = 'Generated Hash:', font = ("Arial Bold", 10), bg = BG).place(x = 0, y = 10, width = w1, height = 15)
	Label(top, text = row_info_hash, font = ("Courier", 8), bg = BG, wraplength = 480).place(x = 0, y = 30, width = w1, height = 30)
	Label(top, text = 'Received Hash:', font = ("Arial Bold", 10), bg = BG).place(x = 0, y = 70, width = w1, height = 15)
	Label(top, text = msg, font = ("Courier", 8), bg = BG, wraplength = 480).place(x = 0, y = 90, width = w1, height = 30)

	if(msg == row_info_hash):
		conn.send(b'Authenticated')
		lblfg = "green"
		lbltxt = "Authenticated"
	else:
		conn.send(b'Not authenticated')
		lblfg = "red"
		lbltxt = "Not Authenticated"

	Label(top, text = lbltxt, font = ("Arial", 14), bg = BG, fg = lblfg).place(x = 0, y = 125, width = w1, height = 30)
	Button(top, text = 'Close', command = top.destroy, bg = BG, fg = "red", font = ("Segoe UI Light", 12)).place(x = w1 / 2 - 50, y = 160, width = 100, height = 30)

	top.mainloop()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((HOST, PORT))
	s.listen()
	while True:
		conn, addr = s.accept()
		with conn:
			hn = str(addr[0])
			hostname = []
			c = 0
			while hn[c] != '.':
				hostname.append(hn[c])
				c += 1
			hostname += ['.xxx.xxx.']
			hostname += hn[-1:]
			hostname = ''.join(hostname)

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
			Label(root, text = "Secured with Hash", font = ("Courier", 12), bg = "white", fg = "gray25").place(x = 0, y = 60, width = w1, height = 40)
			Label(root, text = "Welcome host!", font = ("Arial Bold", 12), bg = BG).place(x = 120, y = 120, width = 120, height = 20)

			Label(root, text = "Connected to client", font = ("Arial Bold", 12), bg = BG).place(x = 0, y = 150, width = w1, height = 20)
			Label(root, text = "Client IP Address", font = ("Arial", 12), justify = "right", bg = BG).place(x = w1 / 2 - 145, y = 205, width = 125, height = 20)
			Label(root, text = ":", font = ("Arial", 12), justify = "center", bg = BG).place(x = w1 / 2, y = 205, width = 10, height = 20)
			Label(root, text = hostname, font = ("Courier", 12), justify = "left", bg = BG).place(x = w1 / 2 + 25, y = 205, width = 130, height = 20)
			Label(root, text = "Port Number", font = ("Arial", 12), justify = "right", bg = BG).place(x = w1 / 2 - 120, y = 230, width = 100, height = 20)
			Label(root, text = ":", font = ("Arial", 12), justify = "center", bg = BG).place(x = w1 / 2, y = 230, width = 10, height = 20)
			Label(root, text = str(addr[1]), font = ("Courier", 12), justify = "left", bg = BG).place(x = w1 / 2 + 25, y = 230, width = 60, height = 20)

			Label(root, text = "File Read", font = ("Arial", 12), justify = "right", bg = BG).place(x = w1 / 2 - 100, y = 260, width = 80, height = 20)
			Label(root, text = ":", font = ("Arial", 12), justify = "center", bg = BG).place(x = w1 / 2, y = 260, width = 10, height = 20)
			Label(root, text = file_path.FILE_PATH[-28:], font = ("Courier", 10), justify = "left", bg = BG).place(x = w1 / 2 + 20, y = 260, width = 250, height = 20)

			msg = conn.recv(1024)
			msg = msg.decode()

			Label(root, text = "Select row number", font = ("Arial", 12), bg = BG).place(x = w1 / 2 - 160, y = 320, width = 145, height = 20)
			Label(root, text = ":", font = ("Arial", 12), justify = "center", bg = BG).place(x = w1 / 2, y = 320, width = 10, height = 20)
			row_num = Spinbox(root, from_ = 0, to = len(file) - 1, font = ("Arial", 12), justify = "center")
			row_num.place(x = w1 / 2 + 30, y = 315, width = 50, height = 30)	# Seperate grid() to be able to collect value in variable
			btn = Button(root, text = 'VERIFY', command = partial(verifyClient, msg), bg = "gray25", fg = "white", font = ("Segoe UI Light", 15))
			btn.place(x = w1 / 2 - 50, y = 380, width = 100, height = 40)
			btn = Button(root, text = 'Terminate Server', command = sysExit, bg = BG, fg = "red", font = ("Segoe UI Light", 12))
			btn.place(x = w1 / 2 - 100, y = 440, width = 200, height = 30)

			root.mainloop()