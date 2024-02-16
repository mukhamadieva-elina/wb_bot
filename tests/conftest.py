import asyncio
from unittest.mock import MagicMock

import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from db.models import Base, User
from middleware.service_middleware import ServiceMiddleware, CounterMiddleware

TEST_DB_NAME = "test"


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
        f"postgresql+asyncpg://postgres:123@localhost:5432/{TEST_DB_NAME}"
    )
    return engine


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    engine = create_engine(
        f"postgresql://postgres:123@localhost:5432/{TEST_DB_NAME}"
    )
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture
def counter_middleware():
    return CounterMiddleware()


@pytest.fixture
def service_middleware():
    engine = MagicMock()
    return ServiceMiddleware(engine)