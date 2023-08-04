import time
import random

from PIL import Image, ImageFont, ImageDraw
from typing import Tuple
from io import BytesIO
from httpx import AsyncClient
from typing import Union

try:
    from numpy import average
except ImportError:
    def average(Itr):
        return sum(Itr) / len(Itr)

rand = random.Random()


def get_average_color(image: Image.Image):
    pix = image.load()
    R_list = []
    G_list = []
    B_list = []
    width, height = image.size
    for x in range(int(width)):
        for y in range(height):
            R_list.append(pix[x, y][0])
            G_list.append(pix[x, y][1])
            B_list.append(pix[x, y][2])
    R_average = int(average(R_list))
    G_average = int(average(G_list))
    B_average = int(average(B_list))
    return R_average, G_average, B_average


def get_jrrp(string: str):
    now = time.localtime()
    seed = f"h&%tkH+cck>#+{string}+t/sHz2t^6nr+{now.tm_year}+Ba`;05gz4x@5+{now.tm_mday}+2NB>9|0A^gz:+{now.tm_mon}+UtH4vfhh^)q^"
    rand.seed(seed)
    return rand.randint(0, 100)


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
    stroke_fill: Union[str, tuple[int, int, int]]="Black",
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
    stroke_fill: Union[str, tuple[int, int, int]]="Black",
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
