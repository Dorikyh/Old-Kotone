import discord
import aiohttp
import json
import requests
from discord.ext.bridge import bridge_command
from discord.ext import commands
from discord.commands import slash_command, user_command, guild_only, Option, SlashCommandGroup
from utils import buttonview
import datetime

class GitHub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge_command(description="🗃️ Github User account data")
    @discord.option("username", description="Enter your Github nickname:")
    async def github(self, ctx, username: str):
        async with aiohttp.ClientSession() as session:
          
            async with session.get(f"https://api.github.com/users/{username}") as response:
                data = await response.json()

                embed = discord.Embed(description=f"## GitHub profile: {data['login']}\n{data['bio']}", color=0xffdfba)
        
                embed.set_thumbnail(url=data['avatar_url'])
                embed.add_field(name=":spy: Username", value=data['name'] or "No disponible", inline=True)
                embed.add_field(name=":map: Location", value=data['location'] or "No disponible", inline=True)
                embed.add_field(name=":file_folder: Repos", value=str(data['public_repos']), inline=True)
                embed.add_field(name=":envelope: Followers", value=str(data['followers']), inline=True)
                embed.add_field(name=":envelope_with_arrow: Following", value=str(data['following']), inline=True)
                embed.add_field(name=":bookmark: Website", value=str(data['blog']), inline=True)
                embed.set_footer(text=f"GitHub ID: {data['id']} | Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
                
                embed.timestamp = datetime.datetime.utcnow()
                

                response = requests.get("https://github-readme-tech-stack.vercel.app/api/cards?title=Dorikyh%20Profile&lineCount=1&line1=python,python,4c77b1;javascript,javascript,bbc253;")
                

                view=buttonview(text="GitHub Profile", url=f"http://www.github.com/{username}", emoji="<:github:1104632918195838976>")

                await ctx.respond(embed=embed, view=view)


def setup(bot):
    bot.add_cog(GitHub(bot))