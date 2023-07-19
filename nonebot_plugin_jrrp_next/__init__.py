from nonebot.adapters.onebot.v11 import Bot, Message, GroupMessageEvent
from nonebot.params import CommandArg
from nonebot.plugin import on_command

from .utils import get_jrrp
from .drwa_img import draw_img

import datetime
import random

JRRP_COMMAND = on_command('jrrp', aliases={"今日人品", "j"})
DEFAULT_IMAGE_URL_LIST = ['https://t.mwm.moe/moez/', 'https://t.mwm.moe/ycy/', 'https://t.mwm.moe/moez/', 'https://t.mwm.moe/ys/']

@JRRP_COMMAND.handle()
async def jrrpCommandHandler(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    args = arg.extract_plain_text().split()
    _jrrp: int = 0

    if len(args) == 0:
        _jrrp = get_jrrp(str(event.user_id))
    else:
        _jrrp = get_jrrp(str(args[0]))

    USER_GROUP_DATA: dict = await bot.call_api('get_group_member_info', **{"group_id": event.group_id, "user_id": event.user_id})
    nickname = USER_GROUP_DATA.get('nickname')
    localtime = datetime.datetime.now()
    url = random.choice(DEFAULT_IMAGE_URL_LIST)
    image = await draw_img(event.user_id ,_jrrp, nickname, url, localtime)
    await JRRP_COMMAND.finish(image)
