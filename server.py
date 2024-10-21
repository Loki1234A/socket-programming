import socket
import threading

# Store client information including the connection socket and unique ID
clients = {}
client_id_counter = 0  # To assign a unique ID to each client

def handle_client(conn, client_address, client_id):
    """
    Function to handle communication with a connected client.
    This runs in a separate thread for each client.
    """
    print(f"Connection established with {client_address}, assigned Client ID: {client_id}")
    
    try:
        while True:
            # Receive data from the client
            data = conn.recv(1024)
            if data:
                message = data.decode()
                print(f"Received from Client {client_id}: {message}")

                # Close connection if the client sends "CLOSE SOCKET"
                if message == "CLOSE SOCKET":
                    print(f"Closing connection with Client {client_id} as requested.")
                    break
                
                # Send back the message in uppercase
                response = message.upper()
                print(f"Sending to Client {client_id}: {response}")
                conn.sendall(response.encode())
            else:
                # No data means the client has closed the connection
                print(f"No more data from Client {client_id}. Closing connection.")
                break
    except Exception as e:
        print(f"An error occurred with Client {client_id}: {e}")
    finally:
        # Close the connection and remove the client from the client list
        conn.close()
        del clients[client_id]
        print(f"Connection with Client {client_id} closed. Waiting for new connections...")

def start_server():
    """
    Main function to start the server and listen for incoming connections.
    Each client is handled in a separate thread.
    """
    global client_id_counter

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12478)
    print(f"Starting server on {server_address[0]}:{server_address[1]}")

    try:
        server_socket.bind(server_address)
        server_socket.listen()
        print("Server is ready to accept connections...")

        while True:
            # Accept a new connection
            conn, client_address = server_socket.accept()
            client_id = client_id_counter
            client_id_counter += 1

            # Store the client info in a dictionary
            clients[client_id] = {
                'socket': conn,
                'address': client_address
            }

            # Start a new thread to handle the client
            client_thread = threading.Thread(
                target=handle_client, 
                args=(conn, client_address, client_id)
            )
            client_thread.start()

            print(f"Client {client_id} connected from {client_address}. Total connected clients: {len(clients)}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        server_socket.close()
        print("Server closed.")

if __name__ == "__main__":
    start_server()
