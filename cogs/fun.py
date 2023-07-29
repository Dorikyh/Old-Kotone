import discord
from discord.ext import commands
from discord.commands import slash_command, Option
import requests
import datetime
import aiohttp
from discord.ext.bridge import bridge_command
from utils import twobuttonview

    
class Fun(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("[✔️] Fun was loaded successfully")  

    @slash_command(name="lolstats")
    async def lolstats(self, ctx, username: str, region: discord.Option(str, choices=['BR', 'LA1', 'LA2', 'JP', 'KR'])):
        """Get stats about a League of Legends player."""
    
        # Make a request to the Riot API to get the player's stats
        async with aiohttp.ClientSession() as session:
            url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{username}"
            headers = {
                "X-Riot-Token": "RGAPI-xxxx"
            }
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    player_data = await response.json()
                else:
                    raise Exception("Error getting player data")
    
            url = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{player_data['id']}"
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    ranked_data = await response.json()
                else:
                    raise Exception("Error getting ranked data")
    
        # Create a embed to display the player's stats
        win_rate = (ranked_data[0]['wins'] / (ranked_data[0]['wins'] + ranked_data[0]['losses'])) * 100
        embed = discord.Embed(description="## League of Legends Stats for {}".format(username), color=0x9AC7A9)
        embed.add_field(name="📏 Level", value=player_data['summonerLevel'])
        embed.add_field(name="📈 Win/Loss", value=f"{ranked_data[0]['wins']}/{ranked_data[0]['losses']}")
        embed.add_field(name="🛡️ Rank", value=f"{ranked_data[0]['tier']} {ranked_data[0]['rank']}")
        embed.add_field(name="🪙 LPoints", value=ranked_data[0]['leaguePoints'])
        embed.add_field(name="📊 WinRate", value=f"{int(win_rate)}%")
    
        # Send the embed to the Discord channel
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_thumbnail(url="https://files.cults3d.com/uploaders/24095013/illustration-file/7b0008e2-c8f1-499e-baba-dc78ca79b12a/Untitled.png")
        await ctx.respond(embed=embed, view=twobuttonview(text="Op.gg", url=f"https://www.op.gg/summoners/{region}/{username}", text2="Blitz.gg", url2=f"https://blitz.gg/lol/profile/{region}/{username}", emoji2="📄", emoji="📄"))


def setup(bot):
    bot.add_cog(Fun(bot))
