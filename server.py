import socket
import threading
import sys
from collections import defaultdict

subscribers = defaultdict(list)  # Dictionary to hold topic-wise subscribers

def handle_client(client_socket, role, topic):
    global subscribers
    while True:
        try:
            message = client_socket.recv(1024).decode().strip()
            if not message:
                break
            print(f"Received from {role} on {topic}: {message}")
            if role == "PUBLISHER" and message.lower() != "terminate":
                broadcast(message, topic, client_socket)
            if message.lower() == "terminate":
                break
        except ConnectionResetError:
            break

    if role == "SUBSCRIBER":
        subscribers[topic].remove(client_socket)
    client_socket.close()
    print(f"Connection closed with {role} on {topic}")

def broadcast(message, topic, exclude_socket):
    for subscriber in subscribers[topic]:
        if subscriber != exclude_socket:
            try:
                subscriber.sendall(f"Received on {topic}: {message}\n".encode())
            except:
                subscribers[topic].remove(subscriber)

def main():
    if len(sys.argv) != 2:
        print("Usage: python server.py <PORT>")
        sys.exit(1)

    port = int(sys.argv[1])
    server_ip = socket.gethostbyname(socket.gethostname())

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((server_ip, port))
        server_socket.listen(5)
        print(f"Server listening on {server_ip}:{port}")

        while True:
            client_socket, client_address = server_socket.accept()
            client_data = client_socket.recv(1024).decode().strip().split()
            role = client_data[0].upper()
            topic = client_data[1].upper()
            if role == "SUBSCRIBER":
                subscribers[topic].append(client_socket)
            print(f"Connected by {client_address} as {role} on {topic}")

            client_thread = threading.Thread(target=handle_client, args=(client_socket, role, topic))
            client_thread.start()

if __name__ == "__main__":
    main()
