import sys

class RPNCalculator:
    def __init__(self):
        self.input_error = False
        self.stack = []

    def is_empty(self):
        return len(self.stack) == 0

    def push(self, operand):
        self.stack.append(operand)

    def pop(self):
        if self.is_empty():
            self.warn_stack_underflow()
            self.input_error = True
            return 0
        return self.stack.pop()

    def warn_stack_underflow(self):
        print("Not enough operands in expression", file=sys.stderr)

    def warn_incomplete_expression(self):
        print("Incomplete expression", file=sys.stderr)

    def subtract(self):
        subtrahend = self.pop()
        minuend = self.pop()
        self.push(minuend - subtrahend)

    def divide(self):
        divisor = self.pop()
        dividend = self.pop()
        self.push(dividend // divisor)

    def evaluate(self, expression):
        tokens = self.tokenize(expression)
        self.stack = []

        for token in tokens:
            if token.isdigit() or (len(token) > 1 and token[0] == '-' and token[1:].isdigit()):
                self.push(int(token))
            else:
                if token == '+':
                    self.push(self.pop() + self.pop())
                elif token == '-':
                    self.subtract()
                elif token == '*':
                    self.push(self.pop() * self.pop())
                elif token == '/':
                    self.divide()
                else:
                    self.input_error = True
            if self.input_error:
                return self.input_error

        value = self.pop()
        if not self.is_empty():
            self.warn_incomplete_expression()
            self.input_error = True
            return self.input_error

        return value

    def tokenize(self, expression):
        tokens = []
        current_token = []

        for ch in expression:
            if ch == "-":
                if current_token:
                    tokens.append(''.join(current_token))
                current_token = [ ch ]
            elif not ch.isalnum():
                if current_token:
                    tokens.append(''.join(current_token))
                    current_token = []
                if not ch.isspace():
                    tokens.append(''.join(ch))
            else:
                current_token.append(ch)

        if current_token:
            tokens.append(''.join(current_token))

        return tokens
    
if __name__ == "__main__":
    calculator = RPNCalculator()

    while True:
        expression = input("Enter an RPN expression: ")
        calculator.input_error = False
        value = calculator.evaluate(expression)
        if not calculator.input_error:
            print(f"Value: {value}")
        else:
            break