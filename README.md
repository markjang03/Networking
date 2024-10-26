Name: Mark Jang

Files Submitted:
- tcpclient.py: TCP client implementation for the RPN calculator.
- tcpserver.py: TCP server implementation for the RPN calculator.
- udpclient.py: UDP client implementation for the RPN calculator.
- udpserver.py: UDP server implementation for the RPN calculator.
- rpncalc.py: Helper module for evaluating RPN expressions.

Key Learnings:
- Understanding of socket programming using TCP and UDP protocols.
- Implementation of client-server architecture.
- Handling network errors and implementing retry mechanisms.
- Designing a simple application-layer protocol for communication.

Challenges:
- Parsing and validating RPN expressions.
- Ensuring correct synchronization between client and server.
- Implementing timeout and retry logic for UDP communication.

Known Bugs or Limitations:
- The client does not handle floating-point numbers; it only supports integers.
- Maximum length of an expression is limited by the buffer size (1024 bytes).
- Division by zero results in an "Invalid expression" error.