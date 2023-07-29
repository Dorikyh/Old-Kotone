from discord.ext.bridge import bridge_command
import discord
import aiohttp
from utils import twobuttonview
from discord.ext import commands
import datetime

class BookInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge_command(description="📒 Get useful info about Books and eBooks")
    @discord.option("book_name",description="Enter a book name (Optional tip: add authors to get better results)")
    async def book(self, ctx, book_name):
        # Get the book information from Google Books
        async with aiohttp.ClientSession() as session:
            response = await session.get(f"https://www.googleapis.com/books/v1/volumes?q={book_name}")
            if response.status == 200:
                book_info = await response.json()
                book_info = book_info["items"][0]
            else:
                await ctx.send("Error getting book information.")
                return

        # Create an embed with the book information
        embed = discord.Embed(title=f":notebook_with_decorative_cover: Book Info: {book_info['volumeInfo']['title']}", description=f"{book_info['searchInfo']['textSnippet']}", color=0xffbdbd)
        embed.add_field(name=":bust_in_silhouette: Author:", value=book_info['volumeInfo']['authors'][0], inline=True)
        embed.add_field(name=":date: Published:", value=book_info['volumeInfo']['publishedDate'], inline=True)
        embed.add_field(name=":page_with_curl: Pages:", value=book_info['volumeInfo']['pageCount'], inline=True)
        embed.add_field(name=":bookmark: Description:", value=book_info['volumeInfo']['description'][:512]+"...", inline=False)
        embed.set_thumbnail(url=book_info['volumeInfo']['imageLinks']['smallThumbnail'])
        view=twobuttonview(text="Free Preview", url=book_info['volumeInfo']['canonicalVolumeLink'],emoji="📓", text2="Buy Book", url2="http://google.com", emoji2="💴")
        embed.set_footer(text=f"Request by {ctx.author.name}", icon_url=ctx.author.avatar.url)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.reply(embed=embed, view=view)

def setup(bot):
    bot.add_cog(BookInfo(bot))

