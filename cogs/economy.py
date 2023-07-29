import os
import datetime
import json
import discord
from discord.ext import commands
from discord.ext.bridge import bridge_command
from utils import buttonview

def check_balance(economy, user_id):
    if user_id not in economy:
        economy[user_id] = 10

def update_balance(economy, user_id, amount, action):
    if action == "add":
        economy[user_id] += amount
    elif action == "subtract":
        economy[user_id] -= amount

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if not os.path.exists("economy.json"):
            with open("economy.json", "w") as f:
                f.write("{}")
        
        if not os.path.exists("claimed.json"):
            with open("claimed.json", "w") as f:
                f.write("{}")

    @commands.Cog.listener()
    async def on_ready(self):
        print("[✔️] Economy was loaded successfully")

    @bridge_command(description="💸 Transfer coins to another user")
    async def transfer(self, ctx, recipient: discord.Member, amount: int):
        if amount <= 0:
            await ctx.send("You must transfer a positive amount of coins!")
            return

        sender_id = str(ctx.author.id)
        recipient_id = str(recipient.id)

        with open("economy.json", "r") as f:
            economy = json.load(f)

        check_balance(economy, sender_id)
        check_balance(economy, recipient_id)

        if economy[sender_id] < amount:
            await ctx.send("You don't have enough coins to make this transfer!")
            return

        economy[sender_id] -= amount
        economy[recipient_id] += amount

        with open("economy.json", "w") as f:
            json.dump(economy, f)

        sender_name = ctx.author.name
        recipient_name = recipient.name

        embed = discord.Embed(
            title=":money_with_wings: Transaction successful!",
            description=f"{sender_name} transferred {amount} coins to {recipient_name}.",
            color=0xffdfba
        )
        embed.set_thumbnail(url=ctx.author.avatar.url)
        embed.timestamp = datetime.datetime.utcnow()

        await ctx.reply(embed=embed)

    @bridge_command(description="💴 Claim your daily bounty!")
    async def claim(self, ctx):
        try:
            user_id = str(ctx.author.id)
            with open("claimed.json", "r") as f:
                claimed = json.load(f)

            if user_id in claimed:
                last_claimed = datetime.datetime.fromisoformat(claimed[user_id])
                time_diff = datetime.datetime.utcnow() - last_claimed
                if time_diff < datetime.timedelta(hours=12):
                    time_remaining = datetime.timedelta(hours=12) - time_diff
                    embed = discord.Embed(
                        title="<:reject:1092153213093957692> Denied Command",
                        description=f"You need to wait {time_remaining.seconds//3600} hour(s) and {(time_remaining.seconds%3600)//60} minute(s) before claiming again.",
                        color=0x8080ff
                    )
                    embed.timestamp = datetime.datetime.utcnow()
                    await ctx.reply(embed=embed, ephemeral=True)
                    return

            with open("economy.json", "r") as f:
                economy = json.load(f)

            check_balance(economy, user_id)

            claimed[user_id] = datetime.datetime.utcnow().isoformat()

            with open("claimed.json", "w") as f:
                json.dump(claimed, f)

            update_balance(economy, user_id, 5, "add")

            with open("economy.json", "w") as f:
                json.dump(economy, f)

            embed = discord.Embed(
                title="<:check:1092153125030334494> Successfully claimed",
                description=f"You have claimed 5 coins! You now have {economy[user_id]} coins.",
                color=0x8080ff
            )
            embed.set_footer(
                text=f"Requested by {ctx.author.name}",
                icon_url=ctx.author.avatar.url
            )
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.reply(embed=embed, view=buttonview(text="Get more credits!", url="https://discord.com/invite/appnkdReFk", emoji="<:credits:1122975107900522588>"))

        except Exception as e:
            print(f"Error: {e}")

    @bridge_command(description="👤 Get a user's current balance")
    async def balance(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        user_id = str(user.id)

        with open("economy.json", "r") as f:
            economy = json.load(f)

        check_balance(economy, user_id)

        thumbnail_url = user.avatar.url if user.avatar else "https://i.pinimg.com/736x/be/3d/c6/be3dc6963cb06aed4f194b8d0029f213.jpg"

        embed = discord.Embed(
            title="<:credits:1122975107900522588> Credit Balance",
            description=f"<:bdiscord:1094835795090735124> {user.name}: {economy[user_id]} credits.",
            color=0x7289da
        )
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_thumbnail(url=thumbnail_url)

        await ctx.reply(embed=embed)

def setup(bot):
    bot.add_cog(Economy(bot))

