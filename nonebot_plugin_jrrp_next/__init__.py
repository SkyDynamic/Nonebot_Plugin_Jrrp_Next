from nonebot.adapters.onebot.v11 import Bot, Message, GroupMessageEvent
from nonebot.params import CommandArg
from nonebot.plugin import on_command

from .utils import get_jrrp
from .drwa_img import draw_img

import datetime
import random

JRRP_COMMAND = on_command('jrrp', aliases={"今日人品", "j"})
DEFAULT_IMAGE_URL_LIST = [
    'https://t.mwm.moe/moez/', 'https://t.mwm.moe/ycy/', 'https://t.mwm.moe/moez/', 'https://t.mwm.moe/ys/'
    ]

@JRRP_COMMAND.handle()
async def jrrpCommandHandler(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    args = arg.extract_plain_text().split()
    _jrrp: int = 0

    if len(args) == 0:
        user_id = event.user_id
        _jrrp = get_jrrp(str(user_id))

    else:
        user_id = args[0]
        _jrrp = get_jrrp(str(user_id))

    USER_DATA: dict = await bot.call_api('get_stranger_info', **{"user_id": user_id})
    nickname = USER_DATA.get('nickname')
    localtime = datetime.datetime.now()
    url = random.choice(DEFAULT_IMAGE_URL_LIST)
    try:
        image = await draw_img(user_id ,_jrrp, nickname, url, localtime)
    except:
        image = "Bot出了点问题, 返回文字版:\n您今天的人品值是: " + str(_jrrp)
    await JRRP_COMMAND.finish(image)
