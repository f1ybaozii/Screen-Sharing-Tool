import subprocess as sp
from PIL import ImageGrab
import cv2
import numpy as np
def Transmit():
    command=['ffmpeg',
            '-y',
            '-f', 'rawvideo',
            '-vcodec','rawvideo',
            '-pix_fmt', 'bgr24',
            '-s', '2560x1600',
            '-i', '-',
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-preset', 'ultrafast',
            '-f', 'flv', 
            'rtmp://127.0.0.1:1935/live/stream']

    p=sp.Popen(command, stdin=sp.PIPE)

    while True:
        image=ImageGrab.grab()
        frame=cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        p.stdin.write(frame.tobytes())
        
if __name__ == "__main__":
    Transmit()