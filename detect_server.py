import socket
import cv2
import pickle
import struct
import imutils
import sys

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host_ip = sys.argv[1]
port = int(sys.argv[2])

server_socket.bind((host_ip, port))
server_socket.listen(5)
print("Listening for incoming connections at {}:{}".format(host_ip, port))

while True:
    
    client_socket, addr = server_socket.accept()
    print("Got a connection from {}".format(addr))

    
    if client_socket:
        
        vid = cv2.VideoCapture(0)

        while vid.isOpened():
          
            success, frame = vid.read()
            if not success:
                break

            frame = imutils.resize(frame, width=320)
            frame = cv2.convertScaleAbs(frame, 0.5, 1.5)

            data = pickle.dumps(frame)
            message = struct.pack("Q", len(data)) + data
            client_socket.sendall(message)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

        vid.release()
        client_socket.close()
