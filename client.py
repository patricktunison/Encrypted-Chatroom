import socket
import threading
from utils import *

fernet = load_key()
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect(('localhost', 12345))
except ConnectionRefusedError:
    print("[!] Could not connect to the server. Is it running?")
    exit()
except Exception as e:
    print(f"[!] Connection error: {e}")
    exit()


def receive_messages():
    while True:
        try:
            msg = client.recv(1024)
            if msg:
                try:
                    print("\n" + decrypt_message(msg, fernet))
                    print(f"[{username}]: ", end="", flush=True)
                except Exception as e:
                    print(f"\n[!] Failed to decrypt message: {e}")
        except:
            print("\n[!] Disconnected from server.")
            break



def send_messages():
    while True:
        msg = input(f"[{username}]: ")
        if msg.strip().lower() == 'exit':
            client.close()
            break
        if msg.strip() != "":
            client.send(encrypt_message(msg, fernet))

# Authenticate
print(client.recv(1024).decode(), end='')
username = input().strip()
client.send(username.encode())

print(client.recv(1024).decode(), end='')
password = input().strip()
client.send(password.encode())

print(client.recv(1024).decode())

# Start chat loop
threading.Thread(target=receive_messages, daemon=True).start()
send_messages()
