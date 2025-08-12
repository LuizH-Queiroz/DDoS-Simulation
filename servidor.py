import socket

HOST = "0.0.0.0"  # Listen on all network interfaces
PORT = 5000       # Port to listen on

def transform_string(s: str) -> str:

    counter = 0
    while counter < 1_000_000:
        counter += 1

    return s

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server listening on {HOST}:{PORT}")
    print("Waiting for connections...")

    while True:
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            data = conn.recv(1024).decode("utf-8").strip()
            if not data:
                continue

            try:
                username, text = data.split(";", 1)
            except ValueError:
                conn.sendall(b"ERROR: Data must be in format 'username;string'\n")
                continue

            print()
            print(f"User '{username}' sent: {text}")
            print()
            result = transform_string(text)
            conn.sendall(result.encode("utf-8"))
