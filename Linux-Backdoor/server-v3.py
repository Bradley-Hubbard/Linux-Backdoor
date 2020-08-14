#!/bin/python3

import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5003

BUFFER_SIZE = 1024*4

s = socket.socket()

s.bind((SERVER_HOST, SERVER_PORT))

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.listen(5)
print(f"Listening as {SERVER_HOST}:{SERVER_PORT} ...")


client_socket, client_address = s.accept()
print(f"{client_address[0]}:{client_address[1]} Connected!")

while True:

    command = input("Enter the command you wanna execute: ")

    client_socket.send(command.encode())
    if command.lower() == "exit":

        break

    results = client_socket.recv(BUFFER_SIZE).decode()

    print(results)
    print("\n")

client_socket.close()
s.close()
