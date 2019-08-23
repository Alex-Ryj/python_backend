from PIL import Image, ImageDraw, ImageFont
import properties

im = Image.open(properties.FILES_PATH + '/Panel1.PNG')
canvas = Image.open(properties.FILES_PATH + '/canvas.PNG')
print(im.format, im.size, im.mode)
img_w, img_h = im.size
im.thumbnail((im.size[0]/2, im.size[1]/2))
# im.show()
print(im.format, im.size, im.mode)
bg_w, bg_h = canvas.size
offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)

canvas.paste(im, offset)
draw = ImageDraw.Draw(canvas)
font = ImageFont.truetype('Roboto-Black.ttf', size=45)
color = 'rgb(0, 0, 0)'
draw.text((10, 50), 'Hello World!', fill=color, font=font)
canvas.show()
