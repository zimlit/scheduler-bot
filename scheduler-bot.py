import os

from discord.ext import commands
import discord
from dotenv import load_dotenv
import asyncio
from scheduling import Scheduling

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!sb ', intents=intents)


@bot.command(help = 'greets the sender')
async def hello(ctx):
    name = ctx.message.author.name
    await ctx.send(f'hello {name}')

async def main():
    await bot.add_cog(Scheduling(bot))

if __name__ == "__main__":
    asyncio.run(main())
    bot.run(TOKEN)
