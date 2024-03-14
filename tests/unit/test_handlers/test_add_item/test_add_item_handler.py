from unittest.mock import AsyncMock

import pytest
from aiogram.fsm.context import FSMContext

import keyboards
from form import Form
from handlers.on_start.add_item.input_item import add_item


@pytest.mark.asyncio
async def test_add_item(state: FSMContext):
    message = AsyncMock()
    await add_item(message, state)
    message.answer.assert_called_once_with(f'Введите артикул',
                                           reply_markup=keyboards.return_to_menu_kb)
    assert await state.get_state() == Form.articul
