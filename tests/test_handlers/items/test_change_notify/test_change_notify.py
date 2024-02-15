from unittest.mock import AsyncMock

import pytest

import keyboards
from handlers import update_treshhold


@pytest.mark.asyncio
async def test_update_treshhold():
    number = 197659450
    callback = AsyncMock(data=f'update_treshhold_{number}')
    await update_treshhold(callback)
    callback.message.edit_text.assert_called_once_with('Выберите порог оповещения',
                                                       reply_markup=keyboards.update_treshhold_kb(number))
