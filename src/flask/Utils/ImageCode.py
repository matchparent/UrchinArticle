import random
import string
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont


def rand_code():
    # return "".join(random.sample(string.ascii_letters + string.digits, 4))
    return "1234"

def rand_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def draw_code():
    code = rand_code()
    width, height = 120, 50
    img = Image.new("RGB", (width, height), "white")
    font = ImageFont.truetype(font="/System/Library/Fonts/Supplemental/Academy Engraved LET Fonts.ttf", size=40)
    draw = ImageDraw.Draw(img)
    for i in range(4):
        draw.text((11 + 25 * i, 10), text=code[i], fill=rand_color(), font=font)
    return img, code


def byte_code():
    img, code = draw_code()
    buf = BytesIO()
    img.save(buf, "jpeg")
    return code, buf.getvalue()
