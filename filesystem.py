
import os
import stat
import datetime



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
