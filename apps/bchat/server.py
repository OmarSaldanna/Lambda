import socket
import threading

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
clients = []
names = []

# print(f'bchat started on {host}:{port}')

def handle_client(client_socket, client_address):
    """Handle a single client connection."""
    #print('New client connected:', client_address)

    # Add the client socket to the list
    clients.append(client_socket)

    while True:
        # Receive a message from the client
        message = client_socket.recv(1024).decode()
        if not message:
            break

        # Print the message and broadcast it to all clients
        #print('Received message from {}: {}'.format(client_address, message))
        # if a new member joins to chat
        if message[0] == '~':
            name = message[1:]
            if name not in names:
                names.append(name)
            # and broadcast
            message = f"\n-> [{name}] se unió\n-> Activos: {names}\n"

        for c in clients:
            if c != client_socket:
                c.send(message.encode())

    # Remove the client socket from the list
    clients.remove(client_socket)
    client_socket.close()
    #print('Client disconnected:', client_address)

while True:
    # Accept incoming connections
    client_socket, client_address = server_socket.accept()

    # Start a new thread to handle the client connection
    thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    thread.start()

