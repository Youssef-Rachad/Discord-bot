import keep_alive
import description as i

import os
import requests
import json

import discord
from discord.utils import get
from discord.ext import commands

bot_description = "bonjour je suis le meilleur bot"
bot = commands.Bot(command_prefix='$', description=bot_description)


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_message(message):
    print(f"{message.author} says:\n {message.content}")
    await bot.process_commands(message)
    if message.content.startswith('inspire'):
        await inspire(await bot.get_context(message))


@bot.command(brief=i.makerole_brief, description=i.makerole_description)
async def makerole(ctx, message):
    if get(ctx.guild.roles, name=message):
        await ctx.send("Role already exists")
    else:
        await ctx.guild.create_role(name=message,
                colour=discord.Colour(0x0062ff))
        await ctx.send(f"made role {message}")


@bot.command(brief=i.inspire_brief, description=i.inspire_description)
async def inspire(ctx):
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + "\n-" + json_data[0]['a']
    await ctx.send(quote)


@bot.command(brief=i.ping_brief, description=i.ping_description)
async def ping(ctx):
    await ctx.send("pong")


@bot.command(brief=i.purge_brief, description=i.purge_description)
@commands.has_role('Admin')
async def purge(ctx, num):
    async for poubelle in ctx.channel.history(limit=int(num)+1):
        await poubelle.delete()
        print(f'deleted {num}messages successfully')


@bot.command(brief=i.comp_brief, description=i.comp_description)
async def comp(ctx, *args):
    if args[0] == 'Euclid':
        await ctx.send(
                f'https://www.cemc.uwaterloo.ca/contests/past_contests/{args[1]}/{args[1]}EuclidContest.pdf'
                )
    if args[0] == 'Euclid-solution':
        await ctx.send(
                f'https://www.cemc.uwaterloo.ca/contests/past_contests/{args[1]}/{args[1]}EuclidSolution.pdf'
                )


keep_alive.keep_alive()

bot.run(os.getenv('TOKEN'))
