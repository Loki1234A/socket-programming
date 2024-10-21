import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12478)
    print(f"Connecting to server at {server_address[0]}:{server_address[1]}")

    try:
        client_socket.connect(server_address)
        print("Connection established.")

        while True:
            message = input("Enter message to send (type 'CLOSE SOCKET' to close the connection): ")
            print(f"Sending message: {message}")
            client_socket.sendall(message.encode())

            if message == "CLOSE SOCKET":
                print("Closing connection to server.")
                break  # Exit the loop if the user wants to close the connection

            data = client_socket.recv(1024)
            print(f"Received uppercase message from server: {data.decode()}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()
        print("Client closed.")

if __name__ == "__main__":
    start_client()
