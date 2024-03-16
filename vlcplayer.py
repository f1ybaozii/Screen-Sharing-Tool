import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from tkinter import messagebox
import tkinter as tk
import numpy as np
import cv2
from PIL import ImageGrab, ImageTk , Image
import os, platform
os.environ['PYTHON_VLC_MODULE_PATH'] = "./VLC-3.0.20"
import vlc

class Player:
    '''
        args:设置 options
    '''
 
    def __init__(self, *args):
        if args:
            instance = vlc.Instance(*args)
            self.media = instance.media_player_new()
        else:
            self.media = vlc.MediaPlayer()
 
    # 设置待播放的url地址或本地文件路径，每次调用都会重新加载资源
    def set_uri(self, uri):
        self.media.set_mrl(uri)
    
    def start_recording(self,path):
        self.media.video_take_snapshot(0, path, 0, 0)
        
    # 播放 成功返回0，失败返回-1
    def play(self, path=None):
        if path:
            self.set_uri(path)
            return self.media.play()
        else:
            return self.media.play()
 
    # 暂停
    def pause(self):
        self.media.pause()
 
    # 恢复
    def resume(self):
        self.media.set_pause(0)
 
    # 停止
    def stop(self):
        self.media.stop()
 
    # 释放资源
    def release(self):
        return self.media.release()
 
    # 是否正在播放
    def is_playing(self):
        return self.media.is_playing()
 
    # 已播放时间，返回毫秒值
    def get_time(self):
        return self.media.get_time()
 
    # 拖动指定的毫秒值处播放。成功返回0，失败返回-1 (需要注意，只有当前多媒体格式或流媒体协议支持才会生效)
    def set_time(self, ms):
        return self.media.get_time()
 
    # 音视频总长度，返回毫秒值
    def get_length(self):
        return self.media.get_length()
 
    # 获取当前音量（0~100）
    def get_volume(self):
        return self.media.audio_get_volume()
 
    # 设置音量（0~100）
    def set_volume(self, volume):
        return self.media.audio_set_volume(volume)
 
    # 返回当前状态：正在播放；暂停中；其他
    def get_state(self):
        state = self.media.get_state()
        if state == vlc.State.Playing:
            return 1
        elif state == vlc.State.Paused:
            return 0
        else:
            return -1
 
    # 当前播放进度情况。返回0.0~1.0之间的浮点数
    def get_position(self):
        return self.media.get_position()
 
    # 拖动当前进度，传入0.0~1.0之间的浮点数(需要注意，只有当前多媒体格式或流媒体协议支持才会生效)
    def set_position(self, float_val):
        return self.media.set_position(float_val)
 
    # 获取当前文件播放速率
    def get_rate(self):
        return self.media.get_rate()
 
    # 设置播放速率（如：1.2，表示加速1.2倍播放）
    def set_rate(self, rate):
        return self.media.set_rate(rate)
 
    # 设置宽高比率（如"16:9","4:3"）
    def set_ratio(self, ratio):
        self.media.video_set_scale(0)  # 必须设置为0，否则无法修改屏幕宽高
        self.media.video_set_aspect_ratio(ratio)
 
    # 设置窗口句柄
    def set_window(self, wm_id):
        if platform.system() == 'Windows':
            self.media.set_hwnd(wm_id)
        else:
            self.media.set_xwindow(wm_id)
 
    # 注册监听器
    def add_callback(self, event_type, callback):
        self.media.event_manager().event_attach(event_type, callback)
 
    # 移除监听器
    def remove_callback(self, event_type, callback):
        self.media.event_manager().event_detach(event_type, callback)
 
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.player = Player()
        self.title("流媒体播放器")
        # self.create_video_view()
        # self.create_control_view()
        self._canvas = tk.Canvas(self, bg="black")
        self._canvas.pack()
        self.player.set_window(self._canvas.winfo_id())
        self.player.play("rtmp://127.0.0.1:1935/live/stream")
        self._canvas.pack()
 
    def create_video_view(self):
        self._canvas = tk.Canvas(self, bg="black")
        self._canvas.pack()
        self.player.set_window(self._canvas.winfo_id())
 
if __name__=="__main__":
    app=App()
    app.mainloop()
