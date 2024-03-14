from unittest.mock import AsyncMock

import pytest

from aiogram.fsm.context import FSMContext

from form import Form
from handlers.on_start.add_item.back import to_menu


@pytest.mark.asyncio
async def test_to_menu(state: FSMContext):
    callback = AsyncMock(data='to_menu')
    await to_menu(callback, state)
    callback.message.edit_text.assert_called_once_with('Вы вернулись в главное меню')
    assert await state.get_state() == Form.menu
