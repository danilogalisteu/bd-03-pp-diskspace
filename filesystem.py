
import os
import stat
import datetime
import pathlib



class DirEntry():
    def __init__(self, dir_entry, follow_symlinks=False):
        self.name = dir_entry.name
        self.path = dir_entry if isinstance(dir_entry, pathlib.Path) else dir_entry.path
        self.is_dir = dir_entry.is_dir() and (follow_symlinks or not dir_entry.is_symlink())
        dstat = dir_entry.stat()
        self.size = dstat.st_size
        self.mode = dstat.st_mode
        self.mtime = dstat.st_mtime
        self.children = self._file_scan_r(follow_symlinks=follow_symlinks) if self.is_dir else None

    def get_mode_str(self):
        return stat.filemode(self.mode)

    def get_mtime_str(self):
        return datetime.datetime.fromtimestamp(self.mtime).strftime("%Y-%m-%d %H:%M:%S.%f")
    
    def _file_scan_r(self, follow_symlinks=False):
        return [
            DirEntry(fn, follow_symlinks=follow_symlinks)
            for fn in os.scandir(self.path)
        ]

    def get_info(self):
        return self.size, self.get_mode_str(), self.get_mtime_str()

    def get_tree_info_r(self):
        if not self.is_dir:
            return self.get_info()

        tree = {
            child.name: child.get_tree_info_r()
            for child in self.children
        }
        tree['.'] = self.get_info()
        return tree
