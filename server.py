"""
===================================================================
GENERAL UDP SERVER TEMPLATE (Python)
===================================================================
This is a simple, iterative request-reply server.
It is "inherently concurrent" because it is stateless.
"""
import socket
import sys

# --- Configuration ---
SERVER_HOST = '0.0.0.0'  # Listen on all interfaces
SERVER_PORT = 1234
BROADCAST_PORT = 1234
BROADCAST_IP = '10.152.255.255'
BUFFER_SIZE = 1024

def main():
    try:
        # --- 1. Create and Bind Socket ---
        # The 'with' statement handles s.close() automatically
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Set the socket to allow address reuse
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # Set the socket to broadcast mode
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            # Bind the socket to the address and port
            s.bind(('', SERVER_PORT)) # same as (SERVER_HOST, SERVER_PORT)
            print(f"Whiteboard server listening on port: {SERVER_PORT}...")
            
            # --- 2. Main Server Loop ---
            while True:
                # --- 3. Receive Data ---
                # This call blocks, waiting for a packet from ANY client
                # It returns the data AND the client's (ip, port) address
                try:
                    data_bytes, client_address = s.recvfrom(BUFFER_SIZE)
                    
                    print(f"Received {len(data_bytes)} bytes from {client_address}")

                    # --- 4. Process Data & Send Reply -
                    # Send a reply back to that specific client
                    s.sendto(data_bytes, (BROADCAST_IP, BROADCAST_PORT))

                except socket.error as e:
                    # Handle errors on a per-client basis
                    print(f"Error during communication: {e}")

    except socket.error as e:
        print(f"Socket error: {e}", file=sys.stderr)
    except KeyboardInterrupt:
        print("\nServer shutting down.")

# Standard Python entry point
if __name__ == "__main__":
    main()