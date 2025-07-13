import tkinter as tk
from frames import MainWindow, LoginWindow, ApiWindow

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("My Application")
        self.login_token = None
        self.username = None
        self.api_timeout = 5  # minutes
        self.container = tk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True)

        self.frames = {}
        for F in (MainWindow, LoginWindow, ApiWindow):
            frame = F(master=self.container, controller=self) #init custom frame
            self.frames[F.__name__] = frame #add frame to the dictionary
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(MainWindow)

    def show_frame(self, frame_class):
        frame = self.frames[frame_class.__name__]
        if frame_class.__name__ == 'ApiWindow':
            if not self.login_token:
                self.show_frame(LoginWindow)
                return
            frame.set_login_token(self.login_token)
            frame.set_username(self.username)
            self.after(60 * 1000 * self.api_timeout, lambda: self.redirect_to_main)  # Auto-redirect after 5 minutes
        frame.tkraise()

    def redirect_to_main(self):
        self.show_frame(MainWindow)

    def set_login_token(self, token):
        self.login_token = token
    
    def set_username(self, username):
        self.username = username

    def mainloop(self):
        super().mainloop()

    def run(self):
        self.mainloop()