
import asyncio
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

wynn_tokens = [
    os.getenv('WYNN_TOKEN'),
    os.getenv('MIGHTY_TOKEN')
]

wynn_tokens = [token for token in wynn_tokens if token]

url_wynn = "https://api.wynncraft.com/v3"


class WynnAPI:

    url = url_wynn

    _instance = None
    _session_lock = asyncio.Lock()

    def __init__(self, session: aiohttp.ClientSession, tokens: list):
        self.session = session
        self.tokens = tokens
        self.token_index = 0

    @property
    def closed(self):
        return self.session.closed

    @classmethod
    async def api(cls, tokens=wynn_tokens):
        """
        Creates or returns the shared Wynncraft API instance.
        """
        try:
            async with cls._session_lock:

                if not tokens:
                    raise ValueError("No Wynncraft API tokens found.")

                if cls._instance is None or cls._instance.closed:
                    session = aiohttp.ClientSession()
                    cls._instance = cls(session, tokens)

                return cls._instance

        except Exception as e:
            print(f"Something happened: {e}")
            return None

    async def close(self):
        if not self.session.closed:
            await self.session.close()

        async with type(self)._session_lock:
            type(self)._instance = None

    async def request(self, url):
        """
        Sends a request and rotates API keys when rate-limited.
        """

        for _ in range(len(self.tokens)):

            token = self.tokens[self.token_index]

            headers = {
                'Authorization': f'Bearer {token}'
            }

            async with self.session.get(url, headers=headers) as resp:

                if resp.status == 429:
                    self.token_index = (
                        self.token_index + 1
                    ) % len(self.tokens)

                    continue

                if resp.status != 200:
                    return None

                return await resp.json()

        raise Exception("All API keys have reached their rate limits. DM TheMightyAde to donate him money for more keys please")

    async def get_player(self, username: str):
        url = f"{self.url}/player/{username}"
        return await self.request(url)

    async def get_guild(self, guild: str):
        url = f"{self.url}/guild/prefix/{guild}"
        return await self.request(url)

    async def get_guild_uuid(self, guild_uuid: str):
        """
        Gets guild information using its UUID.
        """
        url = f"{self.url}/guild/{guild_uuid}"
        return await self.request(url)

    async def get_character(self, username: str, character: str):
        url = f"{self.url}/player/{username}/characters/{character}"
        return await self.request(url)
