from PIL import Image, ImageDraw

def rond(imgg):
    bigsize = (imgg.size[0] * 3, imgg.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(imgg.size, Image.ANTIALIAS)
    imgg.putalpha(mask)

img0 = Image.open("icone0.png").resize((180, 180))

rond(img0)

img0.show()