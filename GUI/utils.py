import sys
sys.path.append('F:\\SJTU\\2023-2\\项目管理与项目设计\\小作业')
import sql

import os
os.environ['PYTHON_VLC_MODULE_PATH'] = "./vlc-3.0.20"
import vlc

import hashlib

def encrypt(password:str):
    return hashlib.md5(password.encode('utf-8')).hexdigest()

import vlcplayer
from screeninfo import get_monitors
def get_screenifo_solution():
    monitor=get_monitors()[0]
    return monitor.width,monitor.height
