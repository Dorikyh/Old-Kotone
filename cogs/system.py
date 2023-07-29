import discord
import datetime
from discord.ext import commands
from discord.commands import slash_command, user_command, guild_only, Option, SlashCommandGroup
from utils import voteview
from utils import supportview
from discord.ext.bridge import bridge_command
import psutil
from utils import format_number


class System(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        start_time=datetime.datetime.utcnow()
      
    @commands.Cog.listener()
    async def on_ready(self):
      try:
        print("[✔️] System loaded successfully") 
      except:
        print("[-] System was not loaded successfully")
        
    start_time=datetime.datetime.utcnow()
  

    @bridge_command(description="⚙️ Kotone System Info")
    async def system(self, ctx):
          
        cpu_percent = psutil.cpu_percent()
        ram_percent = psutil.virtual_memory().percent
    
        # Get total users and totald guilds
        total_servers = len(self.bot.guilds)
        total_users = sum([guild.member_count for guild in self.bot.guilds])
    
        # Get uptime value
        uptime = datetime.datetime.utcnow() - self.start_time
    
        embed = discord.Embed(description="## Kotone Status\nDisplaying Kotone system",
                              colour=0x7289da)
        embed.add_field(name="<:CPU:1097358919745142825> CPU",
                        value=f"`{cpu_percent}%`",
                        inline=True)
      
        embed.add_field(name="<:xram:1097358889755869376> RAM",
                        value=f"`{ram_percent}%`",
                        inline=True)
      
        embed.add_field(name=":floppy_disk: PyCord",
                        value="`v"+discord.__version__+"`",
                        inline=True)
      
        embed.add_field(name="<:bdiscord:1094835795090735124> Servers",
                        value=f"{total_servers}/75",
                        inline=True)
      
        embed.add_field(name="<:users:1119816900550074439> Users",
                        value=f"{format_number(total_users)}",
                        inline=True)
      
        embed.add_field(name="<:clock:1123327374910570597> Uptime",
                        value=f"{uptime.seconds // 3600}h, {uptime.seconds % 3600 // 60}m",
                        inline=True)
    
        embed.set_thumbnail(url=self.bot.user.avatar)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
        await ctx.respond(embed=embed, view=supportview())



def setup(bot):
    bot.add_cog(System(bot))
