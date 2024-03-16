
# import sql as sql
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from utils import *
from tkinter import messagebox
import tkinter as tk
import numpy as np
import cv2
from PIL import ImageGrab, ImageTk , Image
import threading 
import time
import chatserver,chatclient
import transmit

class identity:
    def __init__(self,account:str,is_server:bool):
        self.account=account
        self.is_server=is_server

id=None 


class login_window(tk.Frame):

    def __init__(self,parent=None):
        super().__init__(parent)
        self.parent=parent
        self.is_server=False
        parent.title("login")
        parent.state('normal')
        parent.geometry('380x170+800+600')
        parent.resizable(False,False)
        
        # login_window.iconbitmap(".")
        style=ttk.Style()
        
        ttk.Label(self, text="Account",style='primary').grid(row=0, column=3, padx=5, pady=5)
       
        self.account=ttk.Entry(self,style='primary')
        self.account.grid(row=0, column=4, padx=20, pady=5)
       
        ttk.Label(self, text="Password",style='primary').grid(row=1, column=3, padx=5, pady=5)
        self.password=ttk.Entry(self,style='primary')
        self.password.grid(row=1, column=4, padx=20, pady=5)

        self.check_server=ttk.Checkbutton(self,text='Login as a Client',style='primary-round-toggle',command=self.confirm_server)
        self.check_server.grid(row=2, column=4, padx=5, pady=5)

        ttk.Button(self, text='Register',width=15,command=self.register).grid(row=3, column=3, padx=20, pady=5,sticky=ttk.W+ttk.E)
        ttk.Button(self, text='Login',width=15,command=self.login).grid(row=3, column=4, padx=20, pady=5,sticky=ttk.W+ttk.E)
 
        self.grid()

    def login(self):
        password_encrypted=encrypt(self.password.get())
        if sql.login(self.account.get(),password_encrypted):
            self.display_messagebox(flag='login_success')
            global id
            id=identity(self.account.get(),self.is_server)
            self.grid_remove()
            mainwindow(self.parent)
        else:
            self.display_messagebox(flag='login_failed')
        
      
    def display_messagebox(self,flag:str=None):
        if flag=='login_failed':
            messagebox.showerror(title="Login Failed",message=f"{self.account.get()} failed to login", parent=self)
        elif flag=='login_success':
            messagebox.showinfo(title="Login Success",message=f"{self.account.get()} successfully login", parent=self)
        elif flag=='register_exist':
            messagebox.showerror(title="Register Failed",message=f"{self.account.get()} has already existed.", parent=self)
        elif flag=='register_failed':
            messagebox.showerror(title="Register Failed",message=f"{self.account.get()} failed to register.", parent=self)
        elif flag=='register_success':
            messagebox.showinfo(title="Register Success",message=f"{self.account.get()} successfully register.", parent=self)

    def register(self):
        password_encrypted=encrypt(self.password.get())
        if sql.login(self.account.get(),password_encrypted):
            self.display_messagebox(flag='register_exist')
        else:
            if sql.register(self.account.get(),password_encrypted):
                self.display_messagebox(flag='register_success')
            else:
                self.display_messagebox(flag='register_failed')

    def confirm_server(self):
        if self.check_server.instate(['selected']):
            self.is_server=True
            self.check_server.configure(text='Login as a Server')

        elif self.check_server.instate(['!selected']):
            self.is_server=False
            self.check_server.configure(text='Login as a Client')
        
    
   
    
class mainwindow(tk.Frame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent=parent


        parent.title('Screen Sharing Tool')
        self.chatserver=chatserver.ChatServer()

        parent.geometry('2000x960')
        parent.resizable(0,0)

        self.screen_width = parent.winfo_screenwidth()
        self.screen_height = parent.winfo_screenheight()
        self.create_chat_window()
        self.create_vlc()
        self.create_menu()

        self.chatclient=chatclient.ChatClient(self)
        

        self.pack(fill='both', expand=True)

    def on_message_received(self,account:str,message:str):
        # 将消息添加到Text组件中
        self.chat_log.configure(state='normal')
        self.chat_log.insert('end',f'{account}:{message}' + '\n')
        self.chat_log.configure(state='disabled')

    def send_message(self):
        # 获取Entry组件中的文本
        message = self.message_entry.get()
        self.on_message_received('You',message)
        # 清空Entry组件
        self.message_entry.delete(0, 'end')

    def create_vlc(self,url:str="rtmp://127.0.0.1:1935/live/stream"):
        print("create_vlc")
        self.player=vlcplayer.Player()
        self.canvas=tk.Canvas(bg='black',width=1600,height=960)
        # 使用place布局管理器来布局Canvas组件
        self.canvas.place(x=0, y=0)
        self.player.set_window(self.canvas.winfo_id())
        self.player.play(url)

    def create_chat_window(self):
        # 创建一个Scrollbar组件
        self.scrollbar = tk.Scrollbar(self)
        # 使用place布局管理器来布局Scrollbar组件
        self.scrollbar.place(x=1980, y=0, width=20, height=720)

        # 创建一个Text组件来显示历史聊天记录，并与Scrollbar组件关联
        self.chat_log = tk.Text(self, state='disabled', yscrollcommand=self.scrollbar.set)
        # 使用place布局管理器来布局Text组件
        self.chat_log.place(x=1600, y=0, width=380, height=720)

        # 配置Scrollbar组件，使其可以滚动Text组件
        self.scrollbar.config(command=self.chat_log.yview)

        # 创建一个Entry组件来输入消息
        self.message_entry = tk.Entry(self)
        # 使用place布局管理器来布局Entry组件
        self.message_entry.place(x=1600, y=720, width=300, height=240)

        # 创建一个Button组件来提交消息
        self.submit_button = tk.Button(self, text="Submit", command=self.send_message)
        # 使用place布局管理器来布局Button组件
        self.submit_button.place(x=1900, y=720, width=100, height=240)
    def quit_app(self):
        self.parent.quit()

    def create_menu(self):
        menubar = tk.Menu(self.parent)


        tools = tk.Menu(menubar, tearoff=0)
        tools.add_command(label='Connection',command=self.add_ip_window)
        tools.add_command(label='Exit',command=self.quit_app)
        tools.add_command(label='Full screen _F11',command=lambda: self.parent.attributes('-fullscreen', not self.parent.attributes('-fullscreen')))
        
        self.parent.bind('<F11>', lambda event: self.parent.attributes('-fullscreen', not self.parent.attributes('-fullscreen')))
        menubar.add_cascade(label='Tools', menu=tools)

        self.parent.config(menu=menubar)

    def set_IP(self,ip:str):
        self.ip=ip

    def add_ip_window(self):
    # 创建一个新的窗口
        new_window = tk.Toplevel(self.parent)

        # 创建IP地址的标签和输入框
        ip_label = tk.Label(new_window, text="Input URL")
        ip_label.pack(padx=10, pady=5)
        ip_entry = tk.Entry(new_window)
        ip_entry.pack(padx=10, pady=5)

        # 创建提交按钮，点击时获取输入框的值并调用set_IP方法
        submit_button = tk.Button(new_window, text="Submit", command=lambda:self.player.play(ip_entry.get()))
        submit_button.pack(padx=10, pady=5)
        new_window.update()

        # 计算屏幕的中心位置
        screen_width = new_window.winfo_screenwidth()
        screen_height = new_window.winfo_screenheight()

        # 计算窗口的大小
        window_width = new_window.winfo_width()
        window_height = new_window.winfo_height()

        # 计算窗口的位置
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        # 设置窗口的位置
        new_window.geometry("+{}+{}".format(position_right, position_top))

    def login_exit(self):
        self.parent.config(menu=None)
        print(self.parent)
        self.grid_remove()  # 隐藏mainwindow
        global id 
        id = None
        login_window(self.parent)


    def pause(self):
        pass

if __name__ == "__main__":
    sql.connect_db()
    sql.init_db()
    root=tk.Tk()
    login_window(root)
    root.mainloop()