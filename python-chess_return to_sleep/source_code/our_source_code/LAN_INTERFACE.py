import socket

import main

def start_server(port=9999):
    # create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # set IP address and port number
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    try:
        # bind the socket to a public host and a port
        sock.bind((ip_address, port))
    except OSError:
        print("Error: Failed to bind socket. Please check that the specified port is not already in use.")
        return None

    # listen for incoming connections
    sock.listen()

    print(f"Waiting for a connection... (Server Hostname: {hostname}, Port: {port})")
    print("Server IP Address is:", ip_address)

    # accept the connection
    conn, addr = sock.accept()
    print("Connected by", addr)

    return conn


def connect_to_server(host=None, port=None):
    # create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        if not host:
            # get server's IP address
            host = input("Enter server hostname: ")
        try:
            ip_address = socket.gethostbyname(host)
            break
        except socket.gaierror:
            print("Error: Hostname could not be resolved. Please try again.")
            host = None

    if not port:
        # get port number
        port = input("Enter port number (default=9999): ")
        if port is None or port == '':
            port = 9999
        else:
            try:
                port = int(port)
            except ValueError:
                print("Error: Invalid port number. Please try again.")
                return None

    # connect to the server
    try:
        sock.connect((host, port))
    except (ConnectionRefusedError, TimeoutError):
        print("Error: Connection refused or timed out. Please try again.")
        return None

    print(f"Connected to {host} on port {port}")

    return sock


def play_game():
    print("Welcome to the game!")

    mode = input("Choose your mode (server/client): ")
    if mode == "server":
        print("You are the server.")
        print("Please tell your friend to connect to your IP address.")
        conn = start_server()
        main.main_chessboard()
        if conn is not None:
            print("Starting game...")

            conn.send(b"Starting game...") # Displays "Starting game..." in the terminal of the client
            main.main_chessboard()
    elif mode == "client":
        print("You are the client.")
        print("Please ask your friend to start the server and give you their hostname.")
        sock = connect_to_server()
        main.main_chessboard()
        if sock is not None:
            print("Starting game...")
            data = sock.recv(1024)  # This receives the message sent by the server and prints it to the terminal
            print(data.decode())    # This receives the message sent by the server and prints it to the terminal
            main.main_chessboard()

if __name__ == '__main__':
    play_game()
