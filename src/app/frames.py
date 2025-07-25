import tkinter as tk
import requests
from requests_maker import RequestsMaker

class Window(tk.Frame):
    def __init__(self, master=None, controller=None):
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.login_token = None
        self.headers = None
        self.create_widgets()
        self.pack_widgets()

    def create_widgets(self):
        pass

    def pack_widgets(self):
        pass

    def refresh(self):
        pass
    
    def set_login_token(self, token):
        self.login_token = token


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
        self.result_label = None
        self.requests_maker = RequestsMaker()

        self.password_entry = None
        super().__init__(master, controller)

    def create_widgets(self):
        main_panel = tk.Frame(self)

        input_panel = tk.Frame(main_panel)
        result_panel = tk.Frame(main_panel, height=100)
        navigation_panel = tk.Frame(main_panel)

        username_panel = tk.Frame(input_panel)
        password_panel = tk.Frame(input_panel)

        self.username_input = tk.StringVar()
        self.password_input = tk.StringVar()

        username_label = tk.Label(username_panel, text="username: ")
        username_entry = tk.Entry(username_panel, width=20, textvariable=self.username_input)

        password_label = tk.Label(password_panel, text="password: ")
        self.password_entry = tk.Entry(password_panel, show='*', width=20, textvariable=self.password_input)

        self.result_label = tk.Label(result_panel)

        login_button = tk.Button(navigation_panel, text="Login", width=10, command=self.login)
        back_button = tk.Button(navigation_panel, text="Back", width=10, command=lambda: self.controller.show_frame(MainWindow))
        register_button = tk.Button(navigation_panel, text="Register", width=10, command=self.register)

        # set up main panel
        main_panel.pack(fill=tk.BOTH, expand=True)
        input_panel.grid(row=0, column=0, sticky="nesw", padx=10, pady=10)
        username_panel.grid(row=0, column=0, sticky="nesw", padx=10, pady=10)
        username_label.grid(row=0, column=0, padx=10, pady=10)
        username_entry.grid(row=0, column=1, padx=10, pady=10)

        password_panel.grid(row=1, column=0, sticky="nesw", padx=10, pady=10)
        password_label.grid(row=0, column=0, padx=10, pady=10)
        self.password_entry.grid(row=0, column=1, padx=10, pady=10)

        result_panel.grid(row=1, column=0, sticky="nesw", padx=10, pady=10)
        self.result_label.grid(row=0, column=0, padx=10, pady=10)

        navigation_panel.grid(row=2, column=0, sticky="nesw", padx=10, pady=10)
        login_button.grid(row=0, column=0, padx=5, pady=10)
        register_button.grid(row=0, column=1, padx=5, pady=10)
        back_button.grid(row=0, column=2, padx=5, pady=10)

        self.refresh()

    def refresh(self):
        self.result_label.config(text="")
        self.password_entry.delete(0, tk.END)

    def register(self):
        username = self.username_input.get()
        password = self.password_input.get()

        if (not username or not password):
            self.result_label.config(text=f"Missing username or password!", fg='red')
            return
        try: 
            headers = {"Content-Type" : "application/json"}
            status, response = self.requests_maker.send_post_request_json(endpoint='register', json={"username" : username, "password" : password}, headers=headers)
            if status == 201:
                message = response.get('message')
                self.result_label.config(text=message, fg='green')
            else:
                self.result_label.config(text=f"Register failed! {response.get('error_message')}", fg='red')
        except requests.exceptions.RequestException as e:
            self.result_label.config(text=f"An error occurred: {e}", fg='red')
        
    def login(self):
        username = self.username_input.get()
        password = self.password_input.get()
        
        try:
            headers = {"Content-Type" : "application/json", "username": username, "password": password}
            status, response = self.requests_maker.send_get_request('login', headers=headers)
            if status == 200:
                token = response.get('token')
                self.controller.set_login_token(token)
                self.controller.set_username(username)
                self.controller.show_frame(ApiWindow)
            else:
                self.result_label.config(text=f"Login failed! {response.get('error_message')}", fg='red')
        except requests.exceptions.RequestException as e:
            self.result_label.config(text=f"An error occurred: {e}", fg='red')

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
            self.api_call_result_label.config(text=f"Current login token:{self.login_token}", fg='green')
        else:
            self.api_call_result_label.config(text=f"No login token available!", fg='red')

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
            status, response = requests_maker.send_get_request(endpoint=api_route, params={'username' : self.username}, headers=headers)
            if status == 200:
                self.api_call_result_label.config(text=f"API call result: {response['message']}", fg='green')
            else:
                self.api_call_result_label.config(text=f"Failed to retrieve data from API: {response['error_message']}", fg='red')
        except requests.exceptions.RequestException as e:
            self.api_call_result_label.config(text=f"An error occurred: {e}", fg='red')
    
    def refresh(self):
        if self.api_call_result_label:
            self.api_call_result_label.config(text="API call results will be displayed here.", fg='black')
    
    def create_widgets(self):
        self.main_panel = tk.Frame(self, bg='white')

        header_panel = tk.Frame(self.main_panel)
        content_panel = tk.Frame(self.main_panel)
        navigation_panel = tk.Frame(self.main_panel)

        
        welcome_label = tk.Label(header_panel, text="Welcome to the API Test Window")

        api_content_panel = tk.Frame(content_panel)
        result_content_panel = tk.Frame(content_panel)

        result_label = tk.Label(result_content_panel, text="API Result Panel")
        result_panel = tk.Frame(result_content_panel, bg='white', height=100)
        self.api_call_result_label = tk.Label(result_panel, text="API call results will be displayed here.", fg='black', wraplength=200, justify='left')

        api_label = tk.Label(api_content_panel, text="API Interaction Panel")
        api_panel = tk.Frame(api_content_panel, bg='white', height=100)

        
        back_button = tk.Button(navigation_panel, text="Back", width=10, command=lambda: self.controller.show_frame(LoginWindow))
        quit_button = tk.Button(navigation_panel, text="Quit", width=10, command=self.master.quit)
        
        request_button = tk.Button(api_panel, text="Request Access", width=10, command=lambda: self.controller.show_frame(RequestAccessWindow))
        inbox_button = tk.Button(api_panel, text="Inbox", width=10, command=lambda: self.controller.show_frame(InboxWindow))
        api_button1 = tk.Button(api_panel, text="Call API", width=10, command=lambda: self.call_api('api'))
        api_button2 = tk.Button(api_panel, text="Call API Admin", width=10, command=lambda: self.call_api('admin/api'))

        #set up main panel
        #pack the biggest frame, then add and grid the child, using grid to set the layout. Start from the parent to the child
        #handle layour more easily
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

        api_button1.grid(row=0, column=0, padx=10, pady=10)
        api_button2.grid(row=1, column=0, padx=10, pady=10)
        request_button.grid(row=2, column=0, padx=10, pady=10)
        inbox_button.grid(row=3, column=0, padx=10, pady=10)

        #set up navigation panel
        navigation_panel.grid(row=2, column=0, sticky="nesw", padx=10, pady=10)
        back_button.grid(row=0, column=0, padx=10, pady=10)
        quit_button.grid(row=0, column=1, padx=10, pady=10)

class RequestAccessWindow(Window):
    def __init__(self, master=None, controller=None):
        self.name = 'request-access'
        self.approver_input = None
        self.role_input = None
        self.result_label = None
        self.login_token = None
        self.approver_entry = None
        self.approver_panel = None
        super().__init__(master, controller)
    
    def fetch_valid_approvers(self):
        approvers = []

        if not self.login_token: #or expired
            print("You need to log in first!")
            return ['emptry']

        headers = {'Authorization': f'Bearer {self.login_token}'}
        self.pending_requests = []
        request_maker = RequestsMaker()
        try:
            status, response = request_maker.send_get_request(endpoint='api/fetch-approvers', headers=headers)
            if status == 200:
                for item in response['message']:
                    approvers.append(item)
                self.result_label.config(text=f"API call success", fg='green')
            else:
                self.result_label.config(text=f"Failed to retrieve data from API: {response['error_message']}", fg='red')
        except requests.exceptions.RequestException as e:
            self.result_label.config(text=f"An error occurred: {e}", fg='red')
        
        return approvers

    def create_widgets(self):
        self.main_panel = tk.Frame(self)

        header_panel = tk.Frame(self.main_panel)
        input_panel = tk.Frame(self.main_panel)
        result_panel = tk.Frame(self.main_panel)
        navigation_panel = tk.Frame(self.main_panel)

        header_label = tk.Label(header_panel, text="Request Access")

        self.approver_panel = tk.Frame(input_panel)
        role_panel = tk.Frame(input_panel)

        self.approver_input = tk.StringVar()
        self.role_input = tk.StringVar()

        approver_label = tk.Label(self.approver_panel, text="Approver: ", width=10)
        #approver_entry = tk.Entry(approver_panel, width=20, textvariable=self.approver_input)
        self.approver_entry = tk.OptionMenu(self.approver_panel, self.approver_input, ['empty'])

        role_label = tk.Label(role_panel, text="Role: ", width=10)
        #role_entry = tk.Entry(role_panel, width=20, textvariable=self.role_input)
        role_entry = tk.OptionMenu(role_panel, self.role_input, *["admin", "user", "editor"])

        self.result_label = tk.Label(result_panel)

        send_request_button = tk.Button(navigation_panel, text="Send Request", width=10, command=self.send)
        back_button = tk.Button(navigation_panel, text="Back", width=10, command=lambda: self.controller.show_frame(ApiWindow))

        #set up main panel
        self.main_panel.pack(fill=tk.BOTH, expand=True)

        header_panel.grid(row = 0, column = 0, padx = 10, pady = 10)
        header_label.grid(row = 0, column = 0, padx = 10, pady = 10)

        input_panel.grid(row=1, column=0, padx=10, pady=10)

        self.approver_panel.grid(row=0, column=0, padx=10, pady=10)
        approver_label.grid(row=0, column=0, padx=10, pady=10)
        self.approver_entry.grid(row=0, column=1, padx=10, pady=10)

        role_panel.grid(row=1, column=0, padx=10, pady=10)
        role_label.grid(row=0, column=0, padx=10, pady=10)
        role_entry.grid(row=0, column=1, padx=10, pady=10)

        result_panel.grid(row=2, column=0, padx=10, pady=10)
        self.result_label.grid(row=0, column=0)

        navigation_panel.grid(row=3, column=0, padx=10, pady=10)
        send_request_button.grid(row=0, column=0, padx=10, pady=10)
        back_button.grid(row=0, column=1, padx=10, pady=10)
        
    def set_login_token(self, token):
        self.login_token = token

    def refresh(self):
        self.result_label.config(text="")
        approver_list = self.fetch_valid_approvers()
        menu = self.approver_entry["menu"]
        menu.delete(0, tk.END)
        for item in approver_list:
            text = dict(item)['approver']
            menu.add_command(label=text, command=lambda value=text: self.approver_input.set(value))
        self.approver_input.set("<Select approver>")
        self.role_input.set("<Select role>")

    def send(self):
        if not self.login_token:
            print("You need to log in first!")
            self.controller.show_frame(LoginWindow)
            return
        
        approver = self.approver_input.get()
        role = self.role_input.get()

        requests_maker = RequestsMaker()

        data = {
            "token" : self.login_token,
            "approver" : approver,
            "request_role" : role 
        }

        try:
            status, response = requests_maker.send_post_request_json(endpoint='api/request-access', json=data)
            if status == 201:
                self.result_label.config(text=f"API call result: {response['message']}", fg='green')
            else:
                self.result_label.config(text=f"Failed to retrieve data from API: {response['error_message']}", fg='red')
        except requests.exceptions.RequestException as e:
            self.result_label.config(text=f"An error occurred: {e}", fg='red')

class InboxItem(tk.Button):
    def __init__(self):
        super().__init__()
    

class InboxWindow(Window):
    def __init__(self, master=None, controller = None):
        self.content_panel = None
        self.pending_requests = []
        self.inbox_items = []
        self.result_label = None
        super().__init__(master, controller)
    
    def fetch_pending_requests(self):
        if not self.login_token: #or expired
            print("You need to log in first!")
            self.controller.show_frame(LoginWindow)
            return

        headers = {'Authorization': f'Bearer {self.login_token}'}
        self.pending_requests = []
        request_maker = RequestsMaker()
        try:
            status, response = request_maker.send_get_request(endpoint='api/pending-request', headers=headers)
            if status == 200:
                for item in response['message']:
                    self.pending_requests.append(item)
                self.result_label.config(text=f"API call success", fg='green')
            else:
                self.result_label.config(text=f"Failed to retrieve data from API: {response['error_message']}", fg='red')
        except requests.exceptions.RequestException as e:
            self.result_label.config(text=f"An error occurred: {e}", fg='red')

    def on_inbox_item_click(self):
        pass

    def on_reject(self, request):
        self.result_label.config(text=f"Not yet implemented!", fg='black')

    def on_approve(self, request):
        if not self.login_token: #or expired
            print("You need to log in first!")
            self.controller.show_frame(LoginWindow)
            return

        headers = {'Authorization': f'Bearer {self.login_token}'}
        request_maker = RequestsMaker()
        try:
            status, response = request_maker.send_post_request_json(endpoint='admin/approve-request', json=request, headers=headers)
            if status == 201:
                self.refresh()
                self.result_label.config(text=f"{response['message']}", fg='green')
            else:
                self.result_label.config(text=f"Failed to approve request id {request['_id']}. Error: {response['error_message']}", fg='red')
        except requests.exceptions.RequestException as e:
            self.result_label.config(text=f"An error occurred: {e}", fg='red')

    def refresh(self):
        self.result_label.config(text="")
        for widget in self.content_panel.winfo_children():
            widget.destroy()
        self.fetch_pending_requests()
        id = 0
        for request in self.pending_requests:
            mail_panel = tk.Frame(self.content_panel)
            mail_button = tk.Button(mail_panel, text=request['_id'], width=20, command=self.on_inbox_item_click)
            approve_button = tk.Button(mail_panel, text='Approve', command=lambda: self.on_approve(request))
            reject_button = tk.Button(mail_panel, text='Reject', command=lambda: self.on_reject(request))

            mail_panel.pack(expand=True, fill=tk.X)
            mail_button.grid(row=0, column=0)
            approve_button.grid(row=0, column=1)
            reject_button.grid(row=0, column=2)
            id+=1
            
    def create_widgets(self):
        self.main_panel = tk.Frame(self)

        header_panel = tk.Frame(self.main_panel)
        self.content_panel = tk.Frame(self.main_panel, bg='white', height=200)
        navigation_panel = tk.Frame(self.main_panel)
        result_panel = tk.Frame(self.main_panel)
        
        welcome_label = tk.Label(header_panel, text="Pending Requests")
        self.result_label = tk.Label(result_panel, text="", fg='black')
       
        back_button = tk.Button(navigation_panel, text="Back", width=10, command=lambda: self.controller.show_frame(ApiWindow))

        #set up main panel
        #pack the biggest frame, then add and grid the child, using grid to set the layout. Start from the parent to the child
        #handle layour more easily
        self.main_panel.pack(fill=tk.BOTH, expand=True)
        
        header_panel.grid(row=0, column=0, sticky="nesw", padx=10, pady=10)
        welcome_label.grid(row=0, column=0, padx=10, pady=10)
        
        #set up content panel
        self.content_panel.grid(row=1, column=0, sticky="nesw", padx=10, pady=10)

        result_panel.grid(row=2, column=0, sticky="nesw", padx=10, pady=10)
        self.result_label.grid(row=0, column=0, sticky="nesw", padx=10, pady=10)
        #set up navigation panel
        navigation_panel.grid(row=3, column=0, sticky="nesw", padx=10, pady=10)
        back_button.grid(row=0, column=0, padx=10, pady=10)
    

    