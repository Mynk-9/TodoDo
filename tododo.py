from PIL import Image, ImageDraw, ImageFont
import ctypes
import pathlib


class wallpaperSetter:
    def __init__(self, imageName):
        self.name = imageName
        self.path = str(pathlib.Path().absolute())

    def makeWallpaper(self):
        SPI_SETDESKWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER, 0, self.path+"\\"+self.name, 0)


class TodoGenerator:
    def __init__(self):
        self.todo = ""
        padding = " "*3
        for i in range(1, 5+1):
            self.todo += padding + "task" + str(i) + "\n"

    def getList(self):
        return self.todo


image = Image.open('assets/background1.jpg')
draw = ImageDraw.Draw(image)
font = ImageFont.truetype('fonts/OpenSans-SemiBoldItalic.ttf', size=55)

(x, y) = (960, 50)
todo = TodoGenerator()
message = "Todo List:\n" + todo.getList()
color = 'black'

draw.text((x, y), message, font=font, fill=color)

image.save('output.jpg')

ws = wallpaperSetter("output.jpg")
ws.makeWallpaper()
