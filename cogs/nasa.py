import discord
import os
from discord.ext import commands
import requests
from discord.ext.bridge import bridge_command
from discord.commands import slash_command, Option
from utils import buttonview
import datetime
import aiohttp


from discord.ui import Button, View
class ImgButton(discord.ui.View):
    def __init__(self, query, results):
        super().__init__()

        self.query = query
        self.results = results
        self.current_index = 0

        imagelink = discord.ui.Button(label="Image", style=discord.ButtonStyle.gray, url=results[0]["link"], emoji="📄")
        self.add_item(imagelink)

    async def show_image(self, index, interaction):
        if 0 <= index < len(self.results):
            result = self.results[index]
            enlace_imagen = result["link"]

            embed = discord.Embed(title="Google Image Search", description=self.query)
            embed.set_image(url=enlace_imagen)
            embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar.url)
            embed.timestamp = datetime.datetime.utcnow()

            await interaction.response.edit_message(embed=embed)
            self.current_index = index

    @discord.ui.button(label="Prev", style=discord.ButtonStyle.primary, emoji="◀️")
    async def prev_button_callback(self, button, interaction):
        await self.show_image(self.current_index - 1, interaction)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary, emoji="▶️")
    async def next_button_callback(self, button, interaction):
        await self.show_image(self.current_index + 1, interaction)


class Nasa(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog 'Template' loaded successfully")  
    

    @bridge_command(description="🗒 Google Image Search")
    @discord.option("query", description="Enter the search to Google it:")
    async def search(self, ctx, *, query):
        clave_api = ""
        cx = ""  # El ID de búsqueda personalizada (cx) que creaste en la Consola de Desarrolladores de Google

        url = f"https://www.googleapis.com/customsearch/v1?key={clave_api}&cx={cx}&searchType=image&q={query}&safe=active"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                datos = await response.json()
                
                print(datos)

                if "items" in datos:
                    results = datos["items"]

                    if results:
                        embed = discord.Embed(title="Google Image Search", description=query)
                        embed.set_image(url=results[0]["link"])
                        view = ImgButton(query, results)
                        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
                        embed.timestamp = datetime.datetime.utcnow()
                        await ctx.reply(embed=embed, view=view)
                    else:
                        await ctx.reply("Image not found")
                else:
                    await ctx.reply("Error occurred while searching for images")
                    
                    


def setup(bot):
    bot.add_cog(Nasa(bot))

