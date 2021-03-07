#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
File: call-owner.py
Created Date: 2021-02-19 23:02:45
Author: Kyomotoi
Email: Kyomotoiowo@gmail.com
License: GPLv3
Project: https://github.com/Kyomotoi/ATRI
--------
Last Modified: Sunday, 7th March 2021 3:13:40 pm
Modified By: Kyomotoi (kyomotoiowo@gmail.com)
--------
Copyright (c) 2021 Kyomotoi
'''

from nonebot.permission import SUPERUSER
from nonebot.plugin import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import (
    Bot,
    MessageEvent
)

from ATRI.rule import is_in_banlist
from ATRI.config import nonebot_config
from ATRI.utils.apscheduler import scheduler
from ATRI.utils.list import count_list


repo_list = []


repo = on_command("来杯红茶", rule=is_in_banlist())

@repo.handle()
async def _repo(bot: Bot, event: MessageEvent, state: T_State) -> None:
    msg = str(event.message).strip()
    if msg:
        state["msg"] = msg

@repo.got("msg", prompt="请告诉咱需要反馈的内容~！")
async def _repo_(bot: Bot, event: MessageEvent, state: T_State) -> None:
    global repo_list
    msg = state["msg"]
    user = event.user_id
    
    if count_list(repo_list, user) == 5:
        await repo.finish("吾辈已经喝了五杯红茶啦！明天再来吧。")
    
    repo_list.append(user)

    for sup in nonebot_config["superusers"]:
        await bot.send_private_msg(
            user_id=sup,
            message=f"来自用户[{user}]反馈：\n{msg}"
        )
    
    await repo.finish("吾辈的心愿已由咱转告给咱的维护者了~！")


@scheduler.scheduled_job(
    "cron",
    hour=0,
    misfire_grace_time=60
)
async def _() -> None:
    global repo_list
    repo_list = []


reset_repo = on_command("重置红茶", permission=SUPERUSER)

@reset_repo.handle()
async def _reset_repo(bot: Bot, event: MessageEvent) -> None:
    global repo_list
    repo_list = []
    await reset_repo.finish("红茶重置完成~！")
