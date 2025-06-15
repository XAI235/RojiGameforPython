import cv2
from ffpyplayer.player import MediaPlayer
import time
import numpy as np
from SystemMain.BaseClass import basescene


class MoivePlayer (basescene):
    ff_opts = {
        "out_fmt": "bgr24",
        }

    def __init__(self):
        self.videoPath : str = ""
        self.frame = ""
        self.Player = None

    def initialize(self):
        self.Player = MediaPlayer(self.video_path, ff_opts=MoivePlayer.ff_opts)
        return
    
    def update(self):
        return

    def draw(self):
        return

"""
ff_opts = {
    "out_fmt": "bgr24",
}
player = MediaPlayer(
    video_path,
    ff_opts=ff_opts,
)

window_name = "Video"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

while 1:
    frame, val = player.get_frame()

    img, t = frame

    arr = np.frombuffer(img.to_bytearray()[0], np.uint8)
    arr = arr.reshape((720, 1280, 3))
    cv2.imshow(window_name, arr)
    time.sleep(val)

cv2.destroyAllWindows()
"""