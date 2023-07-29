import discord
from discord.ext import commands
from discord.commands import slash_command, user_command, guild_only, Option, SlashCommandGroup
from utils import buttonview
from discord.ext.bridge import bridge_command
import requests
from mcstatus import JavaServer
import datetime
import traceback
from discord.commands import Option

class MyViewo(discord.ui.View):
    def __init__(self, address):
        super().__init__()
        self.address = address
        url = f"https://mcsrvstat.us/server/{self.address}"
        self.add_item(discord.ui.Button(label="More info", url=url, emoji="<:mc:1092151701856866324>"))
  
    @discord.ui.button(label="Ping again", style=discord.ButtonStyle.primary, emoji="<:tasks:1096883657525964801>")
    async def button_callback(self, button, interaction):
        server = JavaServer.lookup(self.address)
        status = server.status()
      
        url = f"https://api.mcsrvstat.us/2/{self.address}"
        response = requests.get(url)
        data = response.json()
        version = data["version"]
        embed = discord.Embed(
            description=f"## Minecraft Java Server\n<:server:1092154131310985347> **IP: **{self.address}\n<:mc_earth:1096881148367482890> ** Version: **{version}\n<:members:1091982908027310150> **Online: **{status.players.online}\n<:latency:1092152184231178353> **Latency: **{int(status.latency)}ms",
                    color=0x8080ff)
      
        embed.set_thumbnail(url=f"https://eu.mc-api.net/v3/server/favicon/{self.address}")
        embed.set_footer(text=f"Requested by {interaction.user.name}", icon_url=interaction.user.avatar.url)
        embed.set_image(url=f"https://sr-api.sfirew.com/server/{self.address}/banner/motd.png")
        embed.timestamp = datetime.datetime.utcnow()
        await interaction.response.edit_message(embed=embed)


class namemcview(discord.ui.View):
        def __init__(self, username):
          super().__init__()
      
          url = f"https://en.namemc.com/profile/{username}.1"
      
          self.add_item(discord.ui.Button(label="Namemc Profile", url=url, emoji="📄"))

  
        
class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("[✔️] Minecraft was loaded successfully!")  

    @bridge_command(description="👤 Minecraft Skin Body")
    @discord.option("username", description="Enter your Minecraft nickname:")
    async def mcbody(self, ctx, username):
        response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")

        if response.ok:
          data = response.json()
          uuid = data["id"]
        else:
          await ctx.respond("Error al obtener la información del jugador.")
            
        embed = discord.Embed(title="<:mc:1092151701856866324> Minecraft User Body", color=0x7289da)
        embed.set_image(url=f"https://visage.surgeplay.com/full/256/{uuid}")
        embed.timestamp = datetime.datetime.utcnow()
        view = namemcview(username=username)
        await ctx.respond(embed=embed, view=view)
    
    
    
    @bridge_command(description="👤 Minecraft user Bust")
    @discord.option("username", description="Enter your Minecraft nickname:")
    async def mcbust(self, ctx, username):
        embed = discord.Embed(description="## Minecraft User Bust", color=0x7289da)
        embed.set_image(url=f"https://minotar.net/armor/bust/{username}/256")
        embed.timestamp = datetime.datetime.utcnow()
        view = namemcview(username=username)
        await ctx.respond(embed=embed, view=view)
    
    
    
    @bridge_command(description="👤 Minecraft Skin Face")
    @discord.option("username", description="Enter your Minecraft nickname:")
    async def mcface(self, ctx, username):
        embed = discord.Embed(
          description="## Minecraft User Face", color=0x7289da)
        
        embed.set_image(url=f"https://minotar.net/helm/{username}/256")
        embed.set_footer(text=f"Request by {ctx.author.name}", icon_url=ctx.author.avatar.url)
        embed.timestamp = datetime.datetime.utcnow()
        view = namemcview(username=username)
        await ctx.respond(embed=embed, view=view)

    @bridge_command(description="👤 Minecraft Skin Head")
    @discord.option("username", description="Enter your Minecraft nickname:")
    async def mchead(self, ctx, username):
        embed = discord.Embed(description="## Minecraft Skin Head", color=0x7289da)
        response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
      
        data = response.json()
        uuid = data["id"]

        embed.set_image(url=f"https://visage.surgeplay.com/head/256/{uuid}")
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
        embed.timestamp = datetime.datetime.utcnow()
        view = namemcview(username=username)
        await ctx.reply(embed=embed, view=view)
    
    @bridge_command(description="👤 Minecraft Skin Front")
    @discord.option("username", description="Enter your Minecraft nickname:")
    async def mcfront(self, ctx, username):
            response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
          
            if response.ok:
                data = response.json()
                uuid = data["id"]
            else:
                await ctx.respond("Error al obtener la información del jugador.")
            
            embed = discord.Embed(description="## Minecraft User Front", color=0x7289da)
            embed.set_image(url=f"https://visage.surgeplay.com/bust/256/{uuid}.png")
            embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
            embed.timestamp = datetime.datetime.utcnow()
            view = namemcview(username=username)
            await ctx.respond(embed=embed, view=view)

  
    @bridge_command(description="📡 Minecraft Server info")
    @discord.option("address", description="Enter a Minecraft Java address:")
    async def mcping(self, ctx, address):
                url = f"https://api.mcsrvstat.us/2/{address}"
                response = requests.get(url)
                data = response.json()
  
                if data["version"]:
                  version = data["version"]
                else:
                  version = "Unknown"
                  
                server = JavaServer.lookup(address)
                status = server.status()
                embed = discord.Embed(description=f"## Minecraft Java Server\n<:link:1119816801241534495> **IP: **{address}\n<:box:1119818833939664916> **Version: **{version}\n<:users:1119816900550074439> **Online: **{status.players.online}\n<:ping:1119817447839629412> **Latency: **{int(status.latency)}ms",
                    color=0x8080ff)
      
                embed.set_thumbnail(url=f"https://eu.mc-api.net/v3/server/favicon/{address}")
                embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
                embed.set_image(url=f"https://sr-api.sfirew.com/server/{address}/banner/motd.png")
      
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.respond(embed=embed, view=MyViewo(address))
    
    
   

def setup(bot):
    bot.add_cog(Minecraft(bot))
