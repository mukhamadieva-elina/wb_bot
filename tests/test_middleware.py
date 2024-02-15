import pytest
from unittest.mock import MagicMock
from aiogram.types import Message


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
