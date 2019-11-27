# Work with Python 3.6

# Necessaire dans la console : python -m pip install discord.py

import discord
from datetime import datetime, timedelta

TOKEN = "NjQ5MTQxODY0NzIwNzYwODYy.Xd4jQw.znHSp-L6FN4gVGv-upe9h4ihAIE"

CHANNEL_ID = 648637884555067428

pleinDetoiles = "°˖✧◝(⁰▿⁰)◜✧˖°"

client = discord.Client()

'''
def deleteMessage(message):
	await message.channel.purge(limit=1)
	print("Message supprimé")

def deleteMessage(message):
	await message.channel.purge(limit=1)
	print("Message supprimé")
'''
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
    elif (client.user.mentioned_in(message)):
        ignored = False
        await message.channel.send(pleinDetoiles)
    if(message.channel.id == CHANNEL_ID):
        ignored = False
        now = datetime.now()
        if(now.hour != 22 or now.minute != 22):
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

client.run(TOKEN)