import socket
import select
import sys
import time
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP_address = "127.0.0.1"
port = 12345

server.connect((IP_address, port))
print("Connected To server")

user_id = input("Type user id: ")
room_id = input("Type room id: ")

server.send(str.encode(user_id))
time.sleep(0.1)
server.send(str.encode(room_id))

while True:
    socket_list = [sys.stdin, server]


    read_socket, write_socket, error_socket = select.select(socket_list, [], [])

    for socks in read_socket:
        if socks == server:
            message = socks.recv(1024)
            
            print(str(message.decode()))

            if str(message.decode()) == "FILE":
                file_name = socks.recv(1024).decode()
                lenOfFile = socks.recv(1024).decode()
                send_user = socks.recv(1024).decode()

                if os.path.exists(file_name):
                    os.remove(file_name)

                print(file_name, lenOfFile, send_user)

                total = 0
                with open(file_name, 'wb') as file:
                    while str(total) != lenOfFile:
                        data = socks.recv(1024)
                        total = total + len(data)     
                        file.write(data)
                print("<" + str(send_user) + "> " + file_name + " sent")
                       
            else:
                print(message.decode())

        else:
            message = sys.stdin.readline()

            if str(message) == "FILE\n":
                file_name = input("Enter the file name : ")
                server.send("FILE".encode())
                time.sleep(0.1)
                server.send(str("client_" + file_name).encode())
                time.sleep(0.1)
                server.send(str(os.path.getsize(file_name)).encode())
                time.sleep(0.1)

                file = open(file_name, "rb")
                data = file.read(1024)
                while data:
                    server.send(data)
                    data = file.read(1024)
                sys.stdout.write("<You>")
                sys.stdout.write("File sent successfully\n")
                sys.stdout.flush()

            else:
                server.send(message.encode())
                sys.stdout.write("<You>")
                sys.stdout.write(message)
                sys.stdout.flush()
server.close()

