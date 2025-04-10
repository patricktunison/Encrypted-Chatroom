from cryptography.fernet import Fernet
import hashlib

def load_key():
    with open("key.key", "rb") as f:
        return Fernet(f.read())

def encrypt_message(msg, fernet):
    return fernet.encrypt(msg.encode())

def decrypt_message(token, fernet):
    return fernet.decrypt(token).decode()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    try:
        with open("users.txt", "r") as f:
            for line in f:
                user, pwd = line.strip().split(":")
                if user == username and pwd == hash_password(password):
                    return True
    except FileNotFoundError:
        pass
    return False

def register_user(username, password):
    with open("users.txt", "a") as f:
        f.write(f"{username}:{hash_password(password)}\n")
