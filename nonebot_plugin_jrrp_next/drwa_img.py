from nonebot.adapters.onebot.v11 import MessageSegment
from PIL import Image, ImageDraw, ImageFont
from httpx import AsyncClient
from datetime import datetime
from io import BytesIO
import random
import textwrap

from .utils import DataText, open_img, draw_text
from .resource_manager import StaticPath

HITOKOTO_URL = "https://v1.hitokoto.cn/"
HITOKOTO_TYPE = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l"]

def avatar_handler(image: Image.Image) -> MessageSegment:
    scale = 3
    w, h = image.size
    r = w * scale
    alpha_layer = Image.new("L", (r, r), 0)
    draw = ImageDraw.Draw(alpha_layer)
    draw.ellipse((0, 0, r, r), fill=255)
    alpha_layer = alpha_layer.resize((w, w), Image.LANCZOS)
    image.putalpha(alpha_layer)
    return image

# 样式来自Github MoYoez/Lucy_ZeroBot
async def draw_img(user_id: int, jrrp: int, name: str, background_url: str, time: datetime = datetime.now()) -> Image.Image:
    # Background
    # Step 1
    img_cover = await open_img(background_url)
    img_cover_width, img_cover_height = img_cover.size
    img_cover = img_cover.resize((1280, int(1280 / img_cover_width * img_cover_height)))
    image = Image.new("RGBA", img_cover.size, (0, 0, 0, 0))
    image.alpha_composite(img_cover)
    # Step 2
    image_width = image.width
    image_height = image.height
    im1 = Image.new("RGBA", (image_width * 2, image_height * 2))
    first_round = ImageDraw.Draw(im1, "RGBA")
    first_round.rounded_rectangle((0, 0, image_width * 2, 150 * 2), 15 * 2, (238, 211, 222, 225), width=3 * 2, outline=(255, 255, 255, 255))
    # Step 3
    namelength = ImageFont.truetype(str(StaticPath.AlibabaPuHuiTi), 3).getlength(name)
    nameLength = namelength + 160
    if nameLength <= 450:
        nameLength = 450
    im2 = Image.new("RGBA", (image_width * 2, image_height * 2))
    second_round = ImageDraw.Draw(im2, "RGBA")
    second_round.rounded_rectangle((0, 0, nameLength * 2, 250 * 2), 20 * 2, (91, 57, 83, 255))
    image.alpha_composite(im1.resize((image_width, image_height), Image.LANCZOS), (0, image_height-150))
    image.alpha_composite(im2.resize((image_width, image_height), Image.LANCZOS), (50, image_height-175))
    
    # Text
    # Step 4
    format_time_current = time.strftime("%H:%M:%S")
    format_time_date = time.strftime("%Y/%m/%d")
    format_time_week = time.strftime("%A")
    format_time_length = ImageFont.truetype(str(StaticPath.AlibabaPuHuiTi), 25).getlength(format_time_date)
    draw_time_current = DataText(image_width-10-format_time_length, 50, 25, format_time_current, StaticPath.AlibabaPuHuiTi)
    draw_time_data = DataText(image_width-45-format_time_length, 90, 25, format_time_date, StaticPath.AlibabaPuHuiTi)
    draw_time_week = DataText(image_width-45-format_time_length, 130, 25, format_time_week, StaticPath.AlibabaPuHuiTi)
    image = draw_text(image, draw_time_current, (226, 184, 255, 255))
    image = draw_text(image, draw_time_data, (226, 184, 255, 255))
    image = draw_text(image, draw_time_week, (226, 184, 255, 255))

    draw_time_line = DataText(image_width-40, 30, 150, "|", StaticPath.AlibabaPuHuiTi)
    image = draw_text(image, draw_time_line, (152, 127, 176, 255))

    # Step 5
    draw_user_info = DataText(60, image_height-160, 25, "User Info", StaticPath.AlibabaPuHuiTi)
    image = draw_text(image, draw_user_info)
    avatar_img = await open_img(f"http://q1.qlogo.cn/g?b=qq&nk={user_id}&s=640")
    avatar_img = avatar_img.resize((100, 100))
    avatar_img = avatar_handler(avatar_img)
    image.alpha_composite(avatar_img, (60, image_height-130))

    draw_jrrp = DataText(180, image_height-70, 25, f"今日人品值: {jrrp}", StaticPath.AlibabaPuHuiTi)
    draw_nickname = DataText(180, image_height-120, 25, name, StaticPath.AlibabaPuHuiTi)
    image = draw_text(image, draw_nickname, (155, 121, 147, 255))
    image = draw_text(image, draw_jrrp, (155, 121, 147, 255))

    # Step 6
    im3 = Image.new("RGBA", (image_width * 2, image_height * 2))
    third_round = ImageDraw.Draw(im3, "RGBA")
    third_round.rounded_rectangle((0, 0, 450 * 2, 300 * 2), 20 * 2, (91, 57, 83, 255))
    image.alpha_composite(im3.resize((image_width, image_height), Image.LANCZOS), (image_width-300, image_height-350))

    # Get Hitokoto Message
    hitokoto_result = await AsyncClient().get(HITOKOTO_URL, params={"c": str(random.choice(HITOKOTO_TYPE)), "encode": "json", "min_length": 40, "max_length": 100})
    hitokoto_msg: str = hitokoto_result.json().get("hitokoto")
    hitokoto_msg = hitokoto_msg.replace("。", ". ")
    hitokoto_msg = hitokoto_msg.replace("，", ", ")
    hitokoto_msg_list = textwrap.wrap(hitokoto_msg, width=16)
    spacing = 30
    for line in hitokoto_msg_list:
        image = draw_text(image, DataText(image_width-290, image_height-340+spacing, 20, line, StaticPath.AlibabaPuHuiTi), (155, 121, 147, 255))
        spacing += 30

    draw_hitokoto = DataText(image_width-290, image_height-340, 20, "今日一言", StaticPath.AlibabaPuHuiTi)

    image = draw_text(image, draw_hitokoto)

    CREATED_TEXT_LINES = ["Created by Nonebot_Plugin_Jrrp_Next", "Style by @MoYoez", "Python-Version by @SkyDynamic"]
    spacing = 0
    for line in CREATED_TEXT_LINES:
        image = draw_text(image, DataText(10, 15 + spacing, 18, line, StaticPath.AlibabaPuHuiTi), (155, 121, 147, 255))
        spacing += 18

    buffer = BytesIO()
    image.convert("RGB").save(buffer, "png")

    return MessageSegment.image(buffer)
