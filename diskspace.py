
import pathlib
import json

from filesystem import file_scan_r



if __name__ == '__main__':
    initial_path = pathlib.Path.home()
    path_tree = file_scan_r(initial_path)

    print(json.dumps(path_tree, sort_keys=True, indent=4))
