# Work with Python 3.6

# Necessaire dans la console : python -m pip install discord.py

import os
import discord
from datetime import datetime, timedelta

# TOKEN donne autre part

CHANNEL_22H22_ID = 648637884555067428

pleinDetoiles = "°˖✧◝(⁰▿⁰)◜✧˖°"

client = discord.Client()

@client.event
async def on_message(message):
    ignored = True
    # we do not want the bot to reply to itself
    if (message.author == client.user or message.author.bot):
        ignored = False
        return
    elif (message.content.startswith('!ninja')):
        ignored = False
        msgSent = await message.channel.send("~ninja~")
        await msgSent.delete()
        await message.delete()
        print("Message supprimé")
    elif(message.content.startswith('!ecrire')):
        ignored = False
        messageAenvoyer = message.content[7:]
        await message.delete()
        print("Envoi d'un message : ",messageAenvoyer)
        await message.channel.send(messageAenvoyer)
    elif ("ping" in message.content.lower()):
        ignored = False
        await message.channel.send("pong")
    elif ((":weshalors:" in message.content.lower()) or ("wesh alors" in message.content.lower())):
        msg = ':weshalors:' + ' {0.author.mention} !'.format(message)
        ignored = False
        await message.channel.send(msg)
    elif (client.user.mentioned_in(message)):
        ignored = False
        await message.channel.send(pleinDetoiles)
    if(message.channel.id == CHANNEL_22H22_ID):
        ignored = False
        now = datetime.now()
        print("Il est ",now.hour,":",now.minute," donc il n'est pas 22:22.")
        if(now.hour != 21 or now.minute != 44):
        	await message.delete()
    if(ignored):
        print("Message ignored.")
        print("Id du channel : ",message.channel.id)
        print("Message : ",message.content)		

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

TOKEN = os.environ['TOKEN']

client.run(TOKEN)