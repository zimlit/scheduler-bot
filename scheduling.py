from discord.ext import commands
import discord
import random

class Request:
        def __init__(self, author: discord.Member, game, time, people):
            self.author = author
            self.game = game
            self.time = time
            self.people = {}
            for person in people:
                self.people[person] = None

class Scheduling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reqs = {}

    @commands.command(help= "sends a game request [game] [time] [people]*")
    async def req(self, ctx, game, time, *people: discord.Member):
        author = ctx.message.author
        n = random.randrange(9999)
        self.reqs[n] = Request(author, game, time, people)
        for person in people:
            channel = await person.create_dm()
            await channel.send(f'@{author.name} has invited you to play {game} at {time}. this request has code {n}')
    
    @commands.command(help = "accept a game request [code]")
    async def accept(self, ctx, code: int):
        if isinstance(ctx.message.channel,discord.DMChannel):
            try:
                r = self.reqs[code]
                if not (ctx.message.author in r.people):
                    await ctx.send(f"you are not a member of this request")
                    return

                await ctx.send(f"thank you request {code} has been accepted")
                r.people.pop(ctx.message.author)
                if len(r.people) == 0:
                    self.reqs.pop(code)

                channel = await r.author.create_dm()
                await channel.send(f'@{r.author.name} has accepted your request to play {r.game} at {r.time}')
            except KeyError:
                await ctx.send(f"error request {code} does not exist")
        else:
            await ctx.send("cant use outside of dms")

    @commands.command(help = "decline a game request [code]")
    async def decline(self, ctx, code: int):
        if isinstance(ctx.message.channel,discord.DMChannel):
            try:
                r = self.reqs[code]
                if not (ctx.message.author in r.people):
                    await ctx.send(f"you are not a member of this request")
                    return

                await ctx.send(f"thank you request {code} has been declined")
                r.people.pop(ctx.message.author)
                if len(r.people) == 0:
                    self.reqs.pop(code)
                channel = await r.author.create_dm()
                await channel.send(f'@{r.author.name} has declined your request to play {r.game} at {r.time}')
            except KeyError:
                await ctx.send(f"error request {code} does not exist")
        else:
            await ctx.send("cant use outside of dms")
