#!/usr/bin/python3
import os
import discord
import random
import math
import json
from datetime import datetime
import requests

def stat_roll():
    numbers = []

    numbers.append(random.choice(range(1,6)))
    numbers.append(random.choice(range(1,6)))
    numbers.append(random.choice(range(1,6)))
    numbers.append(random.choice(range(1,6)))

    numbers.sort()

    return numbers[1] + numbers[2] + numbers[3]
 

    
wf = open("./logout.txt", "a")


now = str(datetime.now())
wf.write("\n-------------------------------\n")
wf.write(now)
wf.write("\n----------bot is active--------")
wf.write("\n-------------------------------\n")



from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TENOR_TOKEN = os.getenv('TENOR_KEY')

with open('./botstuff.json') as f:
    data = json.load(f)


f.close()

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print("Bot is Ready!")

@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return

    if msg.content.lower() == 'tell me a dad joke':
        response = random.choice(data["dad_jokes"])
        await msg.channel.send(response)

    if msg.content.lower() == 'why am i?':
        response = f'You exist to communicate with a bot'
        await msg.channel.send(response)

    if msg.content.lower() == 'who am i?':
        response = f'You are {msg.author.name}'
        await msg.channel.send(response)

    if '#magic8ball' in msg.content:
        response = random.choice(data["magic_8ball"])
        await msg.channel.send(response)

    if 'good morning' in msg.content.lower():
        response = "Morning. Will not complain. All is well here"
        await msg.channel.send(response)

    if msg.content.lower() == 'morning':
        response = "good morning.  All is well here. How are you?"
        await msg.channel.send(response)

    if 'hicago' in msg.content.lower():
        response = random.choice(data["chicago_responses"])
        await msg.channel.send(response)

    if 'taylor green' in msg.content.lower():
        response = random.choice(data["mtg"])
        await msg.channel.send(response)

    if 'ancouver' in msg.content.lower():
        response = random.choice(data["vancouver"])
        await msg.channel.send(response)



    await bot.process_commands(msg)


@bot.command(name='repeat', help='repeats what you typed')
async def repeat(ctx, *args):
    await ctx.send('{}'.format(' '.join(args)))

@bot.command(name='bot', help='this does very little')
async def isbot(ctx):
    response = random.choice(data["pile_of_stuff"])
    await ctx.send(response)

@bot.command(name='roll', help='Usage: roll <numDice> <numSides>')
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    sum = 0
    mult = 1
    if (number_of_dice <= 0 or number_of_sides == 0):
        dice = ["no"]
        await ctx.send(', '.join(dice))
    else:
        if (-1 * number_of_sides > 0):
            mult = -1
        number_of_sides = abs(number_of_sides)
        dice = [
            str(mult * random.choice(range(1,number_of_sides+1)))
            for _ in range(number_of_dice)
        ]
        for die in dice:
            sum = sum + int(die)
        await ctx.send(', '.join(dice) + " and the sum is: " + str(sum))

@bot.command(name='statroll', help='Usage: statroll')
async def statroll(ctx):
    sum = 0
    strStat = random.choice(range(1,6)) + random.choice(range(1,6)) + random.choice(range(1,6))
    dexStat = random.choice(range(1,6)) + random.choice(range(1,6)) + random.choice(range(1,6))
    wisStat = random.choice(range(1,6)) + random.choice(range(1,6)) + random.choice(range(1,6))
    intStat = random.choice(range(1,6)) + random.choice(range(1,6)) + random.choice(range(1,6))
    conStat = random.choice(range(1,6)) + random.choice(range(1,6)) + random.choice(range(1,6))
    chrStat = random.choice(range(1,6)) + random.choice(range(1,6)) + random.choice(range(1,6))

    myStr = "Strength - " + str(strStat) + "\n"
    myStr += "Dexterity - " + str(dexStat) + "\n"
    myStr += "Wisdom - " + str(wisStat) + "\n"
    myStr += "Intelligence - " + str(intStat) + "\n"
    myStr += "Constitution - " + str(conStat) + "\n"
    myStr += "Charisma - " + str(chrStat)

    await ctx.send(myStr)

@bot.command(name='magic8ball', help='it is a magic 8-ball')
async def magic8ball(ctx):
    response = random.choice(data["magic_8ball"])
    await ctx.send(response)

@bot.command(name='crunchyroll', help='sure why not')
async def crunchy(ctx):
    response = "This is not a command"
    await ctx.send(response)

@bot.command(name='gifme', help='provide a random gif: gifme <searchterm>')
async def gifme(ctx, search_input="random"):
    lmt = 8
    search_term = search_input
    outgifs = []
    r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, TENOR_TOKEN, lmt))

    if r.status_code == 200:
        myReturn = json.loads(r.content)
        for i in range(len(myReturn['results'])):
            url = myReturn['results'][i]['media'][0]['gif']['url'] #This is the url from json.
            outgifs.append(url)
    else:
        myReturn = None

    response = random.choice(outgifs)
    await ctx.send(response)


bot.run(TOKEN)
wf.close()
