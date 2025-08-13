import socket
import sys
import threading
import time

SERVER_IP = "157.230.165.36"
PORT = 5000
username = "Luiz"
text = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit,"
    "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
    "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris"
    "nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in"
    "reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla"
    "pariatur. Excepteur sint occaecat cupidatat non proident, sunt in"
    "culpa qui officia deserunt mollit anim id est laborum."
)

NUM_THREADS = 15  # Number of parallel client threads

def client_task():
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((SERVER_IP, PORT))
            except ConnectionRefusedError:
                print("Connection refused. Is the server running and reachable?")
                sys.exit(1)

            message = f"{username};{text}".encode("utf-8")

            start_time = time.time()
            s.sendall(message)

            data = s.recv(1000000)
            end_time = time.time()

            elapsed_ms = (end_time - start_time) * 1000  # convert to milliseconds

            print(f"[{threading.current_thread().name}] Response time: {elapsed_ms:.2f} ms")


# Create and start threads
threads = []
for i in range(NUM_THREADS):
    t = threading.Thread(target=client_task, name=f"Client-{i+1}", daemon=True)
    threads.append(t)
    t.start()

# Keep main thread alive
for t in threads:
    t.join()
