# udpserver.py

import socket
import sys
from rpncalc import RPNCalculator

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 udpserver.py port", flush=True)
        sys.exit(1)

    port = int(sys.argv[1])
    server_address = ('127.0.0.1', port)

    # Create UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        try:
            sock.bind(server_address)
            print(f"Server started on port {port}. Accepting connections", flush=True)
        except Exception as e:
            print(f"Failed to bind socket: {e}", flush=True)
            sys.exit(1)

        calculator = RPNCalculator()

        while True:
            try:
                data, client_address = sock.recvfrom(1024)  # Buffer size 1024 bytes
                expression = data.decode().strip()

                print(f"Received operation: {expression}", flush=True)

                # Evaluate the expression
                result = calculator.evaluate(expression)

                if isinstance(result, int):
                    response = str(result)
                else:
                    response = "Invalid expression"

                # Send the response back to the client
                sock.sendto(response.encode(), client_address)
            except Exception as e:
                # Handle any unexpected errors gracefully
                print(f"Error processing request: {e}", flush=True)
                continue

if __name__ == "__main__":
    main()