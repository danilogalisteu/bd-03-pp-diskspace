
import pathlib

from window import Window



if __name__ == '__main__':
    initial_path = pathlib.Path.home()

    win = Window(1200, 900)

    win.wait_for_close()
