import aiohttp

async def ask_mighty(question: str) -> str:
    """
    You input a question and mighty_bot will return a response
    """
    payload = {
        "model": "mightybot",
        "prompt": question,
        "stream": False, # I run it locally :D
    }

    timeout = aiohttp.ClientTimeout(total=180)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(
            "http://127.0.0.1:11434/api/generate",
            json=payload,
        ) as response:
            response.raise_for_status()
            data = await response.json()
            return data["response"].strip()
