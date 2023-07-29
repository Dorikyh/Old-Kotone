import discord
import json
from discord.ext import commands
from discord.commands import slash_command, user_command, guild_only, Option, SlashCommandGroup
import aiohttp
import datetime
from discord.ext.bridge import bridge_command
from utils import buttonview
from utils import format_number



class Chess(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("[✔️] Chess was loaded successfully")  

    @bridge_command(description="♟️ Chess.com player data")
    @discord.option("book_name", description="Enter your Chess.com nickname:")
    async def chess(self, ctx, username):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.chess.com/pub/player/{username}") as response:
                data = await response.json()
                profile_data = data
    
                stats_response = await session.get(f"https://api.chess.com/pub/player/{username}/stats")
                data = await stats_response.json()
                stats_data = data
    
        name = profile_data['name'].title()
        country = profile_data['country'].lower()
    
        joined_date = datetime.datetime.fromtimestamp(profile_data['joined']).strftime('%m/%d/%y')
    
        blitz_elo = stats_data["chess_blitz"]["last"]["rating"]
        blitz_wins = stats_data["chess_blitz"]["record"]["win"]
        blitz_loss = stats_data["chess_blitz"]["record"]["loss"]
        blitz_draw = stats_data["chess_blitz"]["record"]["draw"]
    
        embed = discord.Embed(title=f"<:chess:1104192772107411467> Chess.com player info", color=0xbaffc9, description=f":flag_{country[-2:]}: {name}")
        embed.set_thumbnail(url=profile_data['avatar'])
        embed.add_field(name=":bust_in_silhouette: Player", value=username.title(), inline=True)
        embed.add_field(name=":date: Joined", value=joined_date, inline=True)
        embed.add_field(name=":two_hearts: Followers", value=format_number(profile_data['followers']), inline=True)
        embed.add_field(name=":zap: Blitz Elo", value=blitz_elo, inline=True)
        embed.add_field(name=":zap: Blitz Stats", value=f"{blitz_wins}/{blitz_loss}/{blitz_draw}", inline=True)
        embed.add_field(name=":trophy: League", value=profile_data['league'], inline=True)
        embed.set_footer(text=f'Player ID: {profile_data["player_id"]}', icon_url=self.bot.user.avatar.url)
        embed.timestamp = datetime.datetime.utcnow()
        view = buttonview(text="Chess.com Profile", url=profile_data['url'], emoji="♟️")
        await ctx.respond(embed=embed, view=view)
    

def setup(bot):
    bot.add_cog(Chess(bot))
