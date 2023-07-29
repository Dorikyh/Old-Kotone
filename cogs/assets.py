import discord
import datetime
import requests
from forex_python.bitcoin import BtcConverter
from discord.ext import commands
from discord.commands import slash_command, user_command, Option
from utils import buttonview
from utils import check_balance
from discord.ext.bridge import bridge_command

class Assets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        start_time=datetime.datetime.utcnow()
      
    @commands.Cog.listener()
    async def on_ready(self):
        print("[✔️] Assets loaded successfully") 
    start_time=datetime.datetime.utcnow()
  

    
    @bridge_command(description="💴 Get Bitcoin value")
    async def bitcoin(self, ctx):
      if await check_balance(ctx, 1):
        b = BtcConverter()  # force_decimal=True to get Decimal rates
        val = "{:,.2f}".format(b.get_latest_price('USD'))
    
        embed = discord.Embed(
          description=f"# Bitcoin value\nRight now the bitcoin value is:\n### ${val}",
          color=0xb3e6b5)
        embed.set_thumbnail(url="https://cdn.freebiesupply.com/logos/large/2x/bitcoin-logo-png-transparent.png")
        embed.set_footer(text=f"Finance API | Request by {ctx.author.name}", icon_url=ctx.author.avatar.url)
        embed.timestamp = datetime.datetime.utcnow()
        view=buttonview(text="More info", url="https://www.google.com/finance/quote/BTC-USD", emoji="💴")
        await ctx.respond(embed=embed, view=view)
    
    

    
  
        
def setup(bot):
    bot.add_cog(Assets(bot))
