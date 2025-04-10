this is a basic encrypted chatroom using Python sockets and Fernet encryption. every client that connects gets their own thread, and all messages are encrypted with AES using the cryptography library.

users can log in or register with a username and password. everything runs in the terminal. once you're in, anything you type is broadcast to the rest of the chatroom.

no chat logs are saved, and all messages are encrypted in transit. server handles the relaying, not the storage.

run `generate_key.py` first to make the encryption key. then run `server.py`, and open multiple terminals to run `client.py` for each user. you can modify server and client files to route it to a specific address for the server. it is set to localhost and port 12345 by default.

written for a programming class project, mostly just to show off socket programming, threading, and encryption.
