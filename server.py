import socket
import threading
from utils import *

fernet = load_key()
clients = []  # Stores (conn, username)

def broadcast(sender_conn, message):
    for conn, _ in clients:
        if conn != sender_conn:
            try:
                conn.send(encrypt_message(message, fernet))
            except:
                conn.close()

def handle_client(conn, addr):
    try:
        # Authentication
        conn.send(b"Username: ")
        username = conn.recv(1024).decode().strip()
        conn.send(b"Password: ")
        password = conn.recv(1024).decode().strip()

        if authenticate_user(username, password):
            conn.send(b"Login successful.\n")
        else:
            register_user(username, password)
            conn.send(b"New user registered.\n")

        # Add to active clients list
        clients.append((conn, username))
        print(f"[+] {username} connected from {addr}")
        broadcast(conn, f"{username} has joined the chat.")

        # Chat loop
        while True:
            data = conn.recv(1024)
            if not data:
                break
            decrypted = decrypt_message(data, fernet)
            msg = f"[{username}]: {decrypted}"
            print(msg)
            broadcast(conn, msg)

    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        conn.close()
        clients.remove((conn, username))
        broadcast(conn, f"{username} has left the chat.")
        print(f"[-] {username} disconnected.")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 12345))
    server.listen()

    print("[*] Chatroom server running on port 12345...")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
