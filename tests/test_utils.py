import pytest

from utils import exist_in_api, validate_articul


@pytest.mark.parametrize("number, result",
                         [('123', True), (123456789012345678901, False), (12345678901234567890, True), ('abc', False)])
def test_validate_articul(number, result):
    assert validate_articul(number) == result

# @pytest.mark.asyncio
# async def test_not_exist_in_api():
#     product = await exist_in_api(1245678)
#     assert len(product) == 0


# @pytest.mark.asyncio
# async def test_exist_in_api():
#     product = await exist_in_api(210099604)
#     assert len(product) != 0
