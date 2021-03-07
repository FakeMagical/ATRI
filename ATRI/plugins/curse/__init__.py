#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
File: __init__.py
Created Date: 2021-02-04 17:58:27
Author: Kyomotoi
Email: Kyomotoiowo@gmail.com
License: GPLv3
Project: https://github.com/Kyomotoi/ATRI
--------
Last Modified: Sunday, 7th March 2021 3:14:41 pm
Modified By: Kyomotoi (kyomotoiowo@gmail.com)
--------
Copyright (c) 2021 Kyomotoi
'''

from nonebot.plugin import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent

from ATRI.rule import (
    is_in_banlist,
    is_in_dormant,
    is_in_service
)
from ATRI.utils.list import count_list, del_list_aim
from ATRI.utils.request import get_text
from ATRI.exceptions import RequestTimeOut


URL = "https://zuanbot.com/api.php?level=min&lang=zh_cn"
sick_list = []


__plugin_name__ = 'curse'

curse = on_command(
    "口臭一下",
    aliases={"口臭", "骂我"},
    rule=is_in_banlist() & is_in_dormant()
    & is_in_service(__plugin_name__)
)

@curse.handle()
async def _curse(bot: Bot, event: MessageEvent) -> None:
    global sick_list
    user = event.get_user_id()
    
    if count_list(sick_list, user) == 3:
        sick_list.append(user)
        repo = (
            "不是？？你这么想被咱骂的嘛？？"
            "被咱骂就这么舒服的吗？！"
            "该......你该不会是.....M吧！"
        )
        await curse.finish(repo)
    elif count_list(sick_list, user) == 6:
        sick_list = del_list_aim(sick_list, user)
        await curse.finish("给我适可而止阿！？")
    else:
        sick_list.append(user)
        try:
            await curse.finish(await get_text(URL))
        except RequestTimeOut:
            raise RequestTimeOut("Time out!")
