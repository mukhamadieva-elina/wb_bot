import asyncio

import pytest

from sqlalchemy.ext.asyncio import create_async_engine

bd_pass = "nhm5QjITYfBRi51punlNCMnOBAmXXBvi"


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
        f"postgresql+asyncpg://dyvawvhc:{bd_pass}@trumpet.db.elephantsql.com/dyvawvhc"
    )
    return engine
