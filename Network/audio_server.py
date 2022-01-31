import pyaudio
import socket
import pickle
import threading


class AudioServer:

    def __init__(self, server_ip, server_port):

        self.server_ip = server_ip
        self.server_port = server_port

        self.CHUNK = 1024
        self.WIDTH = 2
        self.CHANNELS = 1
        self.RATE = 44100
        self.BUFFER_SIZE = 100000000

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET,
                          socket.SO_SNDBUF, self.BUFFER_SIZE)

        self.p = pyaudio.PyAudio()

        self.stream = self.p.open(format=self.p.get_format_from_width(self.WIDTH),
                                  channels=self.CHANNELS,
                                  rate=self.RATE,
                                  input=True,
                                  output=True,
                                  frames_per_buffer=self.CHUNK)

    def receive_audio(self):

        self.s.bind((self.server_ip, self.server_port))

        while True:
            data_receive = self.s.recvfrom(self.BUFFER_SIZE)
            data_receive = pickle.dumps(data_receive)
            self.stream.write(data_receive, self.CHUNK)

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()


if __name__ == '__main__':

    def local_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip

    def port():
        f = open('ports.dat', 'rb')
        port = pickle.load(f)[1]
        f.close()
        return port

    ip = local_ip()
    port = int(port())
    server = AudioServer(ip, port)
    server.receive_audio()
