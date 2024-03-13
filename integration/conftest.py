import asyncio
import logging
import sys

from pytest_asyncio import fixture
from telethon import TelegramClient
from telethon.sessions import StringSession

import config
import main


@fixture
async def start_bot():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    print("running bot")
    task = asyncio.create_task(main.main())
    await asyncio.sleep(5)
    yield


@fixture
async def conv():
    api_id = config.api_id
    api_hash = config.api_hash
    session_str = config.session_str

    client = TelegramClient(StringSession(session_str), api_id, api_hash, system_version="4.16.30-vxCUSTOM")

    async with client:
        async with client.conversation("@xenob8bot", timeout=5) as conv:
            yield conv
