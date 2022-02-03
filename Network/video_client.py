import cv2
import mediapipe as mp
import pickle
import numpy as np
import pandas as pd
import socket


from PIL import Image, ImageTk
from tkinter import PhotoImage


class Call:

    def __init__(self, serverip, camera_opt=0):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 100000000)
        self.serverip = serverip  # here
        self.serverport = 7777
        self.camera_opt = camera_opt
        self.detect_call_state = ""
        self.normal_call_state = ""
        self.send_vid_img = PhotoImage(file="assets/send_vid.png")

    def detect_call(self, video_label, video_frame):

        with open('assets\\sign_1_1.pkl', 'rb') as model_file:
            model = pickle.load(model_file)

        mp_drawing = mp.solutions.drawing_utils
        mp_holistic = mp.solutions.holistic
        mp_drawing_styles = mp.solutions.drawing_styles
        mp_hands = mp.solutions.hands.Hands()

        cap = cv2.VideoCapture(self.camera_opt+cv2.CAP_DSHOW)

        while cap.isOpened():
            if self.detect_call_state == True:
                ret, frame = cap.read()

                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False

                results = mp_hands.process(image)

                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                try:
                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            mp_drawing.draw_landmarks(image, hand_landmarks, mp_holistic.HAND_CONNECTIONS, mp_drawing_styles.get_default_hand_landmarks_style(
                            ), mp_drawing_styles.get_default_hand_connections_style())
                            for p in mp_holistic.HandLandmark:
                                handrow = list(np.array(
                                    [[landmark.x, landmark.y, landmark.z] for landmark in hand_landmarks.landmark]).flatten())

                            X = pd.DataFrame([handrow])
                            body_signs_class = model.predict(X)[0]
                            body_signs_prob = model.predict_proba(X)[0]

                            prob = round(
                                body_signs_prob[np.argmax(body_signs_prob)], 2)
                            sign = body_signs_class.split(' ')[0]

                            if prob >= 0.8:

                                out = image.copy()
                                alpha = 0.55

                                # Error Probably here................
                                cv2.rectangle(
                                    image, (4, 414), (632, 446), (0, 0, 0), cv2.FILLED)

                                image = cv2.addWeighted(
                                    out, alpha, image, 1 - alpha, 0)
                                cv2.putText(
                                    image, sign, (8, 440), cv2.FONT_HERSHEY_SIMPLEX, 1, (19, 255, 236), 2, cv2.LINE_AA)

                except:
                    pass

                image_transformed = cv2.resize(image, (720, 640))
                image_resized_show = image_transformed
                image_resized_show = cv2.cvtColor(
                    image_resized_show, cv2.COLOR_BGR2RGB)
                image_resized = image_transformed
                image_resized_show = ImageTk.PhotoImage(
                    Image.fromarray(image_resized_show))
                video_label['image'] = image_resized_show
                video_frame.update()

                # <==========sending stuff===============>
                ret, buffer = cv2.imencode(
                    ".jpg", image_resized, [int(cv2.IMWRITE_JPEG_QUALITY), 30])

                x_as_bytes = pickle.dumps(list([ret, buffer]))
                self.socket.sendto(
                    x_as_bytes, (self.serverip, self.serverport))

            else:
                x_as_bytes = pickle.dumps(list([False, "No Frames"]))
                self.socket.sendto(
                    x_as_bytes, (self.serverip, self.serverport))
                video_label['image'] = self.send_vid_img
                video_frame.update()
                break

        cap.release()
        cv2.destroyAllWindows()

    def normal_call(self, label, frame):

        cap = cv2.VideoCapture(self.camera_opt+cv2.CAP_DSHOW)

        while cap.isOpened():

            if self.normal_call_state:
                ret, photo = cap.read()
                photo_transformed = cv2.resize(photo, (720, 640))
                photo_resized_show = photo_transformed
                photo_resized_show = cv2.cvtColor(
                    photo_resized_show, cv2.COLOR_BGR2RGB)
                photo_resized = photo_transformed
                photo_resized_show = ImageTk.PhotoImage(
                    Image.fromarray(photo_resized_show))
                label['image'] = photo_resized_show
                frame.update()

                # <=======sending stuff========>
                ret, buffer = cv2.imencode(
                    ".jpg", photo_resized, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
                x_as_bytes = pickle.dumps(list([ret, buffer]))
                self.socket.sendto(
                    x_as_bytes, (self.serverip, self.serverport))

            else:
                x_as_bytes = pickle.dumps(list([False, "No Frames"]))
                self.socket.sendto(
                    x_as_bytes, (self.serverip, self.serverport))
                label['image'] = self.send_vid_img
                frame.update()
                break

        cap.release()
        cv2.destroyAllWindows()
