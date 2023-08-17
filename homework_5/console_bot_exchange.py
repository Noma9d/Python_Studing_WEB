import aiohttp
import asyncio
import logging
from sys import argv
from datetime import datetime, timedelta


async def get_currency_rates(date):
    url = f"https://api.privatbank.ua/p24api/exchange_rates?json&date={date}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                logging.error(f"Error status {response.status} for {url}")
                return None
        except aiohttp.ClientConnectionError() as err:
            logging.error(f"Connection error {str(err)}")
            return None


async def get_exchange(day, currency=None):
    today = datetime.now()
    result = []
    currency_list = ["EUR", "USD"]
    if currency:
        currency_list.extend(list(currency))

    for days_ago in range(0, int(day)):
        date = today - timedelta(days=days_ago)
        formatted_date = date.strftime("%d.%m.%Y")
        try:
            data = await get_currency_rates(formatted_date)
            for i in data["exchangeRate"]:
                if i["currency"] in currency_list:
                    result.append(
                        {
                            formatted_date: {
                                i["currency"]: {
                                    "sale": i["saleRate"],
                                    "purchase": i["purchaseRate"],
                                }
                            }
                        }
                    )
        except KeyError:
            logging.error("Yo input not suported date")

    return result


async def main():
    if len(argv) == 1:
        day = 1
        currency = None
    elif 0 < int(argv[1]) < 10 and len(argv) == 2:
        day = argv[1]
        currency = None
    elif 0 < int(argv[1]) < 10 and len(argv) >= 3:
        day, currency = argv[1], argv[2:]
    else:
        logging.error("You input not supported day. Pleas input for 1 to 10 days")
    r = await get_exchange(day, currency)
    print(r)


if __name__ == "__main__":
    asyncio.run(main())
