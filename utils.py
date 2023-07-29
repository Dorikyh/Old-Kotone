import discord
import os
import json
import datetime
import aiohttp
 
def owner_check(user_id):
  if user_id == 841368898146402355:
    return True

def format_number(number):
    if number >= 1000000:
        return str(round(number/1000000, 2)) + "m"
    elif number >= 1000:
        return str(round(number/1000, 1)) + "k"
    else:
        return str(number)

async def fetch_json(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

class buttonview(discord.ui.View):
        def __init__(self, text, url, emoji):
          super().__init__()
      
          self.add_item(discord.ui.Button(label=text, url=url, emoji=emoji))

class twobuttonview(discord.ui.View):
        def __init__(self, text, url, text2, url2, emoji, emoji2):
          super().__init__()
      
          self.add_item(discord.ui.Button(label=text, url=url, emoji=emoji))
          self.add_item(discord.ui.Button(label=text2, url=url2, emoji=emoji2))


class supportview(discord.ui.View):

  def __init__(self):
    super().__init__()

    url = "https://discord.com/invite/appnkdReFk"

    self.add_item(discord.ui.Button(label="Support Server", url=url, emoji="<:discord:1092152451836166145>"))
    self.add_item(discord.ui.Button(label="Website", url="https://top.gg/bot/889540062956634164", emoji="<:kotone:1095174885346644080>"))



class voteview(discord.ui.View):

  def __init__(self):
    super().__init__()

    url = "https://top.gg/bot/889540062956634164/vote"

    self.add_item(discord.ui.Button(label="Vote here!", url=url))


async def update_balance(ctx, amount, action="remove"):

  user_id = str(ctx.author.id)
  if not os.path.exists("economy.json"):
    with open("economy.json", "w") as f:
      f.write("{}")
  with open("economy.json", "r") as f:
    economy = json.load(f)
  if user_id not in economy:
    economy[user_id] = 15
  if action == "remove":
    if economy[user_id] < amount:
      embed = discord.Embed(
        title="<:reject:1092153213093957692> Denied Command",
        description="You don't have enough balance.",
        color=0x8080ff)
      embed.timestamp = datetime.datetime.utcnow()
      await ctx.respond(embed=embed, ephemeral=True)
      return False
    else:
      economy[user_id] -= amount
  elif action == "add":
    economy[user_id] += amount
  with open("economy.json", "w") as f:
    json.dump(economy, f)
  return True


# Economy Functions


async def check_balance(ctx, cost):
  user_id = str(ctx.author.id)
  if not os.path.exists("economy.json"):
    with open("economy.json", "w") as f:
      f.write("{}")
  with open("economy.json", "r") as f:
    economy = json.load(f)
  if user_id not in economy:
    economy[user_id] = 15
    with open("economy.json", "w") as f:
      json.dump(economy, f)
    return False  # El usuario no tiene suficiente dinero
  elif economy[user_id] < cost:
    embed = discord.Embed(title="<:reject:1092153213093957692> Denied Command",
                          description="You don't have enough balance.",
                          color=0x8080ff)
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.respond(embed=embed, ephemeral=True)
    return False  # El usuario no tiene suficiente dinero
  else:
    economy[user_id] -= cost
    with open("economy.json", "w") as f:
      json.dump(economy, f)
    return True  # El usuario tiene suficiente dinero