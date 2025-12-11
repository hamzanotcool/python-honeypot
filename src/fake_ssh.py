import socket
import threading
import os
from logger import log_event

PORT = 2222

# Faux système de fichiers virtuel
FAKE_FILES = {
    "documents": ["report.pdf", "notes.txt"],
    "secret": ["key.pem", "credentials.txt"],
    "passwords.txt": ["admin:123456", "root:toor"]
}


def handle_client(conn, addr):
    ip = addr[0]

    conn.send(b"FakeSSH v1.0\r\n")
    conn.send(b"login: ")
    username = conn.recv(1024).decode(errors="ignore").strip()

    conn.send(b"password: ")
    password = conn.recv(1024).decode(errors="ignore").strip()

    log_event({
        "event": "SSH_LOGIN",
        "ip": ip,
        "username": username,
        "password": password
    })

    conn.send(b"Welcome to FakeShell!\r\n")
    conn.send(b"fake@honeypot:~$ ")

    while True:
        data = conn.recv(1024)
        if not data:
            break
        cmd = data.decode(errors="ignore").strip()

        log_event({
            "event": "SSH_COMMAND",
            "ip": ip,
            "command": cmd
        })

        if cmd == "ls":
            conn.send(b"documents  secret  passwords.txt\r\n")

        elif cmd.startswith("cat "):
            filename = cmd.split(" ", 1)[1]
            content = FAKE_FILES.get(filename)
            if content:
                conn.send(("\r\n".join(content) + "\r\n").encode())
            else:
                conn.send(b"File not found\r\n")

        elif cmd in ("exit", "quit"):
            conn.send(b"Goodbye!\r\n")
            break

        else:
            conn.send(b"Command not found\r\n")

        conn.send(b"fake@honeypot:~$ ")

    conn.close()


def run_fake_ssh():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("", PORT))
    server.listen(5)

    print(f"[+] Faux SSH actif sur le port {PORT}")
    try:
        while True:
            conn, addr = server.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\n[+] Faux SSH arrêté.")
    finally:
        server.close()


if __name__ == "__main__":
    run_fake_ssh()
