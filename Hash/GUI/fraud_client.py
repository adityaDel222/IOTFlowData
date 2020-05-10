import pandas as pd
import hashlib
import socket
from tkinter import *
import random
import sys
sys.path.append('../../Resources')
import file_path

HOST = '127.0.0.1'
PORT = 12345

file = pd.read_csv(file_path.FILE_PATH)

BG = "antiquewhite1"

def sysExit():
	sys.exit("Client terminated.")

def verifyClient():
	row = int(row_num.get())
	row_info = str(file.saddr[row]) + str(file.sport[row]) + str(file.daddr[row]) + str(file.dport[row]) + str(random.randint(100,999))
	msg = str(hashlib.sha512((row_info).encode('utf-8')).hexdigest()) + "sha512" + str(row) + str(len(str(row)))
	
	top = Toplevel()
	top.title('IOT Flow Data with Hash - (Fraud) Client')
	top.attributes('-topmost', 1)
	top.attributes('-topmost', 0)
	w, h = top.winfo_screenwidth(), top.winfo_screenheight()
	w1, h1 = w / 2 - 100, h - 550
	sw, sh = w / 2 + 50, 230
	top.geometry("%dx%d+%d+%d" % (w1, h1, sw, sh))
	top.resizable(0, 0)
	top.configure(bg = BG)

	Label(top, text = 'Generated Hash:', font = ("Arial Bold", 12), bg = BG).place(x = 0, y = 20, width = w1, height = 20)
	Label(top, text = msg, font = ("Courier", 8), bg = BG, wraplength = 480).place(x = 0, y = 50, width = w1, height = 30)
	s.send(msg.encode())
	reply = s.recv(1024)
	replytxt = str(reply)[2:-1]
	if(replytxt[0] == 'A'):
		lblfg = "green"
	else:
		lblfg = "red"
	Label(top, text = str(reply)[2:-1], font = ("Arial", 14), bg = BG, fg = lblfg).place(x = 0, y = 100, width = w1, height = 30)
	Button(top, text = 'Close', command = top.destroy, bg = BG, fg = "red", font = ("Segoe UI Light", 12)).place(x = w1 / 2 - 50, y = 150, width = 100, height = 30)

	top.mainloop()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	host = socket.gethostname()
	hn = str(socket.gethostbyname(host))
	hostname = []
	c = 0
	while hn[c] != '.':
		hostname.append(hn[c])
		c += 1
	hostname += ['.xxx.xxx.']
	hostname += hn[-3:]
	hostname = ''.join(hostname)

	root = Tk()
	root.title('IOT Flow Data with Hash - (Fraud) Client')
	root.attributes('-topmost', 1)
	root.attributes('-topmost', 0)
	w, h = root.winfo_screenwidth(), root.winfo_screenheight()
	w1, h1 = w / 2 - 10, h - 250
	sw, sh = w / 2, 100
	root.geometry("%dx%d+%d+%d" % (w1, h1, sw, sh))
	root.resizable(0, 0)
	root.configure(bg = BG)

	Label(root, text = "Authentication of IoT Flow Records", font = ("Verdana Bold", 24), bg = "white", fg = "gray25").place(x = 0, y = 0, width = w1, height = 90)
	Label(root, text = "Secured with Hash", font = ("Courier", 12), bg = "white", fg = "gray25").place(x = 0, y = 60, width = w1, height = 40)
	Label(root, text = "Welcome user!", font = ("Arial Bold", 12), bg = BG).place(x = 120, y = 120, width = 120, height = 20)

	Label(root, text = "Client Details", font = ("Arial Bold", 12), bg = BG).place(x = 0, y = 150, width = w1, height = 20)
	Label(root, text = "Host Name", font = ("Arial", 12), justify = "right", bg = BG).place(x = w1 / 2 - 110, y = 180, width = 90, height = 20)
	Label(root, text = ":", font = ("Arial", 12), justify = "center", bg = BG).place(x = w1 / 2, y = 180, width = 10, height = 20)
	Label(root, text = host, font = ("Courier", 12), justify = "left", bg = BG).place(x = w1 / 2 + 30, y = 180, width = 70, height = 20)
	Label(root, text = "Host IP Address", font = ("Arial", 12), justify = "right", bg = BG).place(x = w1 / 2 - 145, y = 205, width = 125, height = 20)
	Label(root, text = ":", font = ("Arial", 12), justify = "center", bg = BG).place(x = w1 / 2, y = 205, width = 10, height = 20)
	Label(root, text = hostname, font = ("Courier", 12), justify = "left", bg = BG).place(x = w1 / 2 + 30, y = 205, width = 160, height = 20)
	Label(root, text = "Port Number", font = ("Arial", 12), justify = "right", bg = BG).place(x = w1 / 2 - 120, y = 230, width = 100, height = 20)
	Label(root, text = ":", font = ("Arial", 12), justify = "center", bg = BG).place(x = w1 / 2, y = 230, width = 10, height = 20)
	Label(root, text = PORT, font = ("Courier", 12), justify = "left", bg = BG).place(x = w1 / 2 + 30, y = 230, width = 60, height = 20)

	Label(root, text = "File Read", font = ("Arial", 12), justify = "right", bg = BG).place(x = w1 / 2 - 100, y = 260, width = 80, height = 20)
	Label(root, text = ":", font = ("Arial", 12), justify = "center", bg = BG).place(x = w1 / 2, y = 260, width = 10, height = 20)
	Label(root, text = file_path.FILE_PATH[-28:], font = ("Courier", 10), justify = "left", bg = BG).place(x = w1 / 2 + 20, y = 260, width = 250, height = 20)

	Label(root, text = 'Connected to server', font = ("Arial Bold", 12), bg = BG).place(x = w1 / 2 - 75, y = 300, width = 160, height = 20)
	Label(root, text = "Select row number", font = ("Arial", 12), bg = BG).place(x = w1 / 2 - 160, y = 340, width = 145, height = 20)
	Label(root, text = ":", font = ("Arial", 12), justify = "center", bg = BG).place(x = w1 / 2, y = 340, width = 10, height = 20)
	row_num = Spinbox(root, from_ = 0, to = len(file) - 1, font = ("Arial", 12), justify = "center")
	row_num.place(x = w1 / 2 + 30, y = 335, width = 50, height = 30)	# Seperate grid() to be able to collect value in variable
	btn = Button(root, text = 'VERIFY', command = verifyClient, bg = "gray25", fg = "white", font = ("Segoe UI Light", 15))
	btn.place(x = w1 / 2 - 50, y = 380, width = 100, height = 40)
	btn = Button(root, text = 'Terminate Client', command = sysExit, bg = BG, fg = "red", font = ("Segoe UI Light", 12))
	btn.place(x = w1 / 2 - 100, y = 440, width = 200, height = 30)

	root.mainloop()