import discord
import datetime
from discord.ext import commands
from discord.commands import slash_command, user_command, Option
import aiohttp
from utils import twobuttonview
from discord.ext.bridge import bridge_command


class Wikipedia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
      
    @commands.Cog.listener()
    async def on_ready(self):
        print("[✔️] Wikipedia loaded successfully") 

  
    @bridge_command(description="📜 Wikipedia Article Data")
    async def wikipedia(self, ctx, query):
        formatted_query = query.title().replace(" ", "_")

    
        async with aiohttp.ClientSession() as session:
            url_summary = f"c"
            url_media_list = f"https://en.wikipedia.org/api/rest_v1/page/media-list/{formatted_query}"
            
            async with session.get(url_summary) as response_summary, session.get(url_media_list) as response_media:
                data_summary = await response_summary.json()
                data_media = await response_media.json()
        
        image_url = data_media['items'][0]['srcset'][0]['src']
        image_url = image_url[2:]
        
        embed = discord.Embed(description=f"## Wikipedia: {data_summary['titles']['normalized']}\n"+data_summary['description'],
                              color=0xbe9b7b)
      
        embed.set_thumbnail(url="https://"+image_url)
        embed.timestamp = datetime.datetime.utcnow()
        embed.add_field(name="📄 Large Description", value=data_summary['extract'])
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=embed, view=twobuttonview(text="Wikipedia", url=data_summary['content_urls']['desktop']['page'],
                                                       text2="References", url2=data_summary['content_urls']['desktop']['page']+"#References", emoji="<:wikipedia:1117208176501203089>", emoji2="📝"))
    
        


def setup(bot):
    bot.add_cog(Wikipedia(bot))
