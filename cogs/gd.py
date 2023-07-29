import discord
import aiohttp
from discord.ext import commands
from discord.commands import slash_command, user_command, guild_only, Option, SlashCommandGroup
from utils import buttonview
import datetime
import requests
import random


class Dash(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("GD loaded successfully")  
    
    @slash_command(name="dasher", description="🎀 Get data about a Geometry Dash Player (WIP)")
    async def dasher(self, ctx, username: Option(str, description="Enter your Geometry Dash nickname:")):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://gdbrowser.com/api/profile/{username}") as response:
                if response.status == 200:
                    data = await response.json()

                    embed = discord.Embed(title=f"Geometry Dasher: {data['username']}", color=discord.Color.from_rgb(data['col1RGB']['r'], data['col1RGB']['g'], data['col1RGB']['b']))
                    embed.add_field(name="Total Stars", value=data["stars"], inline=False)
                    embed.add_field(name="Total Diamonds", value=data["diamonds"], inline=False)
                    embed.set_footer(text=f"User ID: {data['playerID']}")
                    view = buttonview(text="More Info", url=f"https://gdbrowser.com/u/{username}", emoji="<:gd:1108477889176932373>")
                    
                    embed.timestamp = datetime.datetime.utcnow()
                    await ctx.respond(embed=embed, view=view)
                else:
                    await ctx.respond("No se pudo obtener información del jugador.")


    
def setup(bot):
    bot.add_cog(Dash(bot))