import socket
import sys
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(message.strip())
        except ConnectionResetError:
            break

def main():
    if len(sys.argv) != 5:
        print("Usage: python client.py <SERVER_IP> <SERVER_PORT> <PUBLISHER/SUBSCRIBER> <TOPIC>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    role = sys.argv[3].upper()
    topic = sys.argv[4].upper()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_ip, server_port))
        client_socket.sendall(f"{role} {topic}\n".encode())

        if role == "SUBSCRIBER":
            receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
            receive_thread.start()

        while True:
            if role == "PUBLISHER":
                message = input()
                client_socket.sendall(f"{message}\n".encode())
                if message.lower() == "terminate":
                    break

if __name__ == "__main__":
    main()
