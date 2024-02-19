
import os
import stat
import datetime
import pathlib



class DirEntry():
    def __init__(self, dir_entry, parent=None, follow_symlinks=False):
        self.parent = parent
        self.name = dir_entry.name
        self.path = dir_entry if isinstance(dir_entry, pathlib.Path) else dir_entry.path
        self.is_dir = dir_entry.is_dir() and (follow_symlinks or not dir_entry.is_symlink())
        dstat = dir_entry.stat()
        self.size = dstat.st_size
        self.mode = dstat.st_mode
        self.mtime = dstat.st_mtime
        self.children = self._file_scan_r(follow_symlinks=follow_symlinks) if self.is_dir else None
        self.total_size = dstat.st_size
        if self.is_dir:
            self.total_size += sum(c.total_size for c in self.children)

    def get_mode_str(self):
        return stat.filemode(self.mode)

    def get_mtime_str(self):
        return datetime.datetime.fromtimestamp(self.mtime).strftime("%Y-%m-%d %H:%M:%S.%f")
    
    def _file_scan_r(self, follow_symlinks=False):
        children = []
        try:
            for fn in os.scandir(self.path):
                children.append(DirEntry(fn, self, follow_symlinks=follow_symlinks))
        except PermissionError as e:
            print(f"PermissionError: {e}")
        return sorted(children, key=lambda x: x.total_size, reverse=True)


    def get_info(self):
        return (
            self.size,
            self.total_size,
            self.parent.total_size if self.parent is not None else 0,
            self.get_mode_str(),
            self.get_mtime_str()
        )

    def get_tree_info_r(self):
        if not self.is_dir:
            return self.get_info()

        tree = {
            child.name: child.get_tree_info_r()
            for child in self.children
        }
        tree['.'] = self.get_info()
        return tree
