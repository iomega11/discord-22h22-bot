# Work with Python 3.6

# Necessaire dans la console : python -m pip install discord.py

import os
import discord
from datetime import datetime, timedelta
import sqlite3

# TOKEN donne autre part
TOKEN = os.environ['TOKEN']

OWNERID = os.environ['OWNERID'] # Mon ID (Omega) pour recevoir un message quand le bot est lancé

CHANNEL_22H22_ID = os.environ['CHANNEL_22H22_ID'] # ID du channel 22h22

pleinDetoiles = "°˖✧◝(⁰▿⁰)◜✧˖°"

client = discord.Client()

fichierHelp = open("help.txt","r") # Fichier contenant les commandes possibles et la version du bot
help = fichierHelp.read()
version = fichierHelp.readline(1)
fichierHelp.close()

@client.event
async def on_message(message):
    ignored = True
    now = datetime.now()
    ligne = [now.year,now.month,now.day,now.hour,now.minute,now.second,str(message.author),str(message.channel),message.content]
    c.execute("INSERT INTO logs VALUES (?,?,?,?,?,?,?,?,?)",ligne)
    #(annee , mois , jour , heure , minute , seconde , auteur , salon , message )")
    # we do not want the bot to reply to itself
    if (message.author == client.user or message.author.bot):
        ignored = False
        return
    elif (message.content.startswith('.ninja')):
        ignored = False
        msgSent = await message.channel.send("~ninja~")
        await msgSent.delete()
        await message.delete()
        print("Message supprimé")
    elif(message.content.startswith('.ecrire')):
        ignored = False
        messageAenvoyer = message.content[7:]
        await message.delete()
        print("Envoi d'un message : ",messageAenvoyer)
        await message.channel.send(messageAenvoyer)
    elif(message.content.startswith('.exec') and message.author.id == OWNERID):
        ignored = False
        command = message.content[5:]
        await message.delete()
        print("Execution du code : ",command)
        exec(command)
    elif(message.content.startswith('.help')):
        ignored = False
        print('Demande de help par  : {0.author.mention}. '.format(message))
        await message.channel.send(help)
    elif(message.content.startswith('.version')):
        ignored = False
        print('Demande de version par  : {0.author.mention}. '.format(message))
        await message.channel.send(version)
    elif ("ping" in message.content.lower()):
        ignored = False
        await message.channel.send("pong")
    elif ((":weshalors:" in message.content.lower()) or ("wesh alors" in message.content.lower())):
        msg = 'Wesh alors' + ' {0.author.mention} !'.format(message)
        ignored = False
        await message.channel.send(msg)
    elif ( (message.content.startswith('.close') or message.content.startswith('.stop') or message.content.startswith('.logout'))):
        print(message.author.id," == ", OWNERID," ? ", (str(message.author.id) == OWNERID))
        
        ignored = False
        conn.commit()
        conn.close()
        fichierAtransmettre = discord.File('discord.db')
        await message.channel.send("Le bot va s'arreter. Voila les logs :",file=fichierAtransmettre)
        await client.close()
    elif (client.user.mentioned_in(message)):
        ignored = False
        await message.channel.send(pleinDetoiles)
    if(message.channel.id == CHANNEL_22H22_ID):
        ignored = False
        print("Il est ",now.hour,":",now.minute," donc il n'est pas 22:22.")
        if(now.hour != 21 or now.minute != 22):
        	await message.delete()
    if(ignored):
        print("Message ignored :")
        print("Id du channel : ",message.channel.id)
        print("Auteur : ",message.author.name," (",message.author.id,")")
        print("Message : ",message.content)		

@client.event
async def on_ready():
    print('Connecté.')
    print('Nom : ',client.user.name)
    print('ID : ',client.user.id)
    print('------')
    print("Omega : ",OWNERID)
    user = await client.fetch_user(OWNERID)
    await user.send("Le bot vient d'être lancé.")


# Se connecter a la base de donnees
conn = sqlite3.connect('discord.db')
c = conn.cursor()
# Verifier si les tables existent
# Le cas contraire, les creer
c.execute("CREATE TABLE IF NOT EXISTS channels (nom text, id text)")
c.execute("CREATE TABLE IF NOT EXISTS users (nom text, id text)")
c.execute("CREATE TABLE IF NOT EXISTS logs (annee integer, mois integer, jour integer, heure integer, minute integer, seconde integer, auteur text, salon text, message text)")

client.run(TOKEN)