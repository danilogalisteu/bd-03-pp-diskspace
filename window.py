
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

        self.frame1 = ttk.Frame(self.window)

        self.select_label = ttk.Label(self.frame1, text="Base folder:", width=10)
        self.select_label.grid(column=0, row=0, padx=10, pady=10)

        self.text_entry = tk.StringVar(self.frame1, value=str(self.base_path))
        self.select_entry = ttk.Entry(self.frame1, textvariable=self.text_entry, width=100, state='readonly')
        self.select_entry.grid(column=1, row=0, padx=10, pady=10)

        self.select_button = ttk.Button(self.frame1, text="Select base folder", width=16, command=self._select_folder)
        self.select_button.grid(column=2, row=0, padx=10, pady=10)
        self.select_button.focus()

        self.scan_button = ttk.Button(self.frame1, text="Scan folder", width=12, command=self._scan_folder)
        self.scan_button.grid(column=3, row=0, padx=10, pady=10)

        self.frame1.columnconfigure(1, weight=1)
        self.frame1.pack(fill="both", expand=True)

        self.frame2 = ttk.Frame(self.window)

        self.tree_view = ttk.Treeview(self.frame2, height=30, selectmode='none', columns=['size', 'total', 'percent', 'mode', 'mtime'])
        self.tree_view.pack(side='left', padx=[10, 0], pady=10)
        self.tree_view.column('#0', width=400, anchor='w')
        self.tree_view.heading('#0', text='Path')
        self.tree_view.column('size', minwidth=100, anchor='e')
        self.tree_view.heading('size', text='Size')
        self.tree_view.column('total', minwidth=100, anchor='e')
        self.tree_view.heading('total', text='Total size')
        self.tree_view.column('percent', minwidth=100, anchor='e')
        self.tree_view.heading('percent', text='% of parent size')
        self.tree_view.column('mode', minwidth=80, anchor='w')
        self.tree_view.heading('mode', text='Mode')
        self.tree_view.column('mtime', minwidth=200, anchor='w')
        self.tree_view.heading('mtime', text='Modified time')

        vsb = ttk.Scrollbar(self.frame2, orient="vertical", command=self.tree_view.yview)
        vsb.pack(side='right', fill='y', padx=[0, 10], pady=10)
        self.tree_view.configure(yscrollcommand=vsb.set)

        self.frame2.pack(fill="both", expand=True)
    
    def redraw(self):
        self.window.update_idletasks()
        self.window.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False

    def _select_folder(self):
        base_path = filedialog.askdirectory(
            parent=self.window,
            title="Select base path",
            initialdir=self.base_path,
            mustexist=True
        )
        if base_path:
            self.base_path = pathlib.Path(base_path)
            self.text_entry.set(str(self.base_path))

    def _scan_folder(self):
        self.dir_entry = DirEntry(self.base_path)
        self.tree_view.delete(*self.tree_view.get_children())
        self._fill_tree_view_r('', self.dir_entry)

    def _parse_entry_info(self, dir_entry):
        entry_size, total_size, parent_size, mode_str, mtime_str = dir_entry.get_info()
        percent_parent = total_size / parent_size if parent_size > 0 else 1
        return (
            f"{entry_size:,}",
            f"{total_size:,}",
            f"{percent_parent:.2%}",
            mode_str,
            mtime_str,
        )

    def _fill_tree_view_r(self, root_id, dir_entry):
        text_label = self.base_path if root_id == '' else dir_entry.name
        if dir_entry.is_dir:
            dir_node = self.tree_view.insert(root_id, 'end', text=text_label, open=True, values=self._parse_entry_info(dir_entry))
            for entry in dir_entry.children:
                self._fill_tree_view_r(dir_node, entry)
        else:
            file_node = self.tree_view.insert(root_id, 'end', text=text_label, open=False, values=self._parse_entry_info(dir_entry))
