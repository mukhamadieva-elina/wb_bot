from unittest.mock import Mock, AsyncMock

import aiogram
import pytest
from pytest_mock import MockFixture

import utils
from tests.conftest import input_message
from handlers.on_start.help import help
from tests.conftest import *

@pytest.mark.asyncio
async def test_help(input_message: aiogram.types.Message, mocker: MockFixture):
    mock : AsyncMock = mocker.patch("aiogram.types.Message.answer", new_callable=AsyncMock)

    await help(input_message, None)

    mock.assert_called_once_with(utils.info)