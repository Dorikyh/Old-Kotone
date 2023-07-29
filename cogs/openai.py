import aiohttp
import asyncio
from discord.commands import slash_command, user_command, guild_only, Option, SlashCommandGroup
import discord
from discord.ext.bridge import bridge_command
from utils import twobuttonview
from discord.ext import commands
import datetime
import random
import openai
import os
import json
import time
from utils import check_balance
from discord.commands import Option
openai.api_key = "sk-xxx"

MAX_MESSAGES = 15


conversations = {}

async def delete_conversation(user_id):
    # Eliminar la conversación del usuario del diccionario
    if user_id in conversations:
        del conversations[user_id]

class LLM():
    def __init__(self):
        pass

    def process_functions(self, text):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {"role": "system", "content": "You are KotoneGPT"},
                {"role": "user", "content": text},
            ],
            functions=[
                {
                    "name": "print_text",
                    "description": "Print the text of the user in console",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "text": {
                                "type": "string",
                                "description": "the text to print",
                            }
                        },
                        "required": ["text"],
                    },
                },
                # Resto de las funciones existentes
            ],
            function_call="auto",
        )

        message = response["choices"][0]["message"]

        if message.get("function_call"):
            function_name = message["function_call"]["name"]
            args = message.to_dict()['function_call']['arguments']
            print("Funcion a llamar: " + function_name)
            args = json.loads(args)
            return function_name, args, message

        return None, None, message

    def process_response(self, text, message, function_name, function_response):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {"role": "system", "content": "You are KotoneGPT"},
                {"role": "user", "content": text},
                message,
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                },
            ],
        )
        return response["choices"][0]["message"]["content"]

    def print_text(self, text):
        print(text)
        return f"The text {text} was printed"




async def search_image(query):
    clave_api = ""
    cx = "059e476b46129465e"  # El ID de búsqueda personalizada (cx) que creaste en la Consola de Desarrolladores de Google

    url = f"https://www.googleapis.com/customsearch/v1?key={clave_api}&cx={cx}&searchType=image&q={query}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

            if "items" in data:
                first_result = data["items"][0]
                image_link = first_result["link"]
                return image_link

class OpenAI(discord.ext.commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.llm = LLM()
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("[✔️] OpenAI was loaded successfully")  

    
    @bridge_command(name="chatgpt", description="📓 Use the ChatGPT bot (GPT 3.5 Turbo)")
    @discord.option("prompt", description="Enter your prompt: (Be as accurate as possible with your prompt)")
    @discord.option("style", description="Specify the style of the response", choices=["creative", "precise"], required = False, default=None)
    async def chatgpt(self, ctx, *, prompt, style=None):

        if style is None:
            style = "precise"

        # Defer the initial response to avoid displaying a loading message
        await ctx.defer()
    
        # Make the ChatGPT completion request
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are KotoneGPT, a very intelligent Discord Assistant. Be {style}.Before answering write a title about the conversation in a paragraph, and after reply to the user"},
                {"role": "user", "content": prompt}
            ]
        )
        print(style)
        print(completion)
    
        # Get the model's response and remove backticks from output
        output = completion['choices'][0]['message']['content']
        output = output.replace("`", "")
    
        # Obtain the conversation title
        title_end_index = output.find("\n")
        conversation_title = output[:title_end_index].strip()

        # Search for the image using the conversation title
        image_link = await search_image(conversation_title)
    
        # Check if the response exceeds 1000 characters
        if len(output) > 1000:
            # Split the response into two parts
            first_part = output[:1000]
            second_part = output[1000:]
    
            # Create an embed message with two fields for the response parts (inline=False)
            embed = discord.Embed(
                title="<:chatgpt:1101654964813705226> ChatGPT Turbo",
                description=f"Input: {prompt}",
                color=0x77ab59
            )
            embed.add_field(name="Kotone output (Part 1)", value=f"```{first_part}```", inline=False)
            embed.add_field(name="Kotone output (Part 2)", value=f"```{second_part}```", inline=False)
        else:
            # Create an embed message with a field for the complete response (inline=False)
            embed = discord.Embed(
                title="<:chatgpt:1101654964813705226> ChatGPT Turbo",
                description=f"Input: {prompt}",
                color=0x77ab59
            )
          
            embed.add_field(name="Kotone output", value=f"```{output}```")
    
    
    
        # Set the footer, timestamp, and action buttons
        embed.set_footer(
            text=f"Requested by {ctx.author.name} | Total Tokens {completion['usage']['total_tokens']}",
            icon_url=ctx.author.avatar.url
        )
        embed.set_image(url=image_link)
        embed.timestamp = datetime.datetime.utcnow()
        view = twobuttonview(
            text="ChatGPT",
            url="https://chat.openai.com",
            emoji="<:openai:1116094808474263582>",
            text2="Invite Kotone",
            url2="https://dsc.gg/kotone",
            emoji2="<:invite:1119823128147796098>"
        )
    
        # Reply with the embed message and action buttons
        await ctx.reply(embed=embed, view=view)
        print(completion)


    @bridge_command(description='[Beta Testing] KotoneGPT, AI Assistant powered by Plugins')
    @discord.option("message", description="Chat with KotoneGPT! (Beta-Testing)")
    async def kotone(self, ctx, *, message):
        await ctx.defer()
        user_id = ctx.author.id

        if user_id in conversations:
            conversation = conversations[user_id]
        else:
            conversation = []

        conversation.append({"role": "user", "content": message})

        if len(conversation) > MAX_MESSAGES:
            conversation = conversation[-MAX_MESSAGES:]

        for i, msg in enumerate(conversation):
            if len(msg['content']) > 200:
                conversation[i]['content'] = msg['content'][:200]

        function_name, args, message = self.llm.process_functions(message)

        if function_name == "print_text":
            text = args["text"]
            self.llm.print_text(text)
            output = f"Función {function_name} se ejecutó con {text}"
        else:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are KotoneGPT. You have to act as an AI assintant like Siri. Your messages are extremely short, like a chat conversation. Talking with: {ctx.author.name}"},
                    *conversation
                ]
            )
            
            output = completion['choices'][0]['message']['content']


        conversation.append({"role": "system", "content": output})
        conversations[user_id] = conversation

        await ctx.reply(output)




    @bridge_command(description='Dont know what are they talking about? Make an AI Chat Recap!')
    async def recap(self, ctx, channel: discord.TextChannel = None):
        await ctx.defer()
        if not channel:
            channel = ctx.channel
            
        msgs = await channel.history(limit=40).flatten()

        conversation = ""
        for msg in reversed(msgs):
            conversation += f"{msg.author.name}: {msg.content}\n"


        print(conversation)
                
        # Make the ChatGPT completion request
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "dont exceed more than 800 characters. Your task is to analyze and interpret the following conversation and explain it to the user."},
                {"role": "user", "content": conversation}
            ]
        )



        # Get the model's response and remove backticks from output
        output = completion['choices'][0]['message']['content']


        # Check if the response exceeds 1000 characters
        if len(output) > 1000:
            # Split the response into two parts
            first_part = output[:1000]
            second_part = output[1000:]
    
            # Create an embed message with two fields for the response parts (inline=False)
            embed = discord.Embed(
                title="<:chatgpt:1101654964813705226> Recap Analysis",
                color=0x77ab59
            )
            embed.add_field(name="Kotone output (Part 1)", value=f"```{first_part}```", inline=False)
            embed.add_field(name="Kotone output (Part 2)", value=f"```{second_part}```", inline=False)
        else:
            # Create an embed message with a field for the complete response (inline=False)
            embed = discord.Embed(
                title="<:chatgpt:1101654964813705226> Recap Analysis",
                color=0x77ab59
            )
          
            embed.add_field(name="Kotone output", value=f"```{output}```")
    
        # Set the footer, timestamp, and action buttons
        embed.set_footer(
            text=f"Requested by {ctx.author.name} | Total Tokens {completion['usage']['total_tokens']}",
            icon_url=ctx.author.avatar.url
        )
        embed.timestamp = datetime.datetime.utcnow()
        view = twobuttonview(
            text="OpenAI",
            url="https://chat.openai.com",
            emoji="<:openai:1116094808474263582>",
            text2="Invite Kotone",
            url2="https://dsc.gg/kotone",
            emoji2="<:invite:1119823128147796098>"
        )
    
        # Reply with the embed message and action buttons
        await ctx.reply(embed=embed, view=view)
        
        

    @bridge_command(name="translate", description="📓 Translate in any language with AI")
    @discord.option("language", description="Enter the text you want to translate")
    @discord.option("text", description="Enter the language to translate")
    @discord.option("accent", description="Specify the accent or the style to translate", default='formal')
    async def translate(self, ctx, language, *, text, accent=None):
    
        if accent is None:
            accent = "formal"
    
        # Defer the initial response to avoid displaying a loading message
        await ctx.defer()
    
        # Make the ChatGPT completion request
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are KotoneGPT, a very intelligent Translater. Be accent: "+accent},
                {"role": "user", "content": f"Translate this text to {language}: {text}"}
            ]
        )
        print(accent)
    
        # Get the model's response and remove backticks from output
        output = completion['choices'][0]['message']['content']
    
        # Check if the response exceeds 1000 characters
        if len(output) > 1000:
            # Split the response into two parts
            first_part = output[:1000]
            second_part = output[1000:]
    
            # Create an embed message with two fields for the response parts (inline=False)
            embed = discord.Embed(
                title="<:chatgpt:1101654964813705226> TranslateGPT",
                description=f"Text: {text}\nLanguage: {language}",
                color=0x77ab59
            )
            embed.add_field(name="Kotone output (Part 1)", value=f"```{first_part}```", inline=False)
            embed.add_field(name="Kotone output (Part 2)", value=f"```{second_part}```", inline=False)
        else:
            # Create an embed message with a field for the complete response (inline=False)
            embed = discord.Embed(
                title="<:chatgpt:1101654964813705226> TranslateGPT",
                description=f"Input: {text}",
                color=0x77ab59
            )
          
            embed.add_field(name="Kotone output", value=f"```{output}```")
    
        # Set the footer, timestamp, and action buttons
        embed.set_footer(
            text=f"Requested by {ctx.author.name} | Total Tokens {completion['usage']['total_tokens']}",
            icon_url=ctx.author.avatar.url
        )
        embed.timestamp = datetime.datetime.utcnow()
        view = twobuttonview(
            text="OpenAI",
            url="https://chat.openai.com",
            emoji="<:openai:1116094808474263582>",
            text2="Invite Kotone",
            url2="https://dsc.gg/kotone",
            emoji2="<:invite:1119823128147796098>"
        )
    
        # Reply with the embed message and action buttons
        await ctx.reply(embed=embed, view=view)
    
    
    @bridge_command(name="imagine", description="📓 Generate images using OpenAI Dalle 2")
    @discord.option("prompt", description="Enter your prompt:")
    async def imagine(self, ctx, *, prompt):
    
      if await check_balance(ctx, 3):

        await ctx.defer()

        response = openai.Image.create(
			prompt=prompt,
			n=1,
			size="1024x1024")

        image_url = response['data'][0]['url']

        embed = discord.Embed(title="DALL-E 2", description=f"Input: {prompt}", color=0x77ab59)
        embed.set_image(url=image_url)
        embed.timestamp = datetime.datetime.utcnow()
        view = twobuttonview(
			text="DALL-E",
			url="https://chat.openai.com",
			emoji="<:openai:1116094808474263582>",
			text2="Invite Kotone",
			url2="https://dsc.gg/kotone",
			emoji2="<:kotone:1095174885346644080>")
			
        await ctx.reply(embed=embed, view=view)


def setup(bot):
    bot.add_cog(OpenAI(bot))

