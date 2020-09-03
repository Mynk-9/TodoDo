from PIL import Image, ImageDraw, ImageFont
import ctypes
import pathlib


class WallpaperSetter:
    def __init__(self, imageName):
        self.name = imageName
        self.path = str(pathlib.Path().absolute())

    def makeWallpaper(self):
        SPI_SETDESKWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER, 0, self.path+"\\"+self.name, 0)


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
    def __init__(self, backgroundPath, coordsX=960, coordsY=50):
        self.image = Image.open(backgroundPath)
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


def main():
    backgroundImage = 'assets/background3.jpg'
    font = 'fonts/OpenSans-SemiBoldItalic.ttf'
    fontColor = 'black'
    fontSize = 55

    todo = TodoGenerator()
    message = "Todo List:\n" + todo.getList()

    fontObj = ImageFont.truetype(
        font=font, size=fontSize)
    (width, height) = fontObj.getsize_multiline(message)

    wih = WallpaperImageHandler(backgroundImage, coordsX=(
        1920-width-10), coordsY=(1080-height)/2)
    wih.setText(message, font, fontColor, fontSize)
    imageName = wih.save()

    ws = WallpaperSetter(imageName)
    ws.makeWallpaper()


main()
