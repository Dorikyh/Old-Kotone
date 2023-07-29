import discord
import os
from discord.ext import commands
from discord.ext.bridge import bridge_command
from discord.commands import slash_command, user_command, guild_only, Option, SlashCommandGroup
from utils import twobuttonview
import aiohttp
import datetime
import asyncio

CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = 'http://localhost:8000/callback/'

class SpotiView(discord.ui.View):
    def __init__(self, url):
        super().__init__()
        self.add_item(discord.ui.Button(label="Open in Spotify", url=url, emoji="<:spoti:1099419471187296357>"))

class Spotify(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.access_token = None
        self.token_expires_at = None
        self.refresh_task = None

    async def refresh_token(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                'https://accounts.spotify.com/api/token',
                data={
                    'grant_type': 'client_credentials',
                    'client_id': CLIENT_ID,
                    'client_secret': CLIENT_SECRET
                }
            ) as resp:
                data = await resp.json()
                self.access_token = data['access_token']
                expires_in = data['expires_in']
                self.token_expires_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
                print(f'Token refreshed at {self.token_expires_at}')

    async def start_refresh_task(self):
        while not self.bot.is_closed():
            if self.token_expires_at is None or datetime.datetime.utcnow() > self.token_expires_at:
                await self.refresh_token()
            await asyncio.sleep(3600)

        
    @commands.Cog.listener()
    async def on_ready(self):
        print("[✔️] Spotify loaded successfully")  

  
    @bridge_command(description="🔊 Useful info about your favorite song")
    @discord.option("track", description="Enter the song name: (Spotify)")
    async def track(self, ctx, *, song):
        await self.refresh_token()
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
        }
    
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.spotify.com/v1/search?q={song}&type=track&limit=1", headers=headers
            ) as resp:
                data = await resp.json()
                print(data)
  
      # Extract the details of the first song in the search results
        song = data["tracks"]["items"][0]
  
      # Create an Embed object to send the song information
        if song["explicit"] == True:
          embed = discord.Embed(
            title="🅴 " + song["name"],
            description=f"Song by {', '.join([artist['name'] for artist in song['artists']])}",
            color=0x8080ff,
      )
        else:
      
          embed = discord.Embed(
            title="<:music:1123326615800254484> " + song["name"],
            description=f"Song by {', '.join([artist['name'] for artist in song['artists']])}",
            color=0x8080ff,
        )
        
        embed.set_thumbnail(url=song["album"]["images"][0]["url"])
        embed.add_field(
          name="Length",
          value=f"{int(song['duration_ms'] / 1000 // 60)}:{int(song['duration_ms'] / 1000 % 60)}",
      )
        embed.add_field(name="Popularity", value=song["popularity"])
        embed.add_field(name="Album", value=song["album"]["name"])
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
        embed.timestamp = datetime.datetime.utcnow()
      
  
        await ctx.reply(embed=embed, view=twobuttonview(
          text="Play on Spotify", url="https://google.com",
          text2="Analysis", url2="https://google.com", emoji="🎶", emoji2="🎼"))
  

    


def setup(bot):
    bot.add_cog(Spotify(bot))
