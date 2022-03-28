from tkinter import Tk, Frame, PhotoImage, Label, ttk, Button, StringVar
import pickle as pk
from ttkthemes import ThemedTk
from UserData.user_model import User
from Network.video_client import Call
from Network.audio_client import AudioClient
import os
import tkinter.font as font
from Network.net import local_ip, write_ports
from Network.devices import return_device_list
from Network.stt_client import SpeechToText
from Network.stt_server import SttServer
from UserData.id_maker import set_new_meeting_id, fetch_ip, fetch_user_meeting_id, create_new_meeting_id


class PolinyxApp(ThemedTk, Tk):
    def __init__(self, window_name, icon):
        ThemedTk.__init__(self, window_name, icon)
        # inherited from Themed Tk to use good looking themes
        self.resizable(0, 0)
        self.overrideredirect(True)
        self.style = ttk.Style(self)
        self.style.theme_use("breeze")
        self.window_name = window_name
        self.icon = icon
        self.configure(bg="#1C1D1E")
        self.minsize(640, 320)
        self.maxsize(640, 320)
        self.title(self.window_name)
        self.iconbitmap(self.icon)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # setting up base frame to be used as container
        self.base_frame = Frame(self)
        self.base_frame.grid_columnconfigure(0, weight=1)
        self.base_frame.grid_rowconfigure(0, weight=1)
        self.base_frame.grid(row=0, column=0, sticky="nsew")

        # setting up a dictionary to store frame instances
        self.frames = dict()

        # initializing first frames
        self.create_frames((SplashFrame, RegisterFrame, LoginFrame, HomeFrame))

        # checking user auth state
        self.auth_check()

        # displaying splash frame on application startup
        self.display_splashframe(SplashFrame)

        # function to be executed after 4 seconds of displaying splash frame
        self.frames[SplashFrame].after(
            4000, self.display_mainframe, new_frame, SplashFrame)

    # to create new instance of destroyed frames and adding to frames map
    def create_frames(self, frame_create):
        for frame in (frame_create):
            f = frame(self.base_frame, self)
            self.frames[frame] = f
            f.grid(row=0, column=0, sticky="nsew")

    # to display splashframe
    def display_splashframe(self, frame_key):
        os.system('TASKKILL /F /IM video_server.exe')
        os.system('TASKKILL /F /IM audio_server.exe')
        frame = self.frames[frame_key]
        frame.tkraise()

    # to display other general frames
    def display_mainframe(self, frame_key, old_frame_key):
        self.overrideredirect(False)
        self.minsize(1280, 640)
        self.maxsize(1280, 640)
        old_frame = self.frames[old_frame_key]
        old_frame.pack_forget()
        self.create_frames((old_frame_key,))
        frame = self.frames[frame_key]
        frame.tkraise()

    # method to check user auth state and then send to respective windows
    def auth_check(self):
        global new_frame
        try:
            authfile = open(r"assets/auth_token.dat", "rb")
            authToken = pk.load(authfile)
            authfile.close()
            if len(authToken) != 0:
                new_frame = HomeFrame
            else:
                new_frame = LoginFrame
        except:
            new_frame = LoginFrame

    def create_video_frame(self, framecreate, old_frame_key, ip="", cam_id=0):
        f = framecreate(self.base_frame, self, ip, cam_id)
        self.frames[framecreate] = f
        f.grid(row=0, column=0, sticky="nsew")
        self.display_mainframe(framecreate, old_frame_key)

    def exit_chatframe(self, frame_key, old_frame_key):
        self.overrideredirect(False)
        self.minsize(1280, 640)
        self.maxsize(1280, 640)
        os.system('TASKKILL /F /IM video_server.exe')
        os.system('TASKKILL /F /IM audio_server.exe')
        old_frame = self.frames[old_frame_key]
        old_frame.pack_forget()
        self.create_frames((frame_key,))
        frame = self.frames[frame_key]
        frame.tkraise()


class SplashFrame(Frame):
    def __init__(self, container, root):
        Frame.__init__(self, container)

        self.root = root
        self.configure(bg="#1C1D1E")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # attaching application launcher icon
        self.splash_img = PhotoImage(file=r"assets/Icon.png")
        Label(self, image=self.splash_img, bd=-2).grid(row=0, column=0)


class RegisterFrame(Frame):
    def __init__(self, container, root):
        Frame.__init__(self, container)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        # self.configure(bg="#FFFFFF")
        self.signup_btn_img = PhotoImage(file="assets/signup_btn.png")

    # instantiating user object
        user_obj = User()

    # setup for picture
        pic_frame = Frame(self, width=640, height=640)
        pic_frame.grid(row=0, column=0)
        self.frame_img = PhotoImage(file=r"assets/register.png")
        Label(pic_frame, image=self.frame_img, bd=-
              2).grid(row=0, column=0)

    # setup for signup form
        form_frame = Frame(self, width=640, height=640)
        form_frame.grid(row=0, column=1)
        # form_frame.configure(bg="#FFFFFF")
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_rowconfigure(9, weight=1)

        # labels
        first_name_label = Label(
            form_frame, text="Name", fg="#1C1D1E",  font=font.Font(family="segoe ui semibold", size=16))
        username_label = Label(form_frame, text="Username",
                               fg="#1C1D1E", font=font.Font(family="segoe ui semibold", size=16))
        email_label = Label(form_frame, text="Email Id",
                            fg="#1C1D1E",  font=font.Font(family="segoe ui semibold", size=16))
        password_label = Label(form_frame, text="Password",
                               fg="#1C1D1E",  font=font.Font(family="segoe ui semibold", size=16))
        first_name_label.grid(row=0, column=0, sticky="w", padx="100")
        username_label.grid(row=2, column=0, sticky="w", padx="100")
        email_label.grid(row=4, column=0, sticky="w", padx="100")
        password_label.grid(row=6, column=0, sticky="w", padx="100")

        # entry widgets
        first_name_entry = ttk.Entry(
            form_frame, width="400")
        username_entry = ttk.Entry(form_frame, width="400")
        email_entry = ttk.Entry(form_frame, width="400")
        password_entry = ttk.Entry(form_frame, width="400", show="*")
        first_name_entry.grid(row=1, column=0, padx="100", pady=(0, 16))
        username_entry.grid(row=3, column=0, padx="100", pady=(0, 16))
        email_entry.grid(row=5, column=0, padx="100", pady=(0, 16))
        password_entry.grid(row=7, column=0, padx="100")

        # error label [To be replaced]
        err_label = Label(form_frame, text="", fg="#1C1D1E")
        err_label.grid(row=8, column=0, sticky="nsew")

        # function to be triggered when Signup btn is clicked.
        def signup_action():

            # fetching user entry
            first_name = first_name_entry.get()
            username = username_entry.get()
            email = email_entry.get()
            password = password_entry.get()

            # checking user entry
            if len(email) != 0 and len(password) != 0 and len(first_name) != 0 and len(username) != 0:

                # creating account
                valid_bool = user_obj.create_account(
                    first_name, username, email, password)

                # checking if account creation was successful and login to app as well
                if valid_bool[1]:
                    create_new_meeting_id()
                    window = HomeFrame
                    root.display_mainframe(window, RegisterFrame)
                    root.create_frames((window,))
                else:
                    err_label['text'] = "An Error has Occurred. Try Again later."
            else:
                err_label['text'] = "Please fill in the above fields"

        # signup button
        signup_button = Button(
            form_frame, image=self.signup_btn_img, command=signup_action, borderwidth=0)
        signup_button.grid(row=9, column=0, padx=200)

        # to navigate to login page To be replaced.....
        toLogBtn = Button(form_frame, text="Already have an account?",
                          command=lambda: root.display_mainframe(LoginFrame, RegisterFrame), borderwidth=0, fg="#1C1D1E")
        toLogBtn.grid(row=10, column=0, pady=(20, 0))


class LoginFrame(Frame):
    def __init__(self, container, root):
        Frame.__init__(self, container)
        # self.configure(bg="#FFFFFF")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.login_btn_image = PhotoImage(file="assets/login_btn.png")

    # creating an instance of user object

        user_obj = User()

    # Frame setup for picture

        pic_frame = Frame(self, width=640, height=640)
        pic_frame.grid(row=0, column=0)
        self.frame_img = PhotoImage(file=r"assets/login.png")
        Label(pic_frame, image=self.frame_img, bd=-
              2).grid(row=0, column=0)

    # frame setup for login form
        # frames

        form_frame = Frame(self, width=640, height=640)
        form_frame.grid(row=0, column=1)
        # form_frame.configure(bg="#FFFFFF")
        form_frame.grid_columnconfigure(0, weight=1)
        form_frame.grid_rowconfigure(7, weight=1)

        # labels
        email_label = Label(form_frame, text="Email Id",
                            fg="#1C1D1E", font=font.Font(family="segoe ui semibold", size=16))
        password_label = Label(
            form_frame, text="Password", fg="#1C1D1E", font=font.Font(family="segoe ui semibold", size=16))
        email_label.grid(row=0, column=0, sticky="w", padx="100")
        password_label.grid(row=2, column=0, sticky="w", padx="100")

        # entry widgets
        email_entry = ttk.Entry(form_frame, width="400")
        password_entry = ttk.Entry(form_frame, width="400", show="*")
        email_entry.grid(row=1, column=0, padx="100", pady=(0, 16))
        password_entry.grid(row=3, column=0, padx="100", pady=(0, 16))

        # Error Label [create new frame and pack there for later...]
        err_label = Label(form_frame, text="", fg="#1C1D1E")
        err_label.grid(row=5, column=0)

        # function to be triggered when login button is clikd
        def login_action():
            # fetching user input in entry widgets
            try:
                email = email_entry.get()
                password = password_entry.get()

                # checking user entry
                if len(email) != 0 and len(password) != 0:

                    # logging user in
                    valid_bool = user_obj.login(email, password)

                    # checking if login was successful
                    if valid_bool[1]:
                        window = HomeFrame
                        root.display_mainframe(window, LoginFrame)
                        root.create_frames((window,))
                    else:
                        err_label['text'] = "Try Again! Credentials do not match"

                else:
                    err_label['text'] = "Please fill in the above fields"
            except:
                root.display_mainframe(LoginFrame, LoginFrame)

        # login button
        login_button = Button(
            form_frame, command=login_action, image=self.login_btn_image, borderwidth=0)
        login_button.grid(row=6, column=0)

        # To be replaced later for navigating to Signup
        toRegBtn = Button(form_frame, text="Create a new account?",
                          command=lambda: root.display_mainframe(RegisterFrame, LoginFrame), borderwidth=0, fg="#1C1D1E")
        toRegBtn.grid(row=7, column=0, pady=(20, 0))


class HomeFrame(Frame):
    def __init__(self, container, root):
        Frame.__init__(self, container)
        self.root = root
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
 # <--------------------------comms--------------------------------------->
        # frame to start call from
        self.comm_frame = Frame(self, width=720, height=640)
        self.comm_frame.grid(row=0, column=0)
        self.comm_frame.grid_rowconfigure(11, weight=1)
        self.comm_frame.grid_columnconfigure(0, weight=1)
        self.comm_frame.pack_propagate(0)
        self.cam_id = None
        self.meeting_id = None
        self.option_var = StringVar(self)

        meeting_id_label = Label(
            self.comm_frame, text="Connection ID", font=font.Font(family="segoe ui semibold", size=16))
        meeting_id_label.grid(row=0, column=0, sticky="w", padx="250")
        meeting_id_entry = ttk.Entry(self.comm_frame, width="400")
        meeting_id_entry.grid(row=1, column=0, padx="250", pady=(0, 16))

        options, options_dict = return_device_list()

        def set_id(event):
            self.cam_id = int(options_dict[self.option_var.get()])
        self.root.style.configure('my.TMenubutton', font=font.Font(
            family="segoe ui semibold", size=16))
        device_option_menu = ttk.OptionMenu(
            self.comm_frame, self.option_var, "Select a Camera Device", *options, direction="right", command=set_id, style='my.TMenubutton')
        device_option_menu.grid(
            row=10, column=0, padx="250", pady=(0, 16), sticky="nsew")

        self.start_call_img = PhotoImage(file="assets/start_call.png")
        connect_btn = Button(
            self.comm_frame, image=self.start_call_img, borderwidth=0, command=lambda: self.goTochat(fetch_ip(meeting_id_entry.get()), self.cam_id))
        connect_btn.grid(row=11, column=0)

 # <---------------------------user details-------------------------------->
        # Frame to view and Edit user details
        self.user_frame = Frame(self, bg="lavender", width=560, height=640)
        self.user_frame.grid(row=0, column=1, sticky="nsew")
        self.user_frame.configure(bg="#1C1D1E")
        self.user_frame.grid_columnconfigure(1, weight=1)
        self.user_frame.grid_rowconfigure(8, weight=1)
        self.signout_btn_img = PhotoImage(file="assets/sign_out_1.png")
        self.gen_id_btn_img = PhotoImage(file="assets/generate_id.png")
        self.line_img = PhotoImage(file="assets/line.png")
        sign_out_btn = Button(
            self.user_frame, image=self.signout_btn_img, borderwidth=0, command=self.logout, fg="white", bg="#1C1D1E")
        sign_out_btn.grid(row=8, column=0, pady=(16, 0))

        line_label = Label(
            self.user_frame, image=self.line_img, fg="white", bg="#1C1D1E")
        line_label.grid(row=4, column=0, pady=24)
    # instantiating User Object
        connection_id_label = Label(
            self.user_frame, text="Connection ID", fg="white", bg="#1C1D1E", font=font.Font(family="segoe ui", size=18))
        connection_id_label.grid(
            row=5, column=0, padx=120, sticky="w")

        meeting_id_label = Label(
            self.user_frame, text=fetch_user_meeting_id(), fg="white", bg="#1C1D1E", font=font.Font(family="segoe ui", size=14, weight="bold"))
        meeting_id_label.grid(row=6, column=0, padx=120, sticky="w")

        gen_meeting_id_btn = Button(self.user_frame, image=self.gen_id_btn_img, borderwidth=0, command=lambda: set_new_meeting_id(
            meeting_id_label, self.user_frame), fg="white", bg="#1C1D1E")
        gen_meeting_id_btn.grid(
            row=7, column=0, sticky="w", padx=120, pady=(16, 0))
        self.user_obj = User()

    # function to be triggered on clicking log out

    # checks if a token is present in auth_token.dat
    # and fetches data from db using token then displays it

        def reload():
            try:
                userfile = open(r"assets/auth_token.dat", "rb")
                usertoken = pk.load(userfile)
                userfile.close()
                if len(usertoken) != 0:
                    userdata = self.user_obj.fetch_data(usertoken[0])
                    self.display_data(userdata)
                else:
                    self.display_data()
            except:
                self.logout()

    # calling reload function everytime an instance of HomeFrame Object is created to get refresh data

        reload()

    def logout(self):
        self.user_obj.logout()
        window = LoginFrame
        self.root.display_mainframe(window, HomeFrame)

    # method to display_data on HomeFrame

    def display_data(self, usr_data=[("", "", "")]):
        # Label(self.user_frame, text="Name", fg="white", bg="#1C1D1E", font=font.Font(family="segoe ui semibold", size=20)).grid(
        #     row=0, column=0, padx=150, sticky="w", pady=(100, 0))
        try:
            Label(self.user_frame, text=usr_data[0][0], fg="white", bg="#1C1D1E", font=font.Font(family="segoe ui", size=24, weight="bold")).grid(
                row=1, column=0, padx=120, pady=(120, 0), sticky="w")

            # Label(self.user_frame, text="Username", fg="white", bg="#1C1D1E", font=font.Font(family="segoe ui semibold", size=20)).grid(
            #     row=2, column=0, padx=150, sticky="w")

            Label(self.user_frame, text=usr_data[0][1], fg="white", bg="#1C1D1E", font=font.Font(family="segoe ui", size=18)).grid(
                row=2, column=0, padx=120, sticky="w")

            # Label(self.user_frame, text="Email id", fg="white", bg="#1C1D1E", font=font.Font(family="segoe ui semibold", size=16)).grid(
            #     row=4, column=0, padx=150, sticky="w")

            Label(self.user_frame, text=usr_data[0][2], fg="white", bg="#1C1D1E", font=font.Font(family="segoe ui", size=18)).grid(
                row=3, column=0, padx=120, sticky="w")
        except:
            self.logout()

    def goTochat(self, ip_entry, cam_id):
        self.root.create_video_frame(
            ChatFrame, HomeFrame, ip_entry, int(cam_id))


class ChatFrame(Frame):
    def __init__(self, container, root, ip, cam_id):
        Frame.__init__(self, container)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.root = root
        self.ip = ip

        # Video and Audio Object Instances
        self.call_obj = Call(self.ip, cam_id)
        self.audio_send_obj = AudioClient(self.ip)
        self.stt_client_obj = SpeechToText(False, self.ip)
        self.stt_server_obj = SttServer()
        self.stt_server_obj.transcribe_state = True
        # place holder for user video frame
        self.send_vid = PhotoImage(file=r"assets/send_vid.png")

        os.startfile("dist\\audio_server.exe")

        os.startfile("dist\\video_server.exe")
        # button states
        self.detect_btn_state = False
        self.normal_btn_state = False
        self.audio_send_btn_state = False

        # button Images
        self.cam_disabled_img = PhotoImage(file="assets/cam_disabled.png")
        self.cam_enabled_img = PhotoImage(file="assets/cam_enabled.png")
        self.end_call_img = PhotoImage(file="assets/end_call.png")
        self.muted_state_img = PhotoImage(file="assets/muted_state.png")
        self.unmute_state_img = PhotoImage(file='assets/unmute_state.png')
        self.detect_enabled_img = PhotoImage(file="assets/detect_enabled.png")
        self.detect_disabled_img = PhotoImage(
            file="assets/detect_disabled.png")

        # state dictionaries
        self.detect_dict = {True: self.detect_enabled_img,
                            False: self.detect_disabled_img}
        self.normal_dict = {True: self.cam_enabled_img,
                            False: self.cam_disabled_img}
        self.mic_dict = {True: self.unmute_state_img,
                         False: self.muted_state_img}

        self.video_frame = Frame(self, bg="black")
        self.video_frame.grid(row=0, column=0, sticky="nsew")
        self.video_label = Label(self.video_frame, image=self.send_vid, bd=-2)
        self.video_label.pack()

        self.controls_frame = Frame(self)
        self.controls_frame.grid(row=0, column=1)
        self.controls_frame.grid_columnconfigure(3, weight=1)
        self.controls_frame.grid_rowconfigure(2, weight=1)

        self.send_transcribe_label = Label(
            self.controls_frame, text="...", font=font.Font(family="segoe ui", size=12))
        self.send_transcribe_label.grid(
            row=1, column=0, columnspan=3, sticky="w")

        # self.stt_client_obj.speech(
        #     self.send_transcribe_label, self.controls_frame)
        self.recv_transcribe_label = Label(
            self.controls_frame, text="...", font=font.Font(family="segoe ui", size=12))
        self.recv_transcribe_label.grid(
            row=2, column=0, columnspan=3, sticky="w")

        self.stt_server_obj.receive_audio(
            self.recv_transcribe_label, self.controls_frame)

        self.detect_btn = Button(self.controls_frame, image=self.detect_disabled_img,
                                 command=lambda: self.detect_btn_state_manager(), borderwidth=0)
        self.detect_btn.grid(row=0, column=0)

        self.normal_btn = Button(self.controls_frame, image=self.cam_disabled_img,
                                 command=lambda: self.normal_btn_state_manager(), borderwidth=0)
        self.normal_btn.grid(row=0, column=1)

        self.audio_send_btn = Button(
            self.controls_frame, image=self.muted_state_img, command=self.audio_send_btn_state_manager, borderwidth=0)
        self.audio_send_btn.grid(row=0, column=2)

        self.end_call_btn = Button(
            self.controls_frame, image=self.end_call_img, command=self.exit_call, borderwidth=0)
        self.end_call_btn.grid(row=0, column=3)

    def detect_btn_state_manager(self):
        if self.detect_btn_state == False:
            self.detect_btn_state = True
            self.detect_btn['image'] = self.detect_dict[self.detect_btn_state]
            self.call_obj.detect_call_state = self.detect_btn_state
            self.call_obj.detect_call(self.video_label, self.video_frame)

        else:
            self.detect_btn_state = False
            self.detect_btn['image'] = self.detect_dict[self.detect_btn_state]
            self.call_obj.detect_call_state = self.detect_btn_state
            self.call_obj.detect_call(self.video_label, self.video_frame)

    def normal_btn_state_manager(self):
        if self.normal_btn_state == False:
            self.normal_btn_state = True
            self.normal_btn['image'] = self.normal_dict[self.normal_btn_state]
            self.call_obj.normal_call_state = self.normal_btn_state
            self.call_obj.normal_call(self.video_label, self.video_frame)
        else:
            self.normal_btn_state = False
            self.normal_btn['image'] = self.normal_dict[self.detect_btn_state]
            self.call_obj.normal_call_state = self.normal_btn_state
            self.call_obj.normal_call(self.video_label, self.video_frame)

    def audio_send_btn_state_manager(self):
        if self.audio_send_btn_state == False:
            self.audio_send_btn_state = True
            self.audio_send_btn['image'] = self.mic_dict[self.audio_send_btn_state]
            self.audio_send_obj.send_state = self.audio_send_btn_state
            self.stt_client_obj.send_state = self.audio_send_btn_state
            self.stt_client_obj.speech(
                self.send_transcribe_label, self.controls_frame)
            self.audio_send_obj.send_audio()
        else:
            self.audio_send_btn_state = False
            self.audio_send_btn['image'] = self.mic_dict[self.audio_send_btn_state]
            self.audio_send_obj.send_state = self.audio_send_btn_state
            self.stt_client_obj.send_state = self.audio_send_btn_state
            self.send_transcribe_label['text'] = "..."
            self.stt_client_obj.send_state = self.audio_send_btn_state

    def exit_call(self):
        self.detect_btn_state = False
        self.call_obj.detect_call_state = self.detect_btn_state
        self.call_obj.detect_call(self.video_label, self.video_frame)
        self.stt_server_obj.transcribe_state = False
        self.normal_btn_state = False
        self.call_obj.normal_call_state = self.normal_btn_state
        self.call_obj.normal_call(self.video_label, self.video_frame)
        self.root.exit_chatframe(HomeFrame, ChatFrame)
        self.stt_server_obj.s.close()


# creating an instance of main window for application
root_window = PolinyxApp("", r"assets/polinyx.ico")
root_window.mainloop()
