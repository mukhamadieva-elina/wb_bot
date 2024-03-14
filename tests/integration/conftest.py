import asyncio
import logging
import sys

import pytest
from pytest_asyncio import fixture
from sqlalchemy.ext.asyncio import create_async_engine
from telethon import TelegramClient
from telethon.sessions import StringSession

import config
import main

test_bd_pass = config.test_bd_pass


# @pytest.fixture(scope="session")
# def event_loop():
#     loop = asyncio.get_event_loop()
#     yield loop
#     loop.close()
@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@fixture(scope="module")
async def start_bot():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    print("running bot")
    task = asyncio.create_task(main.main())
    await asyncio.sleep(5)
    yield


@fixture(scope="module")
async def conv():
    api_id = config.api_id
    api_hash = config.api_hash
    session_str = config.session_str

    client = TelegramClient(StringSession(session_str), api_id, api_hash, system_version="4.16.30-vxCUSTOM")

    async with client:
        async with client.conversation("@xenob8bot", timeout=5) as conv:
            yield conv


@pytest.fixture(scope='session')
def event_loop():
    """
    Creates an instance of the default event loop for the test session.
    """
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def connection():
    engine = create_async_engine(
        f"postgresql+asyncpg://dyvawvhc:{test_bd_pass}@trumpet.db.elephantsql.com/dyvawvhc"
    )
    return engine
