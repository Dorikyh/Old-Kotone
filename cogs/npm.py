import discord
from discord.ext import commands
from discord.commands import slash_command, Option
from utils import fetch_json
from utils import twobuttonview
from discord.ext.bridge import bridge_command
import datetime

class NPM(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog 'NPM' loaded successfully")  

    @bridge_command(description="🛰️ Node Package Manager") 
    async def npm(self, ctx, package):
        json_data = await fetch_json(f'https://apiv1.spapi.ga/fun/npm?pkg=´{package}')
        data = json_data['package']
        embed = discord.Embed(description=f"## Package: {data['name']}\n{data['description']}", color=0xd9534f)
        embed.set_thumbnail(url="https://www.npmjs.com/npm-avatar/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdmF0YXJVUkwiOiJodHRwczovL3MuZ3JhdmF0YXIuY29tL2F2YXRhci80NmQ4ZDAwZTE5MGJlNjQ3MDUzZjdkOTdmZDA0NzhlND9zaXplPTQ5NiZkZWZhdWx0PXJldHJvIn0.5nKe6nJhOqDvUG6NzyDo5HVNm_RiThxzGMbRgg2P0Ls")
        embed.add_field(name="Author", value=data['name'])
        embed.add_field(name="Version", value=data['version'])
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.reply(embed=embed, view=twobuttonview(text="Package", url=data['links']['npm'], emoji="🗃️", text2="Website", url2=data['links']['homepage'], emoji2="📓"))
def setup(bot):
    bot.add_cog(NPM(bot))