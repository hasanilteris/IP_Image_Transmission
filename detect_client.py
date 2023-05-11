import socket,cv2, pickle,struct, sys
import torch
import cv2

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip =  sys.argv[1] #'192.168.0.178'
port = 5600
client_socket.connect((host_ip,port))
data = b""
model = torch.hub.load('yolov5', 'custom', path='best.pt', source='local')
payload_size = struct.calcsize("Q")

def send_output(output):
    message = output.to_bytes(1, byteorder='big')
    client_socket.send(message)

while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4*1024)
        if not packet: break
        data+=packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q",packed_msg_size)[0]

    while len(data) < msg_size:
        data += client_socket.recv(4*1024)
    frame_data = data[:msg_size]
    data  = data[msg_size:]
    frame = pickle.loads(frame_data)
    cv2.imshow("RECEIVING VIDEO",frame)
    results = model(frame)
    df = results.pandas().xyxy[0]
    if((not df['name'].empty)):
        df_sort = df.sort_values('confidence')
        top_result = df_sort.iloc[0]
        if(top_result[['confidence']].any() > 0.7):
            client_socket.send(str(data_to_send).encode('utf-8'))
            data_to_send = 1
            print(data_to_send)
        else:
            client_socket.send(str(data_to_send).encode('utf-8'))
            data_to_send = 0
            print(data_to_send)
            
    else:
        
        client_socket.send(str(data_to_send).encode('utf-8'))
        data_to_send = 1
        print(data_to_send)
    send_output(data_to_send)

    key = cv2.waitKey(1) & 0xFF
    if key  == ord('q'):
        break
client_socket.close()

