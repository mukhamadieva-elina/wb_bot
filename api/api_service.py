import aiohttp


def get_session(path):
    return aiohttp.ClientSession(path)


async def get_product(number):
    par = {
        "appType": 1,
        "curr": "rub",
        "dest": -1257786,
        "spp": 29,
        "nm": number,
    }
    async with get_session("https://card.wb.ru/") as session:
        async with session.get("/cards/detail", params=par) as resp:
            data = await resp.json()
            product = data["data"]["products"]
            return product


def get_image(number) -> str:
    _short_id = number // 100000
    if 0 <= _short_id <= 143:
        basket = '01'
    elif 144 <= _short_id <= 287:
        basket = '02'
    elif 288 <= _short_id <= 431:
        basket = '03'
    elif 432 <= _short_id <= 719:
        basket = '04'
    elif 720 <= _short_id <= 1007:
        basket = '05'
    elif 1008 <= _short_id <= 1061:
        basket = '06'
    elif 1062 <= _short_id <= 1115:
        basket = '07'
    elif 1116 <= _short_id <= 1169:
        basket = '08'
    elif 1170 <= _short_id <= 1313:
        basket = '09'
    elif 1314 <= _short_id <= 1601:
        basket = '10'
    elif 1602 <= _short_id <= 1655:
        basket = '11'
    elif 1656 <= _short_id <= 1919:
        basket = '12'
    else:
        basket = '13'
    return f"https://basket-{basket}.wb.ru/vol{number // 100000}/part{number // 1000}/{number}/images/big/{1}.webp"


async def get_price_history(number):
    _short_id = number // 100000
    if 0 <= _short_id <= 143:
        basket = '01'
    elif 144 <= _short_id <= 287:
        basket = '02'
    elif 288 <= _short_id <= 431:
        basket = '03'
    elif 432 <= _short_id <= 719:
        basket = '04'
    elif 720 <= _short_id <= 1007:
        basket = '05'
    elif 1008 <= _short_id <= 1061:
        basket = '06'
    elif 1062 <= _short_id <= 1115:
        basket = '07'
    elif 1116 <= _short_id <= 1169:
        basket = '08'
    elif 1170 <= _short_id <= 1313:
        basket = '09'
    elif 1314 <= _short_id <= 1601:
        basket = '10'
    elif 1602 <= _short_id <= 1655:
        basket = '11'
    elif 1656 <= _short_id <= 1919:
        basket = '12'
    else:
        basket = '13'
    async with get_session(f"https://basket-{basket}.wb.ru/") as session:
        async with session.get(
                f"/vol{number // 100000}/part{number // 1000}/{number}/info/price-history.json") as resp:
            return await resp.json() if resp.ok else None
