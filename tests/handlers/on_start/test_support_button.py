from unittest.mock import AsyncMock, create_autospec
from tests.conftest import *

import aiogram
import pytest
from aiogram.fsm.context import FSMContext
from pytest_mock import MockFixture

import keyboards
from form import Form
from handlers import support
from tests.conftest import input_message


@pytest.mark.asyncio
async def test_support_button(input_message: aiogram.types.Message, mocker: MockFixture):
    fsm_mock: FSMContext = create_autospec(FSMContext, instance=True, new_callable=AsyncMock)
    message_answer_mock: AsyncMock = mocker.patch("aiogram.types.Message.answer", new_callable=AsyncMock)

    await support(input_message, fsm_mock)

    fsm_mock.set_state.assert_awaited_once_with(Form.support)
    message_answer_mock.assert_awaited_once_with(f'Привет! Оставьте свои пожелание разработчикам)',
                                                 reply_markup=keyboards.return_to_menu_kb)
