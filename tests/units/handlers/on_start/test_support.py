import unittest
from unittest.mock import Mock, AsyncMock, create_autospec
from tests.units.conftest import *

import aiogram
import pytest
from aiogram.fsm.context import FSMContext
from pytest_mock import MockFixture

import keyboards
import utils
from tests.units.conftest import input_message
from handlers.on_start.support import process_msg_to_support


@pytest.mark.asyncio
async def test_support(input_message: aiogram.types.Message, mocker: MockFixture):
    admin_id = 480316781
    send_message_mock = mocker.patch("aiogram.Bot.send_message", new_callable=AsyncMock)
    fsm_mock: FSMContext = create_autospec(FSMContext, instance=True, new_callable=AsyncMock)
    message_answer_mock: AsyncMock = mocker.patch("aiogram.types.Message.answer", new_callable=AsyncMock)

    await process_msg_to_support(input_message, fsm_mock)

    send_message_mock.assert_awaited_once_with(admin_id, input_message.text)
    message_answer_mock.assert_awaited_once_with("Спасибо! Комментарий был отправлен разработчикам.",
                                                reply_markup=keyboards.menu_kb)
    fsm_mock.clear.assert_awaited_once()
