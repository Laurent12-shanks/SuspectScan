# tests/fichier_suspect.py
import os
import socket
import base64

cmd = base64.b64decode("aGVsbG8gd29ybGQ=")
exec(cmd)
os.system("whoami")

eval(5+6)
print(eval("salut"))

s = socket.socket()
s.connect(("192.168.1.1", 4444))