import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine

from db.models import Base, User

TEST_DB_NAME = "test"


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


def pytest_sessionstart(session):
    engine = create_engine(
        f"postgresql://postgres:123@localhost:5432/{TEST_DB_NAME}"
    )
    Base.metadata.drop_all(engine)
