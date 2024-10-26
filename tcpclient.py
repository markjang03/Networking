# tcpclient.py

import socket
import sys
from rpncalc import RPNCalculator

def parse_expression(expression):
    calculator = RPNCalculator()
    tokens = calculator.tokenize(expression)
    stack = []
    operations = []

    for token in tokens:
        if token.isdigit() or (len(token) > 1 and token[0] == '-' and token[1:].isdigit()):
            stack.append(int(token))
        else:
            if len(stack) < 2:
                return None  # Invalid expression
            op2 = stack.pop()
            op1 = stack.pop()
            operations.append(f"{op1} {op2} {token}")
            # Perform the operation to get the intermediate result
            temp_expr = f"{op1} {op2} {token}"
            result = calculator.evaluate(temp_expr)
            if isinstance(result, int):
                stack.append(result)
            else:
                return None  # Invalid expression
    if len(stack) != 1:
        return None  # Invalid expression
    return operations, stack[0]

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 tcpclient.py hostname port \"expression\"", flush=True)
        sys.exit(1)

    hostname = sys.argv[1]
    port = int(sys.argv[2])
    expression = sys.argv[3]

    # Parse the expression into operations
    parsed = parse_expression(expression)
    if not parsed:
        print("Invalid expression", flush=True)
        sys.exit(0)

    operations, final_result = parsed

    server_address = (hostname, port)

    # Create TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect(server_address)
        except Exception as e:
            print(f"Failed to connect to server: {e}", flush=True)
            sys.exit(1)

        for op in operations:
            try:
                print(f"Sending operation: {op}", flush=True)
                sock.sendall(op.encode())

                data = sock.recv(1024)
                if not data:
                    print("Invalid expression", flush=True)
                    sys.exit(0)
                response = data.decode().strip()

                if response == "Invalid expression":
                    print("Invalid expression", flush=True)
                    sys.exit(0)

                # Update op1 for the next operation if needed
            except Exception as e:
                print(f"Error communicating with server: {e}", flush=True)
                sys.exit(1)

        print(f"Total: {final_result}", flush=True)

if __name__ == "__main__":
    main()