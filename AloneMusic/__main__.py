#
# Copyright (C) 2021-2022 by TheAloneteam@Github, < https://github.com/TheAloneTeam >.
# This file is part of < https://github.com/TheAloneTeam/AloneMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TheAloneTeam/AloneMusic/blob/master/LICENSE >
#
# All rights reserved.

import asyncio
import importlib
import os
from aiohttp import web

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from AloneMusic import LOGGER, app, userbot
from AloneMusic.core.call import Alone
from AloneMusic.misc import sudo
from AloneMusic.plugins import ALL_MODULES
from AloneMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


# ✅ Render HTTP health check server
async def health_check(request):
    return web.Response(text="Bot is running!")


async def start_web_server():
    port = int(os.environ.get("PORT", 8080))
    web_app = web.Application()
    web_app.router.add_get("/", health_check)
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    LOGGER("AloneMusic").info(f"✅ Web server started on port {port}")


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        exit()

    # ✅ Start web server FIRST (Render needs port binding quickly)
    await start_web_server()

    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass

    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("AloneMusic.plugins" + all_module)
    LOGGER("AloneMusic.plugins").info("Successfully Imported Modules...")
    await userbot.start()
    await Alone.start()
    try:
        await Alone.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("AloneMusic").error(
            "Please turn on the videochat of your log group/channel.\n\nStopping Bot..."
        )
        exit()
    except:
        pass
    await Alone.decorators()
    LOGGER("AloneMusic").info(
        "ʙᴏᴛ sᴛᴀʀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ"
    )
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("AloneMusic").info("Stopping Bot...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
