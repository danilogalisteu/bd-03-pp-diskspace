
from tkinter import Tk



class Window():
    def __init__(self, width, height):
        self.window = Tk()
        self.window.title("boot.dev diskspace")
        self.window.geometry(f"{width}x{height}")
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        self.running = False
    
    def redraw(self):
        self.window.update_idletasks()
        self.window.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False
