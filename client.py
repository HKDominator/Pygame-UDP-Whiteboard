"""
===================================================================
UDP CLIENT TEMPLATE (Python)
===================================================================
This template demonstrates the core steps of a UDP client.
It does NOT connect. It just sends a packet and waits for one back.
"""
import pygame
import struct
import threading
import queue
import socket
import sys
import math

# --- Configuration ---
DRAW_MESSAGE_FORMAT = '!BBBBBHHHH'  # Message Type (1), Color (1), X (2), Y (2)
SERVER_HOST = '10.152.3.6'  # Server's hostname or IP
SERVER_PORT = 1234       # Server's port
BROADCAST_PORT = 1234       # Server's broadcast port
SERVER_ADDRESS = (SERVER_HOST, SERVER_PORT) # The (host, port) tuple

draw_queue = queue.Queue()

def receive_drawings(draw_queue):
    # Create a UDP socket for receiving drawings
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as recv_socket:
        #enable reuse address/port
        recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #enable receiving broadcasts
        recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        recv_socket.bind(('', BROADCAST_PORT))  # Bind to all interfaces on the broadcast port

        while True:
            data, addr = recv_socket.recvfrom(1024)  # Buffer size is 1024 bytes
            if len(data) == struct.calcsize(DRAW_MESSAGE_FORMAT):
                shape_data = struct.unpack(DRAW_MESSAGE_FORMAT, data)
                draw_queue.put(shape_data)
    

def main():
    try:
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        screen.fill((255, 255, 255))# White background

        receiver = threading.Thread(target=receive_drawings, args=(draw_queue,), daemon=True)
        receiver.start()

        # --- 1. Create Socket ---
        # Use 'with' for automatic cleanup (auto-close)
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #sending out our drawings

        draw_mode = 1 # 1 for line, 2 for rectangle, 3 for circle
        my_color = (0, 0, 255)  # Blue color
        my_fill = 0 #0 - outline, 1 - filled
        print("CONTROLS:")
        print("  Press '1': Draw Lines")
        print("  Press '2': Draw Rectangles")
        print("  Press '3': Draw Circles")
        print("  Press 'f': Toggle Fill/Outline")
        # --- 2. Communicate (Send/Receive) ---
        drawing = False
        start_pos = (0, 0)
        while True:
            # handle user input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        draw_mode = 1
                        my_color = (23,137,252)  # blue de france color
                    elif event.key == pygame.K_2:
                        draw_mode = 2
                        my_color = (255,208,123)  # jasmine
                    elif event.key == pygame.K_3:
                        draw_mode = 3
                        my_color = (186,165,255)  # red
                    elif event.key == pygame.K_f:
                        my_fill = 1 - my_fill  # Toggle between 0 and 1
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    start_pos = event.pos
                    drawing = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if drawing:
                        drawing = False
                        end_pos = event.pos

                    #Finished drawing a line, send it to server
                        shape_type = draw_mode
                        #color = (255, 0, 0)  # Red color
                        shape_data_tuple = (shape_type, *my_color, my_fill, *start_pos, *end_pos)
                        packed_data = struct.pack(DRAW_MESSAGE_FORMAT, *shape_data_tuple)

                        send_socket.sendto(packed_data, SERVER_ADDRESS)
            # handle incoming drawings
            try:
                shape_data = draw_queue.get_nowait()

                shape_type, r, g, b, fill, x1, y1, x2, y2 = shape_data
                color = (r, g, b)
                draw_width = 0 if fill == 1 else 2
                if shape_type == 1:  # Line
                    # --- LINE ---
                    # (x1, y1) to (x2, y2)
                    pygame.draw.line(screen, color, (x1, y1), (x2, y2), 2)
                elif shape_type == 2:  # Rectangle
                    # --- RECTANGLE ---
                    # Top-left (x1, y1), Bottom-right (x2, y2)
                    rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
                    pygame.draw.rect(screen, color, rect, draw_width)
                elif shape_type == 3:  # Circle
                    # --- CIRCLE ---
                    # Center (x1, y1), point on circumference (x2, y2)
                    radius = math.dist((x1, y1), (x2, y2))
                    if radius > draw_width:
                        pygame.draw.circle(screen, color, (x1, y1), radius, draw_width)
            except queue.Empty:
                pass
            pygame.display.flip() #update the full display Surface to the screen
        print("4. Socket closed.")

    except socket.error as e:
        print(f"Socket error: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)

# Standard Python entry point
if __name__ == "__main__":
    main()