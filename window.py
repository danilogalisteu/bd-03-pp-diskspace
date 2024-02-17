
import pathlib

import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk

from filesystem import DirEntry



class Window():
    def __init__(self, width, height):
        self.running = False
        self.base_path = pathlib.Path.home()
        self.dir_entry = None

        self.window = tk.Tk()
        self.window.title("boot.dev diskspace")
        # self.window.geometry(f"{width}x{height}")
        self.window.protocol("WM_DELETE_WINDOW", self.close)

        self.frame = ttk.Frame(self.window)

        self.select_label = ttk.Label(self.frame, text="Base folder:", width=10)
        self.select_label.grid(column=0, row=0, padx=5, pady=10)

        self.text_entry = tk.StringVar(self.frame, value=str(self.base_path))
        self.select_entry = ttk.Entry(self.frame, textvariable=self.text_entry, width=50, state='readonly')
        self.select_entry.grid(column=1, row=0, padx=5, pady=10)

        self.select_button = ttk.Button(self.frame, text="Select base folder", width=16)
        self.select_button.grid(column=2, row=0, padx=5, pady=10)
        self.select_button.focus()

        self.scan_button = ttk.Button(self.frame, text="Scan folder", width=12)
        self.scan_button.grid(column=3, row=0, padx=5, pady=10)

        self.tree_view = ttk.Treeview(self.frame, height=20, selectmode='none', columns=['Size', 'Mode', 'Modified time'])
        self.tree_view.grid(column=0, row=1, columnspan=4, padx=10, pady=10)

        self.frame.columnconfigure(3, weight=1)
        self.frame.rowconfigure(1, weight=1)

        self.frame.pack(fill="both", expand=True)
    
    def redraw(self):
        self.window.update_idletasks()
        self.window.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False
