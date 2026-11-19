
# REQUIRES THE 'APIs' FOLDER

import discord as dc

from discord.ext import commands
from discord import app_commands

import json
import io
import pandas as pd

class wynncraft(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.api = bot.api

    @app_commands.command(
        name="stalk_guild",
        description="Gather Guild info as a JSON file"
    )
    async def stalk_guild(self, interaction: dc.Interaction, guild: str):

        await interaction.response.defer()

        try:
            data = await self.api.get_guild(guild)

            if data is None:
                await interaction.followup.send(
                    f"`{guild}` Not Found. (Does not exist)"
                )
                return

            json_data = json.dumps(data, indent=2)

            file = dc.File(
                io.BytesIO(json_data.encode("utf-8")),
                filename=f"{guild}.json"
            )

            await interaction.followup.send(
                content=f"We got your data now :D **{guild}**:",
                file=file
            )

        except Exception as e:
            print(
                f"ERROR: MY CODE BROKE. "
                f"Also {type(e).__name__}: {e}"
            )

            await interaction.followup.send(
                f"ERROR: MY CODE BROKE, Dm TheMightyAde. "
                f"Also `{type(e).__name__}: {e}`"
            )

    @app_commands.command(
        name="warteam",
        description="Gather an estimate of the guilds warteam (Heavily Inaccurate)"
    )
    async def warteam(self, interaction: dc.Interaction, guild: str):

        await interaction.response.defer()

        try:
            data = await self.api.get_guild(guild)

            if data is None:
                await interaction.followup.send(
                    f'{guild} Not Found. (Does not Exist)'
                )
                return

            o_members = []
            rank = []

            online = int(data['online'])
            data = data['members']

            for key in data:

                if key == 'total':
                    continue

                for player in data[key]:

                    p_data = data[key][player]

                    if p_data['online'] is True:
                        o_members.append(player)
                        rank.append(key)

            streamers = online - len(o_members)
            max_size = 5 - streamers

            if max_size <= 0:
                await interaction.followup.send(
                    'Hey, The warrers are in `/stream`.'
                )
                return

            world_v = []
            character_v = []

            for member in o_members:

                p_data = await self.api.get_player(member)

                if p_data is None:
                    world_v.append('N/A')
                    character_v.append('N/A')

                else:
                    world_v.append(p_data.get('server', 'N/A'))
                    character_v.append(p_data.get('type', 'N/A'))

            df = pd.DataFrame({
                'players': o_members,
                'world': world_v,
                'class': character_v
            })

            counts = df['world'].value_counts()
            world_max = counts[counts <= max_size]

            if world_max.empty:
                await interaction.followup.send(
                    'Could not find a suitable warteam.'
                )
                return

            world = world_max.idxmax()

            warteam = df[df['world'] == world].head(max_size)

            # Sort the world of online members
            # Take account of max members in a team and /stream
            # Return message containing war team

            await interaction.followup.send(
                f'{warteam} \n help or ban. Also {streamers} people in /stream'
            )

        except Exception as e:
            print(
                f"ERROR: MY CODE BROKE. "
                f"Also {type(e).__name__}: {e}"
            )

            await interaction.followup.send(
                f"ERROR: MY CODE BROKE, DM TheMightyAde. "
                f"Also `{type(e).__name__}: {e}`"
            )

    @app_commands.command(
        name="stalk_player",
        description="Gather Player info as a JSON file"
    )
    async def stalk_player(self, interaction: dc.Interaction, username: str):

        await interaction.response.defer()

        try:
            data = await self.api.get_player(username)

            if data is None:
                await interaction.followup.send(
                    f"`{username}` Not Found (Does Not Exist)."
                )
                return

            json_data = json.dumps(data, indent=2)

            file = dc.File(
                io.BytesIO(json_data.encode("utf-8")),
                filename=f"{username}.json"
            )

            await interaction.followup.send(
                content=f"We got your data now :D **{username}**:",
                file=file
            )

        except Exception as e:
            print(
                f"ERROR: MY CODE BROKE. "
                f"Also {type(e).__name__}: {e}"
            )

            await interaction.followup.send(
                f"ERROR: MY CODE BROKE, Dm TheMightyAde. "
                f"Also `{type(e).__name__}: {e}`"
            )


async def setup(bot):
    await bot.add_cog(wynncraft(bot))
