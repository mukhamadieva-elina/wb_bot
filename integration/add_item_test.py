import pytest
from pytest_mock import MockerFixture
from telethon.tl.custom import Message
from telethon.tl.types import ReplyInlineMarkup, KeyboardButton

from integration import constants


@pytest.mark.asyncio(scope="module")
async def test_add_item_exists_available_not_in_user_base(start_bot, conv, mocker: MockerFixture, product_item):
    await conv.send_message("/start")
    await conv.get_response()
    await conv.send_message("➕ Добавить товар")
    resp_input_item: Message = await conv.get_response()
    reply_input_item: ReplyInlineMarkup = resp_input_item.reply_markup
    link_example = 'https://basket-05.wbbasket.ru/vol815/part81575/81575967/images/big/2.webp'
    mocker.patch("utils.validate_articul", return_value=True)
    mocker.patch('utils.exist_in_api', return_value=True)
    mocker.patch('db.product_service.ProductService.get_product', return_value=product_item)
    mocker.patch('db.user_service.UserService.user_product_exists_by_number', return_value=False)
    mocker.patch('db.user_service.UserService.add_user_product')
    mocker.patch('api.api_service.get_image', return_value=link_example)
    await conv.send_message("197659450")
    resp_item_added: Message = await conv.get_response()
    resp_card_item: Message = await conv.get_response()
    reply_card_item: ReplyInlineMarkup = resp_card_item.reply_markup
    all_buttons: list[KeyboardButton] = []
    assert resp_input_item.text == f'Введите артикул'
    assert len(reply_input_item.rows) == 1
    assert reply_input_item.rows[0].buttons[0].text == 'Назад'
    assert resp_item_added.text == 'Товар успешно добавлен!'
    assert (resp_card_item.text == f"[\u200b]({link_example})Название товара: {'Cолнцезащитные очки'}\n"
                                      f"Изначальная цена товара: {420.0}\nПоследняя измененная цена товара: {420.0}\n"
                                      f"Разница в цене: {abs(0)}\nТекущий порог оповещения: {'всегда'}")
    for row in reply_card_item.rows:
        all_buttons.extend(row.buttons)
    for button, resp_kb in zip(all_buttons, constants.available_item_inline_keyboard_1):
        assert button.text == resp_kb['text']
        if 'data' in resp_kb:
            assert button.data == resp_kb['data']
        if 'url' in resp_kb:
            assert button.url == resp_kb['url']

@pytest.mark.asyncio(scope="module")
async def test_add_item_exists_available_in_user_base(start_bot, conv, mocker: MockerFixture, product_item):
    await conv.send_message("/start")
    await conv.get_response()
    await conv.send_message("➕ Добавить товар")
    resp_input_item: Message = await conv.get_response()
    reply_input_item: ReplyInlineMarkup = resp_input_item.reply_markup
    mocker.patch("utils.validate_articul", return_value=True)
    mocker.patch('utils.exist_in_api', return_value=True)
    mocker.patch('db.product_service.ProductService.get_product', return_value=product_item)
    mocker.patch('db.user_service.UserService.user_product_exists_by_number', return_value=True)
    await conv.send_message("197659450")
    resp_item_added: Message = await conv.get_response()
    reply_card_item: ReplyInlineMarkup = resp_item_added.reply_markup
    all_buttons: list[KeyboardButton] = []
    assert resp_input_item.text == f'Введите артикул'
    assert len(reply_input_item.rows) == 1
    assert reply_input_item.rows[0].buttons[0].text == 'Назад'
    assert resp_item_added.text == f"Вы уже отслеживаете этот товар!"
    for row in reply_card_item.rows:
        all_buttons.extend(row.buttons)
    for button, resp_kb in zip(all_buttons, constants.expected_start_kb_texts):
        assert button.text == resp_kb
