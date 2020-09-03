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
        f = open("todos.txt")
        self.todos = [(padding+todo.strip()) for todo in f]

    def getList(self):
        todosString = ""
        for todo in self.todos:
            todosString += todo + "\n"
        return todosString


class WallpaperImageHandler:
    def __init__(self, backgroundColor, coordsX=960, coordsY=50, screenSizeX=1920, screenSizeY=1080):
        self.image = Image.new(
            'RGB', (screenSizeX, screenSizeY), color=backgroundColor)
        self.draw = ImageDraw.Draw(self.image)
        self.x = coordsX
        self.y = coordsY

    def setText(self, message, fontPath, fontColor, fontSize):
        font = ImageFont.truetype(fontPath, fontSize)
        color = fontColor
        self.draw.text((self.x, self.y), message, font=font, fill=color)

    def save(self):
        filename = 'output.jpg'
        self.image.save(filename)
        return filename


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
    font = 'fonts/OpenSans-BoldItalic.ttf'
    fontSize = 55

    todo = TodoGenerator()
    message = "Todo List:\n" + todo.getList()

    fontObj = ImageFont.truetype(
        font=font, size=fontSize)
    (width, height) = fontObj.getsize_multiline(message)

    wih = WallpaperImageHandler(backgroundColor,
                                coordsX=(1920-width-10),
                                coordsY=(1080-height)/2)
    wih.setText(message, font, fontColor, fontSize)
    imageName = wih.save()

    ws = WallpaperSetter(imageName)
    ws.makeWallpaper()


main(random.randint(0, 7))
