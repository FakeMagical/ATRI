#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
File: hitokoto.py
Created Date: 2021-02-04 17:40:21
Author: Kyomotoi
Email: Kyomotoiowo@gmail.com
License: GPLv3
Project: https://github.com/Kyomotoi/ATRI
--------
Last Modified: Sunday, 7th March 2021 3:11:44 pm
Modified By: Kyomotoi (kyomotoiowo@gmail.com)
--------
Copyright (c) 2021 Kyomotoi
'''

import os
import json
from pathlib import Path
from random import choice, randint

from nonebot.plugin import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent

from ATRI.rule import (
    is_in_banlist,
    is_in_dormant,
    is_in_service,
    to_bot
)
from ATRI.exceptions import LoadingError
from ATRI.utils.list import count_list, del_list_aim


HITOKOTO_DIR = Path('.') / 'ATRI' / 'data' / 'database' / 'hitokoto'
sick_list = []


__plugin_name__ = 'hitokoto'

hitokoto = on_command(
    "一言",
    aliases={"抑郁一下", "网抑云"},
    rule=is_in_banlist() & is_in_dormant()
    & is_in_service(__plugin_name__) & to_bot()
)

@hitokoto.handle()
async def _hitokoto(bot: Bot, event: MessageEvent) -> None:
    global sick_list
    user = event.get_user_id()

    if count_list(sick_list, user) == 3:
        sick_list.append(user)
        await hitokoto.finish("额......需要咱安慰一下嘛~？")
    elif count_list(sick_list, user) == 6:
        sick_list = del_list_aim(sick_list, user)
        msg = (
            "如果心里感到难受就赶快去睡觉！别再憋自己了！\n"
            "我...我会守在你身边的！...嗯..一定"
        )
        await hitokoto.finish(msg)
    else:
        sick_list.append(user)
        rd = choice(os.listdir(HITOKOTO_DIR))
        path = HITOKOTO_DIR / rd
        data = {}
        try:
            data = json.loads(path.read_bytes())
        except LoadingError:
            raise LoadingError("Loading error!")
        await hitokoto.finish(data[randint(1, len(data) - 1)]['hitokoto'])
