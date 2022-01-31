import socket
import pickle


def local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def write_ports(ports_list):
    f = open("ports.dat", "wb")
    pickle.dump(ports_list, f)
    f.close()
