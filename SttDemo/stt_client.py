import speech_recognition as sr
import socket
import pickle
import threading


class SpeechToText:
    def __init__(self, send_state, client_ip):
        self.client_ip = client_ip
        self.client_port = 60000
        self.recog_text = None
        self.send_state = send_state
        self.BUFFER_SIZE = 1000000
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET,
                          socket.SO_SNDBUF, self.BUFFER_SIZE)
        self.s.connect((self.client_ip, self.client_port))

    def speech(self):
        while self.send_state:
            try:
                if self.send_state:
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        audio = recognizer.listen(source)
                        self.recog_text = recognizer.recognize_google(
                            audio)
                        print(self.recog_text)
                        t_as_bytes = pickle.dumps(self.recog_text)
                        self.s.sendto(
                            t_as_bytes, (self.client_ip, self.client_port))
                else:
                    break
            except sr.UnknownValueError:
                print("Kindly repeat could not transcribe..\n")

        else:
            pass
