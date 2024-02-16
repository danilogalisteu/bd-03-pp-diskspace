
import pathlib
import json

from filesystem import DirEntry



if __name__ == '__main__':
    initial_path = pathlib.Path.home()

    path_tree = DirEntry(initial_path).get_tree_info_r()

    print(json.dumps(path_tree, sort_keys=True, indent=4))
