from PIL import Image, ImageDraw, ImageFont
import ctypes
import pathlib
import random


class WallpaperSetter:
    def __init__(self, imageName):
        self.name = imageName
        self.path = str(pathlib.Path().absolute())

    def makeWallpaper(self):
        SPI_SETDESKWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER, 0, self.path+"\\"+self.name, 1)


class TodoGenerator:
    def __init__(self):
        padding = " "*3
        f = open("todos.txt", "a")
        f.close()
        f = open("todos.txt", "r")
        self.todos = [(padding+todo.strip()) for todo in f]

    def getList(self):
        todosString = ""
        for todo in self.todos:
            todosString += todo + "\n"
        return todosString


class NoticeGenerator:
    def __init__(self):
        padding = " "*3
        f = open("notices.txt", "a")
        f.close()
        f = open("notices.txt", "r")
        self.notices = [(padding+notice.strip()) for notice in f]

    def getList(self):
        noticeString = ""
        for notice in self.notices:
            noticeString += notice + "\n"
        return noticeString


class WallpaperImageHandler:
    def __init__(self, backgroundColor, screenSizeX=1920, screenSizeY=1080):
        self.image = Image.new(
            'RGB', (screenSizeX, screenSizeY), color=backgroundColor)
        self.draw = ImageDraw.Draw(self.image)

    def setText(self, message, fontPath, fontColor, fontSize, coordsX=960, coordsY=50):
        font = ImageFont.truetype(fontPath, fontSize)
        color = fontColor
        self.draw.text((coordsX, coordsY), message, font=font, fill=color)

    def save(self):
        filename = 'output.jpg'
        self.image.save(filename)
        return filename


def loadSettings():
    f = open("settings.txt")
    i = 0
    data = [""]*6
    for line in f:
        if (i == 6):
            break
        if line.strip()[0] == '#':
            continue
        data[i] = line.strip()
        i += 1
    return ((data[0], int(data[1]), data[2]), (data[3], int(data[4]), data[5]))


def convertPositionData(position, width, height):
    # return format (X, Y)
    padding = 20
    if position == 'l':     # left
        return (padding, (1080-height)//2)
    elif position == 'r':   # right
        return (1920-width-padding, (1080-height)//2)
    elif position == 't':   # top
        return ((1920-width)//2, padding)
    elif position == 'b':   # bottom
        return ((1920-width)//2, 1080-height-padding)
    else:                   # center
        return ((1920-width)//2, (1080-height)//2)


def main(colorIndex):
    colorCombinations = [
        ('#166a68', '#CAF4F3'),     # 0
        ('#FFF2CD', '#000000'),     # 1
        ('#121212', '#BB86FC'),     # 2
        ('#f5f0e1', '#1e3d59'),     # 3
        ('#3b4d61', '#6b7b8c'),     # 4
        ('rgb(45, 45, 45)', 'rgb(75, 74, 72)'),         # 5
        ('rgb(52, 73, 94)', 'rgb(215, 215, 215)'),      # 6
        ('rgb(74, 103, 98)', 'rgb(98, 134, 124)'),      # 7
    ]

    (backgroundColor, fontColor) = colorCombinations[colorIndex]
    ((fontT, fontSizeT, positionT), (fontN, fontSizeN, positionN)) = loadSettings()
    # *T - for Todo list
    # *N - for Notice list

    todo = TodoGenerator()
    todos = "Todo List:\n" + todo.getList()
    notice = NoticeGenerator()
    notices = "Notices:\n" + notice.getList()

    fontObj = ImageFont.truetype(
        font=fontT, size=fontSizeT)
    (widthT, heightT) = fontObj.getsize_multiline(todos)
    fontObj = ImageFont.truetype(
        font=fontN, size=fontSizeN)
    (widthN, heightN) = fontObj.getsize_multiline(notices)

    Xt = 0   # x-position of todo
    Yt = 0   # y-position of todo
    Xn = 0   # x-position of notices
    Yn = 0   # y-position of notices
    (Xt, Yt) = convertPositionData(positionT, widthT, heightT)
    (Xn, Yn) = convertPositionData(positionN, widthN, heightN)

    wih = WallpaperImageHandler(backgroundColor)
    wih.setText(todos, fontT, fontColor, fontSizeT, coordsX=Xt, coordsY=Yt)
    wih.setText(notices, fontN, fontColor, fontSizeN, coordsX=Xn, coordsY=Yn)
    imageName = wih.save()

    ws = WallpaperSetter(imageName)
    ws.makeWallpaper()


main(random.randint(0, 7))
