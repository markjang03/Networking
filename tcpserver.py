# tcpserver.py

import socket
import sys
from rpncalc import RPNCalculator

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 tcpserver.py port", flush=True)
        sys.exit(1)

    port = int(sys.argv[1])
    server_address = ('127.0.0.1', port)

    # Create TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.bind(server_address)
            sock.listen(1)  # Listen for incoming connections
            print(f"Server started on port {port}. Accepting connections", flush=True)
        except Exception as e:
            print(f"Failed to bind socket: {e}", flush=True)
            sys.exit(1)

        calculator = RPNCalculator()

        while True:
            try:
                connection, client_address = sock.accept()
                with connection:
                    while True:
                        data = connection.recv(1024)
                        if not data:
                            break  # No more data from client
                        expression = data.decode().strip()

                        print(f"Received operation: {expression}", flush=True)

                        # Evaluate the expression
                        result = calculator.evaluate(expression)

                        if isinstance(result, int):
                            response = str(result)
                        else:
                            response = "Invalid expression"

                        # Send the response back to the client
                        connection.sendall(response.encode())
            except Exception as e:
                # Handle any unexpected errors gracefully
                print(f"Error processing request: {e}", flush=True)
                continue

if __name__ == "__main__":
    main()