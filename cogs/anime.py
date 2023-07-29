import discord
import json
from discord.ext import commands
from discord.commands import slash_command, Option
import requests
import datetime
import random
from discord.ui import View
from discord.ext.bridge import bridge_command

class AnimeView(discord.ui.View):
    def __init__(self):
        super().__init__()

        supportServerButton = discord.ui.Button(label='More Pictures', style=discord.ButtonStyle.gray, url='https://discord.com', emoji="📄")
        self.add_item(supportServerButton)

    @discord.ui.button(label="Reload Image", style=discord.ButtonStyle.primary, emoji="📝")
    async def button_callback(self, button, interaction):
        response = requests.get("https://api.waifu.pics/sfw/waifu")
        data = json.loads(response.content)

        embed = discord.Embed(description="## Random Waifu", color=0x7289da)
        embed.set_image(url=data['url'])

        embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar.url)
        embed.timestamp = datetime.datetime.utcnow()

        # Update the embed with the new image.
        if button.label == "Reload Image":
            embed.set_image(url=data['url'])

        await interaction.response.edit_message(embed=embed)



    
class Anime(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("[✔️] Anime was loaded successfully")  

    @bridge_command(description="💖 Anime waifu")
    async def waifu(self, ctx):
            response = requests.get("https://api.waifu.pics/sfw/waifu")
            data = json.loads(response.content)
            photo = data['url']

            embed = discord.Embed(description="## Random Waifu", color=0x7289da)
            embed.set_image(url=photo)

            embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.respond(embed=embed, view=AnimeView())

def setup(bot):
    bot.add_cog(Anime(bot))