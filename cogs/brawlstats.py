import discord
import brawlstats
import datetime, os
from discord.ext import commands
from discord.ext.bridge import bridge_command
from discord.commands import slash_command, user_command, guild_only, Option
from utils import check_balance
from utils import buttonview


client = brawlstats.Client("")

class BrawlStats(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog 'Template' loaded successfully")  



    @bridge_command(description="Info about a Brawl Stars player")
    @discord.option("tag", description="Enter player's tag (ex: PQQJ08GR9)", type=str)
    async def brawlstats(self, ctx, tag):
    
      if await check_balance(ctx, 1):
        try:
            player = client.get_profile(tag)
        except Exception as e:
            error_embed = discord.Embed(title="Error", description=str(e))
            await ctx.respond(embed=error_embed)
            return
    
        embed = discord.Embed(title=f"<:brawl:1099839698597314590> Brawl Stats About {player.name}", description=f"Player Tag: {player.tag}", colour=0x8080ff)
        embed.add_field(name="<:trophies:1099837812532064307> Trophies", value=f"{player.trophies}")
        embed.add_field(name="<:showdown:1099858361480122489> Solo wins", value=f"{player.solo_victories}")
        embed.add_field(name="<:brawlevel:1099858292630622311> EXP Level", value=f"{player.exp_level}")
        view = buttonview(url=f"https://brawlstats.com/profile/{tag}", emoji="<:trophies:1099837812532064307>", text="More info")
        embed.set_thumbnail(url="https://d2u1q3j7uk6p0t.cloudfront.net/jPMis1QstwmqA3yv7lENNKmVlgsxs3VxgcUNbkl9VWsHSXxHKJ2SaaKAlH2ONtqOZeaV=w64")
        embed.set_footer(text=f"Request by {ctx.author.name}", icon_url=ctx.author.avatar.url)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.respond(embed=embed, view=view)
        
def setup(bot):
    bot.add_cog(BrawlStats(bot))
