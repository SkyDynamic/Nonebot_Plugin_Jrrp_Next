import time

from PIL import Image, ImageFont, ImageDraw
from typing import Tuple
from io import BytesIO
from httpx import AsyncClient

def rol(num: int, k: int, bits: int = 64):
    b1 = bin(num << k)[2:]
    if len(b1) <= bits:
        return int(b1, 2)
    return int(b1[-bits:], 2)

def get_hash(string: str):
    num = 5381
    num2 = len(string) - 1
    for i in range(num2 + 1):
        num = rol(num, 5) ^ num ^ ord(string[i])
    return num ^ 12218072394304324399

def get_jrrp(string: str):
    now = time.localtime()
    num = round(abs((get_hash("".join([
        "asdfgbn",
        str(now.tm_yday),
        "12#3$45",
        str(now.tm_year),
        "IUY"
    ])) / 3 + get_hash("".join([
        "QWERTY",
        string,
        "0*8&6",
        str(now.tm_mday),
        "kjhg"
    ])) / 3) / 527) % 1001)
    if num >= 970:
        num2 = 100
    else:
        num2 = round(num / 969 * 99)
    return num2

async def open_img(image_path: str, is_url: bool = True) -> Image.Image:
    if is_url:
        origin_data = await AsyncClient().get(image_path)
        img_bytes = BytesIO(origin_data.content)
        return Image.open(img_bytes).convert("RGBA")
    with open(image_path, "rb") as f:
        return Image.open(f).convert("RGBA")

class DataText:
    def __init__(self, L, T, size, text, path, anchor="lt") -> None:
        self.L = L
        self.T = T
        self.text = str(text)
        self.path = path
        self.font = ImageFont.truetype(str(self.path), size)
        self.anchor = anchor

def write_text(
    image: Image.Image,
    font,
    text="text",
    pos=(0, 0),
    color=(255, 255, 255, 255),
    anchor="lt",
    stroke_width=0,
    stroke_fill="Black",
) -> Image.Image:
    rgba_image = image
    text_overlay = Image.new("RGBA", rgba_image.size, (255, 255, 255, 0))
    image_draw = ImageDraw.Draw(text_overlay)
    image_draw.text(
        pos,
        text,
        font=font,
        fill=color,
        anchor=anchor,
        stroke_width=stroke_width,
        stroke_fill=stroke_fill,
    )
    return Image.alpha_composite(rgba_image, text_overlay)

def draw_text(
    image,
    class_text: DataText,
    color: Tuple[int, int, int, int] = (255, 255, 255, 255),
    stroke_width=0,
    stroke_fill="Black",
) -> Image.Image:
    font = class_text.font
    text = class_text.text
    anchor = class_text.anchor
    color = color
    return write_text(
        image,
        font,
        text,
        (class_text.L, class_text.T),
        color,
        anchor,
        stroke_width=stroke_width,
        stroke_fill=stroke_fill,
    )