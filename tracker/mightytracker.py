import asyncio
from APIs.wynnapi import WynnAPI 

guilds = ['ESI', 'BFS']

async def track_guild(wynn, guild):
    g_data = await wynn.get_guild(guild)
    if g_data is None:
        raise ValueError(f'{guild} Data has returned as None')
    ranks = g_data['members']
    members = []
    for rank in ranks:
        if rank == 'total':
            continue
        for member in ranks[rank]:
            members.append(member)
    return members

async def main():
    wynn = await WynnAPI.api()
    if wynn is None:
        return
    try:
        for guild in guilds:
            print(await track_guild(wynn, guild))
    finally:
        await wynn.close()

if __name__ == '__main__':
    asyncio.run(main())
