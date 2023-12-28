import socket
import requests
import threading

print("Lambda BChat Server")

# Define the host and port number to listen on
host = '0.0.0.0'
port = 31416

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific host and port
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen()

# Create a list to store the client sockets
# 'id': socket
clients = {}

# function to append on logs
def save_log(message: str, db="bchat"):
    # send the request on the logs
    requests.post("http://127.0.0.1:8081/logs", json={
        "db": db,
        "data": message
    })

# save when the bchat server was started
save_log(f'bchat started on {host}:{port}')

# function to handle cleints
def handle_client(client_socket, client_address):
    """Handle a single client connection."""
    print('New client connected:', client_address)
    save_log(f"[connected] {client_address}")

    # Add the client socket to the list
    # clients.append(client_socket)

    while True:
        # Receive a message from the client
        message = client_socket.recv(1024).decode()

        # if the message is empty
        if not message:
            # save a log to see that it happened
            save_log(f"[error] empty message from: {client_address}", db="bchat-errors")
            # and ignore it
            continue

        # if the message is to regist the user
        # message: +[id]
        if message[0] == '+':
            # select the id
            name = message[1:]
            # a little verification for lambda user
            if name == 'lambda' and client_socket.getpeername()[0] != '127.0.0.1':
                # save a log to see that it happened
                save_log(f"[attack] lambda login from: {client_address}", db="bchat-errors")
                # and ignore it
                continue

            # regist the user and its socket
            clients[name] = client_socket
            # and save on log
            save_log(f"[registered] {name}: {client_address}")


        # SECURITY BREACH: anyone connected on the server can send messages
        # to other people devices

        # if the message is for broadcast
        # message: -[from]-[to]-[content]
        if message[0] == '-':
            # extract the data
            _, sender, receiver, content = message.split('-')
            # security verification: messages from lambda came from 127.0.0.1
            if sender == 'lambda' and client_socket.getpeername()[0] != '127.0.0.1':
                # save a log to see that it happened
                save_log(f"[attack] lambda login from: {client_address}, to: {receiver}, content: {content} ", db="bchat-errors")
                # and ignore it
                continue

            # if the message was for lambda
            if receiver == 'lambda':
                # then save it in a special log, to then read it
                save_log(f"{sender}-{receiver}-{content}-", db="bchat-receipts")

            # else, it was from lambda, then deliver the message
            else:
                # try to find the socket connection
                try:
                    # select the receiver's socket
                    receiver_socket = clients[receiver]
                    # and send the whole message
                    receiver_socket.send(message.encode())
                except:
                    pass

        # 
        print(message)

    # Remove the client socket from the list
    clients.remove(client_socket)
    client_socket.close()

while True:
    # Accept incoming connections
    client_socket, client_address = server_socket.accept()

    # Start a new thread to handle the client connection
    thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    thread.start()