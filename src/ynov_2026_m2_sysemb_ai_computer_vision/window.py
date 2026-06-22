from tkinter import Tk

import tkinter as tk, threading
import imageio

from PIL import Image, ImageTk

class Window(Tk):
    def __init__(self):
        Tk.__init__(self)
        video_name = "circulation.mp4"
        video = imageio.get_reader(video_name)
        video_frame_renderer_label = tk.Label(self)
        video_frame_renderer_label.pack()
        thread = threading.Thread(target=self.stream, args=(video, video_frame_renderer_label))
        thread.daemon = True
        thread.start()
        self.mainloop()

    def stream(self, video, video_frame_renderer_label):
        for image in video.iter_data():
            frame_image = ImageTk.PhotoImage(Image.fromarray(image))
            video_frame_renderer_label.config(image=frame_image)
            video_frame_renderer_label.image = frame_image