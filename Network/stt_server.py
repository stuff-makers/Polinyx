import socket
import pickle
import threading


class SttServer:

    def __init__(self):

        def local_ip():
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip

        self.server_ip = local_ip()
        self.server_port = 60000
        self.BUFFER_SIZE = 1000000
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET,
                          socket.SO_SNDBUF, self.BUFFER_SIZE)
        self.s.bind((self.server_ip, self.server_port))
        self.transcribe_state = False
        self.t = None

    def receive_audio(self, label, frame):
        def thread_receive_audio():
            try:
                while self.transcribe_state:
                    data_receive = self.s.recvfrom(self.BUFFER_SIZE)
                    data_receive = pickle.loads(data_receive[0])
                    if len(data_receive[0]) != 0:
                        label['text'] = data_receive
                        frame.update()
                    else:
                        label['text'] = "....."
                        frame.update()
                        self.receive_audio(label, frame)
                else:
                    pass
            except OSError:
                self.receive_audio(label, frame)

        self.t = threading.Thread(target=thread_receive_audio, daemon=True)
        self.t.start()
