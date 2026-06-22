from tkinter import HORIZONTAL, Tk

import tkinter as tk, threading
import imageio

from PIL import Image, ImageTk

class Window(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.min_red_threshold_value = 0
        self.max_red_threshold_value = 255

        self.min_green_threshold_value = 0
        self.max_green_threshold_value = 255

        self.min_blue_threshold_value = 0
        self.max_blue_threshold_value = 255

        self.zoom = 1

        # MIN RED
        self.min_red_threshold_label = tk.Label(self, text="Red (0, 255) : ")
        self.min_red_threshold_label.pack()
        self.min_red_threshold_slider = tk.Scale(
                self, 
                from_=0, 
                to=255, 
                orient=tk.HORIZONTAL, 
                length=200,
                resolution=1,
                command=self.update_min_red_threshold_slider
        )
        self.min_red_threshold_slider.set(self.min_red_threshold_value)
        self.min_red_threshold_slider.pack()

        # MAX RED
        self.max_red_threshold_label = tk.Label(self, text="Red (0, 255) : ")
        self.max_red_threshold_label.pack()
        self.max_red_threshold_slider = tk.Scale(
                self, 
                from_=0, 
                to=255, 
                orient=tk.HORIZONTAL, 
                length=200,
                resolution=1,
                command=self.update_max_red_threshold_slider
        )
        self.max_red_threshold_slider.set(self.max_red_threshold_value)
        self.max_red_threshold_slider.pack()


        # MIN GREEN
        self.min_green_threshold_label = tk.Label(self, text="Green (0, 255) : ")
        self.min_green_threshold_label.pack()
        self.min_green_threshold_slider = tk.Scale(
                self, 
                from_=0, 
                to=255, 
                orient=tk.HORIZONTAL, 
                length=200,
                resolution=1,
                command=self.update_min_green_threshold_slider
        )
        self.min_green_threshold_slider.set(self.min_green_threshold_value)
        self.min_green_threshold_slider.pack()

        # MAX GREEN
        self.max_green_threshold_label = tk.Label(self, text="Green (0, 255) : ")
        self.max_green_threshold_label.pack()
        self.max_green_threshold_slider = tk.Scale(
                self, 
                from_=0, 
                to=255, 
                orient=tk.HORIZONTAL, 
                length=200,
                resolution=1,
                command=self.update_max_green_threshold_slider
        )
        self.max_green_threshold_slider.set(self.max_green_threshold_value)
        self.max_green_threshold_slider.pack()


        # MIN BLUE
        self.min_blue_threshold_label = tk.Label(self, text="Blue (0, 255) : ")
        self.min_blue_threshold_label.pack()
        self.min_blue_threshold_slider = tk.Scale(
                self, 
                from_=0, 
                to=255, 
                orient=tk.HORIZONTAL, 
                length=200,
                resolution=1,
                command=self.update_min_blue_threshold_slider
        )
        self.min_blue_threshold_slider.set(self.min_blue_threshold_value)
        self.min_blue_threshold_slider.pack()

        # MAX BLUE
        self.max_blue_threshold_label = tk.Label(self, text="Blue (0, 255) : ")
        self.max_blue_threshold_label.pack()
        self.max_blue_threshold_slider = tk.Scale(
                self, 
                from_=0, 
                to=255, 
                orient=tk.HORIZONTAL, 
                length=200,
                resolution=1,
                command=self.update_max_blue_threshold_slider
        )
        self.max_blue_threshold_slider.set(self.max_blue_threshold_value)
        self.max_blue_threshold_slider.pack()

        video_name = "circulation.mp4"
        video = imageio.get_reader(video_name)
        video_frame_renderer_label = tk.Label(self)
        video_frame_renderer_label.pack()
        thread = threading.Thread(target=self.stream, args=(video, video_frame_renderer_label))
        thread.daemon = True
        thread.start()
        self.mainloop()

    def _adjust_slider_limits(self, min_slider, max_slider):
        min_value = min_slider.get()
        max_value = max_slider.get()
        
        max_slider.config(from_=min_value)
        min_slider.config(to=max_value)
        
        if min_value > max_value:
            min_slider.set(max_value)

    # Tes fonctions de callback deviennent super légères :
    def adjust_red_limits(self):
        self._adjust_slider_limits(self.min_red_threshold_slider, self.max_red_threshold_slider)

    def adjust_green_limits(self):
        self._adjust_slider_limits(self.min_green_threshold_slider, self.max_green_threshold_slider)

    def adjust_blue_limits(self):
        self._adjust_slider_limits(self.min_blue_threshold_slider, self.max_blue_threshold_slider)

    def stream(self, video, video_frame_renderer_label):
        for image in video.iter_data():
            frame_image = ImageTk.PhotoImage(Image.fromarray(image))
            video_frame_renderer_label.config(image=frame_image)
            video_frame_renderer_label.image = frame_image
    
    def update_min_red_threshold_slider(self, value):
        self.min_red_threshold_value = int(value)
        self.adjust_red_limits()
    
    def update_max_red_threshold_slider(self, value):
        self.max_red_threshold_value = int(value)
        self.adjust_red_limits()
    
    def update_min_green_threshold_slider(self, value):
        self.min_green_threshold_value = int(value)
        self.adjust_green_limits()
    
    def update_max_green_threshold_slider(self, value):
        self.max_green_threshold_value = int(value)
        self.adjust_green_limits()

    def update_min_blue_threshold_slider(self, value):
        self.min_blue_threshold_value = int(value)
        self.adjust_blue_limits()
    
    def update_max_blue_threshold_slider(self, value):
        self.max_blue_threshold_value = int(value)
        self.adjust_blue_limits()