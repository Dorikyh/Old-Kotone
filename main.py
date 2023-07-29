import sys, discord
import requests
import asyncio
from time import sleep
from traceback import print_exc
from os import environ, system
from datetime import datetime
from discord.ext import commands
from discord.ext.bridge import bridge_command
from threading import Thread
from discord.ext import bridge
import datetime


extensions = ["cogs.minecraft","cogs.economy", "cogs.spotify", "cogs.assets", "cogs.chess", "cogs.openai", "cogs.anime", "cogs.github", "cogs.gd", "cogs.system", "cogs.books", "cogs.nasa", "cogs.memes", "cogs.testing", "cogs.npm", "cogs.fun", "cogs.wikipedia", "cogs.reputation"]

statuses = [
  "Kotone is back!", "k/ChatGPT", "New Commands!", "Fixing Issues!",
  "Working on!", "/Chess", "Invite Kotone!", "/McFront", "Fixing Issues!",
  "The bot your server needs", "/Bitcoin", "78k+ Users!", "Check Mate!",
  "k/McPing" , "Leave a vote!", "Join Support Server", "/Help", "dsc.gg/kotone"
]

class Bot(bridge.Bot):
    def __init__(self):
        super().__init__(
            owner_id=841368898146402355,
            command_prefix="k/",
            intents=discord.Intents.all(),
            case_insensitive=True,
            help_command=None,

            allowed_mentions=discord.AllowedMentions(
                users=True,
                replied_user=False,
                roles=True,
                everyone=False
            ))



bot = Bot()

@bot.event
async def on_ready():
    print("\nKotone is online!\n")
    ip = requests.get('https://api.ipify.org').text
    await bot.get_channel(1104244458813403228).edit(name=f"📊︱Users: {sum([guild.member_count for guild in bot.guilds])}")
    await bot.get_channel(1099451934982803508).edit(name=f"📊︱Servers: {len(bot.guilds)}")
    print(ip)

    while True:
        for status in statuses:
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status, status=discord.Status.idle))

            await asyncio.sleep(40)




@bot.event
async def on_guild_join(guild):
    channel = bot.get_channel(1104857693749006448)  # Channel where the message will be sent

    # Create a new embed
    embed = discord.Embed(title="Kotone has a new home!", color=discord.Color.green())

    embed.add_field(name="Server name", value=f"{guild.name}")
    embed.add_field(name="Members", value=f"{guild.member_count}")
    embed.add_field(name="Guid ID", value=guild.id)
    embed.set_thumbnail(url=guild.icon)
  
    # Send the embed to the specified channel
    embed.set_footer(text=f"Guild owner: {guild.owner} ", icon_url=bot.user.avatar)
    embed.timestamp = datetime.datetime.utcnow()
    await channel.send(embed=embed) 
  


  
@bot.event
async def on_application_command(ctx):
    channel = bot.get_channel(1114304321622921226)  # Channel where the message will be sent

    # Create a new embed
    embed = discord.Embed(title=f"Slash command: {ctx.command}")

    # Add fields to the embed
    embed.add_field(name=ctx.guild, value=f"`{ctx.guild.id}`")
    embed.add_field(name=ctx.channel, value=f"`{ctx.channel.id}`")
    embed.set_footer(text=f"Executed by: {ctx.author.name}", icon_url=ctx.author.avatar.url)
    embed.timestamp = datetime.datetime.utcnow()

    await channel.send(embed=embed)  # Send the embed to the specified channel

class MyModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Short post title"))
        self.add_item(discord.ui.InputText(label="Large Description (Kotone.tech/feedback)", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(description='# Thank you, feedback sent!')
        embed.add_field(name=self.children[0].value, value=self.children[1].value)
        await interaction.response.send_message(embeds=[embed], ephemeral=True)
        await bot.get_channel(1103475571851276349).send(embed=embed)

class MyView(discord.ui.View):
    @discord.ui.button(label="Submit feedback")
    async def button_callback(self, button, interaction):
        await interaction.response.send_modal(MyModal(title="Help us to make Kotone better"))
        


@bot.event
async def on_command(ctx):
    channel = bot.get_channel(1114304321622921226)  # Channel where the message will be sent

    # Create a new embed
    embed = discord.Embed(title=f"Prefix command: {ctx.command}")

    # Add fields to the embed
    embed.add_field(name=ctx.guild, value=f"`{ctx.guild.id}`")
    embed.add_field(name=ctx.channel, value=f"`{ctx.channel.id}`")
    embed.set_footer(text=f"Executed by: {ctx.author.name}", icon_url=ctx.author.avatar.url)
    embed.timestamp = datetime.datetime.utcnow()
    
    await channel.send(embed=embed)  # Send the embed to the specified channel

@bot.event
async def on_application_command_error(ctx, exception):
  channel = bot.get_channel(1103475571851276349) 
  error_embed = discord.Embed(
            title="<:reject:1092153213093957692> An error occurred while executing that command", description=
            "The following error was caused by an internal failure. This error has been automatically reported to the development staff and is being resolved as soon as possible.", color=0xff0000)
  error_embed.add_field(name="Error Details", value=f"```{exception}```")
  error_embed.timestamp = datetime.datetime.utcnow()
  admin_embed = discord.Embed(title=f"<:reject:1092153213093957692> Error executed: {ctx.command}")
  admin_embed.add_field(name="Server", value=f"**{ctx.guild}** `{ctx.guild.id}`")
  admin_embed.add_field(name="Channel", value=f"**{ctx.channel}** `{ctx.channel.id}`")
  admin_embed.add_field(name="Error Details", value=f"```{exception}```", inline=False)
  admin_embed.timestamp = datetime.datetime.utcnow()
  await channel.send(embed=admin_embed)
  await ctx.reply(embed=error_embed, view=MyView(), ephemeral=True)

@bot.event
async def on_command_error(ctx, exception):
  channel = bot.get_channel(1103475571851276349) 
  error_embed = discord.Embed(
            title="<:reject:1092153213093957692> An error occurred while executing that command", description=
            "The following error was caused by an internal failure. This error has been automatically reported to the development staff and is being resolved as soon as possible.", color=0xff0000)
  error_embed.add_field(name="Error Details", value=f"```{exception}```")
  error_embed.timestamp = datetime.datetime.utcnow()
  admin_embed = discord.Embed(title=f"<:reject:1092153213093957692> Error executed: {ctx.command}")
  admin_embed.add_field(name="Server", value=f"**{ctx.guild}** `{ctx.guild.id}`")
  admin_embed.add_field(name="Channel", value=f"**{ctx.channel}** `{ctx.channel.id}`")
  admin_embed.add_field(name="Error Details", value=f"```{exception}```", inline=False)
  admin_embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
  admin_embed.timestamp = datetime.datetime.utcnow()
  await channel.send(embed=admin_embed)
  await ctx.reply(embed=error_embed)


@bot.event
async def on_guild_remove(guild):
    channel = bot.get_channel(1104857693749006448) 
    embed = discord.Embed(title="Kotone left a server!", color=discord.Color.red())

    # Add info to the embed
    embed.add_field(name="Server name", value=f"{guild.name}")
    embed.add_field(name="Members", value=f"{guild.member_count}")
    embed.add_field(name="Guid ID", value=guild.id)
    embed.set_thumbnail(url=guild.icon)
  
    # Send the embed to the specified channel
    embed.set_footer(text=f"Guild owner: {guild.owner}", icon_url=bot.user.avatar)
    embed.timestamp = datetime.datetime.utcnow()
    await channel.send(embed=embed) 

          
for extension in extensions:
  try:
    bot.load_extension(extension)
  except:
    print(f'Failed to load extension {extension[0]}.', file=sys.stderr)
    print_exc()


try:
    bot.loop.run_until_complete(bot.run(""))
except discord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests")
        for i in range(15, -1, -1):
            print(f"After {i} second, there will be an attempt to connect to discord servers.", end='\r', flush=False)
            sleep(1)
        system("clear")
        print("Reconnecting...")
        system("kill 1")
    else:
        raise e
