import pytest

from wb_bot.utils import validate_articul


@pytest.mark.parametrize("number, result", [('123', True), (123456789012345678901, False), ('abc', False)])
def test_validate_articul(number, result):
    assert validate_articul(number) == result
