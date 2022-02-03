import cv2
import socket
import numpy
import pickle
import sys


def local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


ip = local_ip()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 7777  # here
s.bind((ip, port))
state = ""

while True:
    x = s.recvfrom(100000000)
    data = x[0]
    data = pickle.loads(data)
    state = data[0]
    img_data = data[1]
    if cv2.waitKey(10) == 13 or state == False:
        try:
            cv2.destroyWindow('Incoming Video')
            continue
        except:
            pass
    else:
        img_data = cv2.imdecode(img_data, cv2.IMREAD_COLOR)
        cv2.imshow('Incoming Video', img_data)
        continue
