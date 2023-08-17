import asyncio
import logging
import websockets
import aiohttp
from aiofile import async_open
from datetime import datetime, timedelta
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK

logging.basicConfig(level=logging.INFO)


# url = https://api.privatbank.ua/p24api/exchange_rates?date=22.07.2023


async def request(url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    r = await resp.json()
                    return r
                else:
                    logging.error(f"Error status: {resp.status} for {url}")
        except aiohttp.ClientConnectorError as err:
            logging.error(f"Connection error: {url}", str(err))


async def get_exchange(day, currency=None):
    today = datetime.now()
    currency_list = ["EUR", "USD"]
    res = []

    for days_ago in range(0, int(day)):
        date = today - timedelta(days=days_ago)
        formatted_date = date.strftime("%d.%m.%Y")
        try:
            data = await request(
                f"https://api.privatbank.ua/p24api/exchange_rates?date={formatted_date}"
            )

            for i in data["exchangeRate"]:
                if i["currency"] in currency_list:
                    res.append(
                        f"|| date : {formatted_date} || {i['currency']} - sale : {i['saleRate']} and  purchase : {i['purchaseRate']} ||"
                    )
        except KeyError:
            return "You input incorect data"

    return "".join(res)


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        self.clients.add(ws)
        logging.info(f"{ws.remote_address} connects")

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f"{ws.remote_address} disconnects")

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distrubute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def exchange(self, list_message: list):
        if len(list_message) == 2 and list_message[1].isdigit():
            r = await get_exchange(list_message[1])
            await self.send_to_clients(r)
        elif len(list_message) == 1:
            r = await get_exchange(1)
            await self.send_to_clients(r)

    async def distrubute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            if message.startswith("exchange"):
                async with async_open("Exchange.log", "a") as afp:
                    await afp.write(
                        f"{str(datetime.now())}: - exchange was be called.\n"
                    )

                list_message = message.split(" ")
                await self.exchange(list_message)
            else:
                await self.send_to_clients(message)


async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, "localhost", 8080):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
