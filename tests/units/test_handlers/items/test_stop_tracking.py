from unittest.mock import AsyncMock

import pytest

from db.user_service import UserService
from handlers import stop_tracking_item


@pytest.mark.asyncio
async def test_stop_tracking_item(user_service: UserService):
    number = 197659450
    callback = AsyncMock(data=f'stop_tracking_{number}')
    await stop_tracking_item(callback, user_service)
    user_service.delete_user_product.assert_called_once_with(callback.from_user.id, number)
    callback.message.edit_text.assert_called_once_with('Вы больше не отслеживаете этот товар')
    callback.message.delete_reply_markup.assert_called_once_with()
