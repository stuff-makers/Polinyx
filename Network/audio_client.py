import pyaudio
import socket
import threading
# from Network.stt import SpeechToText


class AudioClient:

    def __init__(self, client_ip):

        self.client_ip = client_ip  # here
        self.client_port = 8888
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
        self.send_state = False

        # self.stt_obj = SpeechToText(self.send_state)

    def send_audio(self):
        def thread_send_audio():
            self.s.connect((self.client_ip, self.client_port))

            while self.send_state:
                # self.stt_obj.send_state = self.send_state
                data_send = self.stream.read(self.CHUNK)
                self.s.sendto(data_send, (self.client_ip, self.client_port))
            else:
                if not(self.stream.is_active()):
                    self.stream.stop_stream()
                    self.stream.close()
                    self.p.terminate()
                    print("Exiting")
        t = threading.Thread(target=thread_send_audio, daemon=True)
        t.start()
