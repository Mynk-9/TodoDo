import ctypes
from PIL import Image, ImageDraw, ImageFont
from sys import platform
import pathlib
import random
import subprocess
import os
import tkinter as tk
from dotenv import load_dotenv

#### global variables start

screen_width = 1920  # default values
screen_height = 1080

background_color = ""
font_color = ""

todo_font = ""
todo_size = 0
todo_position = ""
notice_font = ""
notice_size = 0
notice_position = ""

todo_padding = 0
notice_padding = 0

### global variables end


class WallpaperSetter:
    def __init__(self, imageName):
        self.name = imageName
        self.path = str(pathlib.Path().absolute())

    def makeWallpaper(self):
        if platform == "linux" or platform == "linux2":
            print("Linux not supported yet")
        elif platform == "darwin":
            SCRIPT = """/usr/bin/osascript<<END
                tell application "Finder"
                set desktop picture to POSIX file "%s"
                end tell
                END"""
            subprocess.Popen(SCRIPT % f"{self.path}/{self.name}", shell=True)
        elif platform == "win32":
            SPI_SETDESKWALLPAPER = 20
            ctypes.windll.user32.SystemParametersInfoW(
                SPI_SETDESKWALLPAPER, 0, self.path + "\\" + self.name, 1
            )


class TodoGenerator:
    def __init__(self):
        padding = " " * 3
        f = open("todos.txt", "a")
        f.close()
        f = open("todos.txt", "r")
        self.todos = [(padding + todo.strip()) for todo in f]

    def getList(self):
        todosString = ""
        for todo in self.todos:
            todosString += todo + "\n"
        return todosString


class NoticeGenerator:
    def __init__(self):
        padding = " " * 3
        f = open("notices.txt", "a")
        f.close()
        f = open("notices.txt", "r")
        self.notices = [(padding + notice.strip()) for notice in f]

    def getList(self):
        noticeString = ""
        for notice in self.notices:
            noticeString += notice + "\n"
        return noticeString


class WallpaperImageHandler:
    def __init__(
        self, background_color, screen_size_x=screen_width, screen_size_y=screen_height
    ):
        self.image = Image.new(
            "RGB", (screen_size_x, screen_size_y), color=background_color
        )
        self.draw = ImageDraw.Draw(self.image)

    def setText(self, message, fontPath, fontColor, fontSize, coordsX=960, coordsY=50):
        font = ImageFont.truetype(fontPath, fontSize)
        color = fontColor
        self.draw.text((coordsX, coordsY), message, font=font, fill=color)

    def save(self):
        filename = f"outputs/output{random.random()}.jpg"
        self.image.save(filename)
        return filename


def init_system_dimensions():
    root = tk.Tk()
    global screen_width, screen_height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()


def init_settings():
    load_dotenv("settings.txt")

    global todo_font, todo_size, todo_position, notice_font, notice_size, notice_position
    global todo_padding, notice_padding

    todo_font = os.environ.get("TODO_FONT")
    todo_size = int(os.environ.get("TODO_SIZE"))
    todo_position = os.environ.get("TODO_POSITION")
    notice_font = os.environ.get("NOTICE_FONT")
    notice_size = int(os.environ.get("NOTICE_SIZE"))
    notice_position = os.environ.get("NOTICE_POSITION")

    todo_padding = int(os.environ.get("TODO_PADDING"))
    notice_padding = int(os.environ.get("NOTICE_PADDING"))


def init_color_config():
    load_dotenv("color_config.txt")

    global background_color, font_color
    background_color = os.environ.get("BACKGROUND_COLOR")
    font_color = os.environ.get("FONT_COLOR")


def convert_position_data(position, width, height, padding=0):
    # return format (X, Y)
    if position == "l":  # left
        return (padding, (screen_height - height) // 2)
    elif position == "r":  # right
        return (screen_width - width - padding, (screen_height - height) // 2)
    elif position == "t":  # top
        return ((screen_width - width) // 2, padding)
    elif position == "b":  # bottom
        return ((screen_width - width) // 2, screen_height - height - padding)
    elif position == "tl":  # top-right
        return (padding, padding)
    elif position == "tr":  # top-right
        return (screen_width - width - padding, padding)
    elif position == "br":  # top-right
        return (screen_width - width - padding, screen_height - height - padding)
    elif position == "bl":  # top-right
        return (padding, screen_height - height - padding)
    else:  # center
        return ((screen_width - width) // 2, (screen_height - height) // 2)


def main():
    init_system_dimensions()
    init_color_config()
    init_settings()

    todo = TodoGenerator()
    todos = "Todo List:\n" + todo.getList()
    notice = NoticeGenerator()
    notices = "Notices:\n" + notice.getList()

    fontObj = ImageFont.truetype(font=todo_font, size=todo_size)
    (widthT, heightT) = fontObj.getsize_multiline(todos)
    fontObj = ImageFont.truetype(font=notice_font, size=notice_size)
    (widthN, heightN) = fontObj.getsize_multiline(notices)

    Xt = 0  # x-position of todo
    Yt = 0  # y-position of todo
    Xn = 0  # x-position of notices
    Yn = 0  # y-position of notices
    (Xt, Yt) = convert_position_data(todo_position, widthT, heightT, todo_padding)
    (Xn, Yn) = convert_position_data(notice_position, widthN, heightN, notice_padding)

    wih = WallpaperImageHandler(
        background_color, screen_size_x=screen_width, screen_size_y=screen_height
    )
    wih.setText(todos, todo_font, font_color, todo_size, coordsX=Xt, coordsY=Yt)
    wih.setText(notices, notice_font, font_color, notice_size, coordsX=Xn, coordsY=Yn)
    imageName = wih.save()

    ws = WallpaperSetter(imageName)
    ws.makeWallpaper()


main()
