import socket, cv2, pickle, struct
# create socket
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

sock.connect(('127.0.0.1',9090))

data = b""
payload_size = struct.calcsize("Q")

while True:
    while len(data) < payload_size:
        packet = sock.recv(4*1024) 
        if not packet: break
        data+=packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q",packed_msg_size)[0]
    while len(data) < msg_size:
        data += sock.recv(4*1024)
    frame_data = data[:msg_size]
    data  = data[msg_size:]
    frame = pickle.loads(frame_data)
    cv2.imshow("RECEIVING VIDEO",frame)
    key = cv2.waitKey(1) & 0xFF
    if key  == ord('q'):
        break
sock.close()
cv2.destroyAllWindows()
