from PIL import Image, ImageDraw, ImageFont

image = Image.open('assets/background5.jpg')

draw = ImageDraw.Draw(image)

font = ImageFont.truetype('fonts/OpenSans-SemiBoldItalic.ttf', size=55)

(x,y) = (960, 50)
message = "test message1"
color = 'white'

draw.text((x,y), message, font=font, fill=color)

image.save('output.jpg')