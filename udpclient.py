# udpclient.py

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
        print("Usage: python3 udpclient.py hostname port \"expression\"", flush=True)
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

    # Create UDP socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(2)  # Set timeout to 2 seconds

        for op in operations:
            attempts = 0
            while attempts < 3:
                try:
                    print(f"Sending operation: {op}", flush=True)
                    sock.sendto(op.encode(), server_address)

                    data, _ = sock.recvfrom(1024)
                    response = data.decode().strip()

                    if response == "Invalid expression":
                        print("Invalid expression", flush=True)
                        sys.exit(0)

                    # Update op1 for the next operation
                    op_parts = op.split()
                    op1 = response
                    if len(operations) > 0:
                        # Replace op1 with the result for the next operation
                        pass  # Since operations are already correctly sequenced
                    break  # Received a response, move to next operation
                except socket.timeout:
                    attempts += 1
                    if attempts == 3:
                        print("Error - No response after 3 attempts", flush=True)
                        sys.exit(0)

        print(f"Total: {final_result}", flush=True)

if __name__ == "__main__":
    main()