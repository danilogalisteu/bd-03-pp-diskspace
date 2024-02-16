
import os
import stat
import pathlib
import datetime
import json



def file_scan_r(path, follow_symlinks=False):
    scan = {}
    for fn in os.scandir(path):
        fs = fn.stat()
        if fn.is_dir(follow_symlinks=follow_symlinks):
            scan[fn.name] = file_scan_r(path / fn.name)
            scan[fn.name]['.'] = [fs.st_size, stat.filemode(fs.st_mode), datetime.datetime.fromtimestamp(fs.st_mtime).strftime("%Y-%m-%d %H:%M:%S.%f")]
        elif fn.is_file(follow_symlinks=follow_symlinks):
            scan[fn.name] = [fs.st_size, stat.filemode(fs.st_mode), datetime.datetime.fromtimestamp(fs.st_mtime).strftime("%Y-%m-%d %H:%M:%S.%f")]
    return scan


if __name__ == '__main__':
    initial_path = pathlib.Path.home()
    path_tree = file_scan_r(initial_path)

    print(json.dumps(path_tree, sort_keys=True, indent=4))
