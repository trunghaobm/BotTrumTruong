import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import sys

def create_image():
    # Tạo một hình ảnh nhỏ để sử dụng làm biểu tượng
    image = Image.open("icon.png")

    return image

def on_exit(icon, item):
    icon.stop()
    sys.exit()

def setup(icon):
    icon.visible = True

def run_tray():
    icon = pystray.Icon("test_icon")
    icon.menu = pystray.Menu(
        item('Quit', on_exit)
    )
    icon.icon = create_image()
    icon.title = "Trùm Trường"
    icon.run(setup)
