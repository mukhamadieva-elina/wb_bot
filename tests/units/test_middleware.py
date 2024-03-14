import pytest
from unittest.mock import MagicMock
from aiogram.types import Message

from middleware.service_middleware import ServiceMiddleware


async def handler(event, data):
    return event, data


@pytest.mark.asyncio
async def test_call_counter(counter_middleware):
    event = MagicMock(spec=Message)
    data = {}

    result = await counter_middleware(handler, event, data)
    assert result[1]['counter'] == 1
    result = await counter_middleware(handler, event, data)
    assert result[1]['counter'] == 2


@pytest.mark.asyncio
async def test_call_service(service_middleware):
    event = MagicMock(spec=Message)
    data = {}

    result = await service_middleware(handler, event, data)

    assert result == (event, data)
    assert data['product_service'] == service_middleware.product_service
    assert data['user_service'] == service_middleware.user_service

@pytest.fixture
def service_middleware():
    engine = MagicMock()
    return ServiceMiddleware(engine)