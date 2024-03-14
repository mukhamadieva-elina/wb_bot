from unittest.mock import AsyncMock

import aiogram.types
import pytest
from pytest_mock import MockerFixture
from tests.units.conftest import *

from api.api_service import get_image
from api.models import item_info
from db.models import UserProduct, Product
from handlers import back_to_item_from_diagram
from tests.units import constants


@pytest.mark.asyncio
async def test_back(callback_query: aiogram.types.CallbackQuery, mocker: MockerFixture, user_product_item,
                    user_service):
    user_product = user_product_item[0]
    user_service.get_user_product_by_number = AsyncMock(return_value=user_product)
    print("--------------------", user_product.Product.availability)
    callback_query_mock = AsyncMock(data=f'to_card_{user_product.Product.number}')

    info, kb = item_info.get_card(get_image(int(user_product.Product.number)), user_product.Product.availability,
                                  user_product.Product.title,
                                  user_product.UserProduct.start_price,
                                  user_product.Product.price,
                                  user_product.Product.price - user_product.UserProduct.start_price,
                                  user_product.UserProduct.alert_threshold)

    get_card_mock = mocker.patch("api.models.item_info.get_card", return_value=(info, kb))
    await back_to_item_from_diagram(callback_query_mock, user_service)
    user_service.get_user_product_by_number.assert_awaited_once_with(callback_query_mock.from_user.id,
                                                                     user_product.Product.number)
    get_card_mock.assert_called_once_with(get_image(int(user_product.Product.number)),
                                          user_product.Product.availability,
                                          user_product.Product.title,
                                          user_product.UserProduct.start_price,
                                          user_product.Product.price,
                                          user_product.Product.price - user_product.UserProduct.start_price,
                                          user_product.UserProduct.alert_threshold)
