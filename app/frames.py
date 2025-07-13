import tkinter as tk
import requests
from requests_maker import RequestsMaker

class Window(tk.Frame):
    def __init__(self, master=None, controller=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()
        self.pack_widgets()
        self.controller = controller

    def create_widgets(self):
        pass

    def pack_widgets(self):
        pass

class MainWindow(Window):
    def __init__(self, master=None, controller=None):
        self.name = 'main'
        super().__init__(master, controller)

    def create_widgets(self):
        label = tk.Label(self, text="Welcome to the Main Window!", height=10).grid(row=0, column=1, padx=10, pady=10)
        
        login_button = tk.Button(self, text="Login", width=10, command=lambda: self.controller.show_frame(LoginWindow)).grid(row=1, column=1, padx=10, pady=2)
        quit_button = tk.Button(self, text="Quit", width=10, command=self.master.quit).grid(row=2, column=1, padx=10, pady=2)

class LoginWindow(Window):
    def __init__(self, master=None, controller=None):
        self.name = 'login'
        super().__init__(master, controller)

    def create_widgets(self):
        self.username_input = tk.StringVar()
        self.password_input = tk.StringVar()
        self.username_label = tk.Label(self, text="username: ").grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = tk.Entry(self, width=20, textvariable=self.username_input).grid(row=0, column=1, padx=10, pady=10)

        self.password_label = tk.Label(self, text="password: ").grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = tk.Entry(self, show='*', width=20, textvariable=self.password_input).grid(row=1, column=1, padx=10, pady=10)

        login_button = tk.Button(self, text="Login", width=10, command=self.login).grid(row=2, column=0, padx=10, pady=2)
        back_button = tk.Button(self, text="Back", width=10, command=lambda: self.controller.show_frame(MainWindow)).grid(row=2, column=1, padx=10, pady=2)


    def login(self):
        username = self.username_input.get()
        password = self.password_input.get()
        
        requests_maker = RequestsMaker()
        try:
            response = requests_maker.send_get_request('login', params={'username': username, 'password': password})
            if response:
                token = response.get('token')
                self.controller.set_login_token(token)
                self.controller.set_username(username)
                self.controller.show_frame(ApiWindow)
            else:
                tk.Label(self, text="Login failed! Please try again.", fg='red').grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        except requests.exceptions.RequestException as e:
            tk.Label(self, text=f"An error occurred! Please try again", fg='red').grid(row=3, column=0, columnspan=2, padx=10, pady=10)

class ApiWindow(Window):
    def __init__(self, master=None, controller=None):
        self.login_token = None
        self.username = None
        self.main_panel = None
        self.api_call_result_label = None
        self.name = 'api'
        super().__init__(master, controller)

    def set_login_token(self, token):
        self.login_token = token
    
    def set_username(self, username):
        self.username = username
    
    def show_token(self):
        if self.login_token:
            print(f"Current login token: {self.login_token}")
        else:
            print("No login token available.")

    def call_api(self, api_route):
        if not self.login_token:
            print("You need to log in first!")
            self.controller.show_frame(LoginWindow)
            return
        
        if not self.username:
            print("Username is not set!")
            self.controller.show_frame(LoginWindow)
            return
        
        headers = {'Authorization': f'Bearer {self.login_token}'}
        requests_maker = RequestsMaker()
        try:
            response = requests_maker.send_get_request(endpoint=api_route, params={'username' : self.username}, headers=headers)
            if response:
                self.api_call_result_label.config(text=f"API call result: {response['message']}", fg='green')
            else:
                self.api_call_result_label.config(text="Failed to retrieve data from API.", fg='red')
        except requests.exceptions.RequestException as e:
            self.api_call_result_label.config(text=f"An error occurred: {e}", fg='red')
    
    def create_widgets(self):
        self.main_panel = tk.Frame(self, bg='lightgray')

        header_panel = tk.Frame(self.main_panel)
        content_panel = tk.Frame(self.main_panel)
        navigation_panel = tk.Frame(self.main_panel)

        
        welcome_label = tk.Label(header_panel, text="Welcome to the API Test Window")

        api_content_panel = tk.Frame(content_panel)
        result_content_panel = tk.Frame(content_panel)

        result_label = tk.Label(result_content_panel, text="API Result Panel")
        result_panel = tk.Frame(result_content_panel, bg='white', height=100)
        self.api_call_result_label = tk.Label(result_panel, text="API call results will be displayed here.")

        api_label = tk.Label(api_content_panel, text="API Interaction Panel")
        api_panel = tk.Frame(api_content_panel, bg='white', height=100)

        
        back_button = tk.Button(navigation_panel, text="Back", width=10, command=lambda: self.controller.show_frame(MainWindow))
        quit_button = tk.Button(navigation_panel, text="Quit", width=10, command=self.master.quit)
        
        api_button = tk.Button(api_panel, text="Show Token", width=10, command=self.show_token)
        api_button1 = tk.Button(api_panel, text="Call API", width=10, command=lambda: self.call_api('api'))
        api_button2 = tk.Button(api_panel, text="Call API Admin", width=10, command=lambda: self.call_api('api/admin'))

        self.main_panel.pack(fill=tk.BOTH, expand=True)
        
        header_panel.grid(row=0, column=0, sticky="nesw", padx=10, pady=10)
        welcome_label.grid(row=0, column=0, padx=10, pady=10)
        
        #set up content panel
        content_panel.grid(row=1, column=0, sticky="nesw", padx=10, pady=10)
        result_content_panel.grid(row=0, column=0, sticky="nesw", padx=10, pady=10)
        api_content_panel.grid(row=0, column=1, sticky="nesw", padx=10, pady=10)

        result_label.grid(row=0, column=0, padx=10, pady=10)
        result_panel.grid(row=1, column=0, padx=10, pady=10)
        self.api_call_result_label.grid(row=0, column=0, padx=10, pady=10)

        api_label.grid(row=0, column=0, padx=10, pady=10)
        api_panel.grid(row=1, column=0, padx=10, pady=10)

        api_button.grid(row=0, column=0, padx=10, pady=10)
        api_button1.grid(row=1, column=0, padx=10, pady=10)
        api_button2.grid(row=2, column=0, padx=10, pady=10)

        #set up navigation panel
        navigation_panel.grid(row=2, column=0, sticky="nesw", padx=10, pady=10)
        back_button.grid(row=0, column=0, padx=10, pady=10)
        quit_button.grid(row=0, column=1, padx=10, pady=10)


