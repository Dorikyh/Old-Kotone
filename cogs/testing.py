import discord, asyncio
from discord.commands import slash_command, Option
import aiohttp
from discord.ext.bridge import bridge_command
import datetime
from utils import buttonview
import json
import time

description_text="Showing the list of commands of the selected category.\nAny troubles? join to [Support Server](https://discord.com/invite/appnkdReFk)"

class ReqView(discord.ui.View):
    def __init__(self, url):
        super().__init__()

        supportServerButton = discord.ui.Button(label='Request Link', style=discord.ButtonStyle.gray, url=url, emoji="📄")
        self.add_item(supportServerButton)

        self.url = url

    @discord.ui.button(label="Reload Request", style=discord.ButtonStyle.primary, emoji="📝")
    async def button_callback(self, button, interaction):
        async with aiohttp.ClientSession() as session:
            start_time = time.time()
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url) as response:
                    data = await response.json()
                    latency = time.time() - start_time  # Latencia en segundos
    
                    embed = discord.Embed(description="## HTTP Request", color=0xffe28a)
                    embed.add_field(name="Response", value=str(response.status), inline=True)
                    embed.add_field(name="Latency", value=f"{latency:.2f}s", inline=True)
                    embed.add_field(name="JSON", value=f"```json\n{json.dumps(data, indent=4)}\n```", inline=False)
                    embed.set_footer(text=f"Request by {interaction.user.name}", icon_url=interaction.user.avatar.url)
                    embed.timestamp = datetime.datetime.utcnow()
                    await interaction.response.edit_message(embed=embed, view=ReqView(self.url))

economy_info = [
    {
        "name": "<:slash:1094828379909402685> Balance",
        "description": "Get an user's current balance"
    },
    {
        "name": "<:slash:1094828379909402685> Claim",
        "description": "Get your daily bounty"
    },
    {
        "name": "<:slash:1094828379909402685> Transfer [user] [$]",
        "description": "Transfer coins to another user"
    }
]

commands_info = [
    {
        "name": "<:slash:1094828379909402685> Bitcoin",
        "description": "Get BTC value in USD."
    },
    {
        "name": "<:slash:1094828379909402685> Book [name]",
        "description": "Useful info about books"
    },
    {
        "name": "<:slash:1094828379909402685> GitHub [nick]",
        "description": "Info about GitHub user"
    },
    {
        "name": "<:slash:1094828379909402685> Wikipedia [article]",
        "description": "Read Wikipedia articles"
    },
    {
        "name": "<:slash:1094828379909402685> Seach [query]",
        "description": "Search images in google (wip)"
    },
]

deepmind_info = [
    {
        "name": "<:slash:1094828379909402685> ChatGPT [prompt] <style>",
        "description": "Use ChatGPT Turbo for free!"
    },
    {
        "name": "<:slash:1094828379909402685> Translate [lang] [prompt] <style>",
        "description": "Translate texts in any language"
    },
    {
        "name": "<:slash:1094828379909402685> Imagine [prompt]",
        "description": "Use Dall-e 2 to generate images"
    },
    {
        "name": "<:slash:1094828379909402685> Behavior [user]",
        "description": "This command is in Beta-Testing"
    },
    {
        "name": "<:slash:1094828379909402685> Shell [article]",
        "description": "Not yet..."
    },
    {
        "name": "<:slash:1094828379909402685> More soon",
        "description": "We are working hard to make more commands."
    },
]

fun_info = [
    {
        "name": "<:slash:1094828379909402685> Waifu",
        "description": "Get a pretty picture of random waifus"
    },
    {
        "name": "<:slash:1094828379909402685> NasaPhoto",
        "description": "The official Nasa photo of the day"
    },
    {
        "name": "<:slash:1094828379909402685> Meme <reddit>",
        "description": "Random meme (subreddit is optional)"
    },
    {
        "name": "<:slash:1094828379909402685> Cat",
        "description": "Get a random picture of a cat"
    }
]


minecraft_info = [
    {
        "name": "<:slash:1094828379909402685> McPing [address]",
        "description": "Get a Java Server info."
    },
    {
        "name": "<:slash:1094828379909402685> McSkin [username]",
        "description": "Get user's Avatar."
    },
    {
        "name": "<:slash:1094828379909402685> McBust [username]",
        "description": "Get Player's Bust"
    },
    {
        "name": "<:slash:1094828379909402685> McHead [nick]",
        "description": "Get Player's Skin Head"
    },
    {
        "name": "<:slash:1094828379909402685> McFront [username]",
        "description": "Get Player's nice photo"
    },
    {
        "name": "<:slash:1094828379909402685> McFace [username]",
        "description": "Get Player's nice photo"
    }
]


class MyView(discord.ui.View):
    @discord.ui.select(
        placeholder='Pick something to get help about it',
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(
                label='Help Embed',
                description='Back to help embed command',
                emoji='🏔️'),
            discord.SelectOption(
                label='Economy help',
                description='Get info about all the global economy',
                emoji='🌆'),
            discord.SelectOption(
                label='General Commands',
                description='Random commands that may be useful',
                emoji='🌠'),
            discord.SelectOption(
                label='Artificial Intelligence',
                description='AIs commands!',
                emoji='🤖'),
            discord.SelectOption(
                label='Minecraft Commands',
                description='Blocky command list',
                emoji='🌄'),
            discord.SelectOption(
                label='Fun Commands',
                description='Unique fun commands for everyone',
                emoji='🎡')
          
        ])

    async def select_callback(self, select, interaction):
        selected_option = select.values[0]
        if selected_option == "Economy help":
            embed = discord.Embed(
                title="🌆 Economy Commands",
                description=description_text,
                color=0xfff6c9)
            embed.set_thumbnail(url="https://em-content.zobj.net/thumbs/120/twitter/322/cityscape-at-dusk_1f306.png")
          
            for command in economy_info:
                embed.add_field(
                    name=command["name"],
                    value=f"<:info:1095874438173577297> {command['description']}\n", inline=True)
              
        elif selected_option == "General Commands":
            embed = discord.Embed(
                title="🌠 General Commands",
                description=description_text,
                color=0xeaebd6)
            embed.set_thumbnail(url="https://em-content.zobj.net/thumbs/160/twitter/214/shooting-star_1f320.png")
          
            for command in commands_info:
                embed.add_field(
                    name=command["name"],
                    value=f"<:info:1095874438173577297> {command['description']}\n", inline=True)
              
        elif selected_option == "Help Embed":
            embed = discord.Embed(
                title="Kotone Discord Bot", 
                description="Kotone is the bot your server needs. AI-Powered, Economy System, Minecraft Commands, Spotify Info, Brawl Stats and more!\nYou can use Kotone prefix `k/`, but we recommend using Slash Commands", color=0x7289da)
            embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/889540062956634164/b5391187966e16361ddb4a52b33ca1d8.png?size=1024")
            embed.set_author(name='Help Command', icon_url="https://cdn.discordapp.com/avatars/889540062956634164/b5391187966e16361ddb4a52b33ca1d8.png?size=1024")

        elif selected_option == "Minecraft Commands":
            embed = discord.Embed(
                title="🌄 Minecraft Commands",
                description=description_text,
                color=0xfae1ee
            )
            embed.set_thumbnail(url="https://i.ibb.co/74rbdnk/sunrise-emoji-by-twitter.png")
          
            for command in minecraft_info:
                embed.add_field(
                    name=command["name"],
                    value=f"<:info:1095874438173577297> {command['description']}\n", inline=True)
                

        elif selected_option == "Fun Commands":
            embed = discord.Embed(
                title="🎡 Fun Commands List",
                description=description_text,
                color=0xdaecf2
            )
            embed.set_thumbnail(url="https://em-content.zobj.net/thumbs/160/twitter/31/ferris-wheel_1f3a1.png")
            
            for command in fun_info:
                embed.add_field(
                    name=command["name"],
                    value=f"<:info:1095874438173577297> {command['description']}\n", inline=True)


        elif selected_option == "Artificial Intelligence":
            embed = discord.Embed(
                title="🤖 Artificial Intelligence Commands",
                description=description_text,
                color=0xdaecf2
            )
            embed.set_thumbnail(url="https://em-content.zobj.net/thumbs/160/twitter/31/ferris-wheel_1f3a1.png")
            
            for command in deepmind_info:
                embed.add_field(
                    name=command["name"],
                    value=f"<:info:1095874438173577297> {command['description']}\n", inline=True)

        embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar.url)
        embed.timestamp = datetime.datetime.utcnow()

        await interaction.response.edit_message(embed=embed)



class MyModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Short Input"))
        self.add_item(discord.ui.InputText(label="Long Input", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Modal Results")
        embed.add_field(name="Short Title", value=self.children[0].value)
        embed.add_field(name="Long Input", value=self.children[1].value)
        await interaction.response.send_message(embeds=[embed])

async def send_message(ctx, message: str):
    await asyncio.sleep(10)
    await ctx.reply(message)


class MyViewe(discord.ui.View):
    @discord.ui.button(label="Send Modal")
    async def button_callback(self, button, interaction):
        await interaction.response.send_modal(MyModal(title="Modal via Button"))


class Testing(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @bridge_command(description="📝 HTTP JSON request.")
    async def http(self, ctx, url):
        try:
            start_time = time.time()
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    data = await response.json()
                    latency = time.time() - start_time  # Latencia en segundos
    
                    embed = discord.Embed(description="## HTTP Request", color=0xffe28a)
                    embed.add_field(name="Response", value=str(response.status), inline=True)
                    embed.add_field(name="Latency", value=f"{latency:.2f}s", inline=True)
                    embed.add_field(name="JSON", value=f"```json\n{json.dumps(data, indent=4)}\n```", inline=False)
                    embed.set_footer(text=f"Request by {ctx.author.name}", icon_url=ctx.author.avatar.url)
                  
                    await ctx.reply(embed=embed, view=ReqView(url))
    
        except Exception as e:
            await ctx.reply(f'Error: {e}')
    

    

    @bridge_command(description="📓 All available info about Kotone bot")
    async def help(self, ctx):
      embed = discord.Embed(title="Kotone Discord Bot", description="Kotone is the bot your server needs. AI-Powered, Economy System, Minecraft Commands, Spotify Info, Brawl Stats and more!\nYou can use Kotone prefix `k/`, but we recommend using Slash Commands.\n[Support server](https://discord.com/invite/appnkdReFk) | [Kotone Website](https://gg.gg/kotone)", color=0x7289da)
      embed.set_thumbnail(url=self.bot.user.avatar)
      embed.set_author(name='Help Command', icon_url=self.bot.user.avatar.url)
      embed.timestamp = datetime.datetime.utcnow()
      embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
      await ctx.reply(embed=embed, view=MyView(timeout=None))


      

def setup(bot):
    bot.add_cog(Testing(bot))
