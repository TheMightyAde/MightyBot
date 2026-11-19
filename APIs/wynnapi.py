api = None
url_wynn = "https://api.wynncraft.com/v3"

import asyncio
import aiohttp

import os
from dotenv import load_dotenv
load_dotenv()
wynn_token = os.getenv('WYNN_TOKEN')
class WynnAPI:
    url = url_wynn
    _instance = None
    _session_lock = asyncio.Lock()
    def __init__(self,
                 session: aiohttp.ClientSession,
                 token: str = wynn_token
                 ):
        self.token = token
        self.session = session
    @property
    def closed(self):
        return self.session.closed
    @classmethod
    async def get_wynn_api(cls):
        async with cls._session_lock:
            if cls._instance is None or cls._instance.closed:
                _session = aiohttp.ClientSession()
                cls._instance = cls(_session)
            return cls._instance

    async def close(self):
        if not self.session.closed:
            await self.session.close()

    async def get_player(self, username: str):
        url = f"{self.url}/player/{username}"

        async with self.session.get(url) as resp:
            if resp.status != 200:
                return None
            return await resp.json()

    async def get_guild(self, guild: str):
        url = f"{self.url}/guild/prefix/{guild}"

        async with self.session.get(url) as resp:
            if resp.status != 200:
                return None
            return await resp.json()
    async def get_character(self, username: str, character:str):
        url = f"{self.url}/player/{username}/characters/{character}"

        async with self.session.get(url) as resp:
            if resp.status != 200:
                return None
            return await resp.json()


async def api():
    """
    Turns a desired variable into the wynncraft API to be used.
    Example:
        something = api()
    """
    try:
       client = await WynnAPI()
    except Exception as e:
        print(f"Something happened {e}")
        return None
    return client
