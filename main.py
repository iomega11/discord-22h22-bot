# Work with Python 3.6

# Necessaire dans la console : python -m pip install discord.py

import os
import discord
from threading import Thread, Event
from datetime import date, time, datetime, timedelta
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

# Event necessaire au timer de 22h22
stopFlag = Event()

def attendreJusquA(self,hours,minutes):
	d = date.today()
	t = time(hours, minutes)
	timeToStart = datetime.combine(d, t)
	now = datetime.now()
	if(timeToStart > now): # L'heure est depassee
		timeToStart.replace(day = timeToStart.day + 1)
	delta = timeToStart - now
	print("Il me faut attendre ",int(delta.seconds / 3600)," heures, ",int(delta.seconds / 60)," minutes et ",int(delta.seconds % 60)," secondes.")
	self.stopped.wait(delta.seconds)

class MyThread(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
            attendreJusquA(self,22,15)
            user = await client.fetch_user(OWNERID)
            await user.send("Le bot vient d'être lancé.")

thread = MyThread(stopFlag) # Thread qui gere le timer

def peutSupprimer(channel):
    return ((type(channel)!=discord.DMChannel) and (type(channel)!=discord.GroupChannel))

@client.event
async def on_message(message):
    ignored = True
    now = datetime.now()
    ligne = [now.year,now.month,now.day,now.hour,now.minute,now.second,str(message.author),str(message.channel),message.content]
    c.execute("INSERT INTO logs VALUES (?,?,?,?,?,?,?,?,?)",ligne)
    #(annee , mois , jour , heure , minute , seconde , auteur , salon , message )")
    # we do not want the bot to reply to itself
    if (message.author == client.user or message.author.bot):
        return
    elif (message.content.startswith('.ninja')):
        msgSent = await message.channel.send("~ninja~")
        await msgSent.delete()
        if(peutSupprimer(message.channel)):
            await message.delete()
        print("Message supprimé")
        ignored = False
    elif((str(message.author.id) == OWNERID) and message.content.startswith('.ecrire')):
        messageAenvoyer = message.content[7:]
        if(peutSupprimer(message.channel)):
            await message.delete()
        print("Envoi d'un message : ",messageAenvoyer)
        await message.channel.send(messageAenvoyer)
        ignored = False
    elif((str(message.author.id) == OWNERID) and message.content.startswith('.exec') and (str(message.author.id) == OWNERID)):
        command = "        " + message.content[6:]
        print("Execution du code : ",message.content[6:])
        exec(command)
        ignored = False
    elif(message.content.startswith('.help')):
        print('Demande de help par  : {0.author.mention}. '.format(message))
        await message.channel.send(help)
        ignored = False
    elif(message.content.startswith('.version')):
        print('Demande de version par  : {0.author.mention}. '.format(message))
        await message.channel.send(version)
        ignored = False
    elif ("ping" in message.content.lower()):
        await message.channel.send("pong")
        ignored = False
    elif ((":weshalors:" in message.content.lower()) or ("wesh alors" in message.content.lower())):
        msg = 'Wesh alors' + ' {0.author.mention} !'.format(message)
        await message.channel.send(msg)
        ignored = False
    elif ((str(message.author.id) == OWNERID) and (message.content.startswith('.close') or message.content.startswith('.stop') or message.content.startswith('.logout'))):
        conn.commit()
        conn.close()
        fichierAtransmettre = discord.File('discord.db')
        await message.channel.send("Le bot va s'arreter. Voila les logs :",file=fichierAtransmettre)
        await client.close()
        ignored = False
    elif (client.user.mentioned_in(message)):
        await message.channel.send(pleinDetoiles)
        ignored = False
    if(str(message.channel.id) == CHANNEL_22H22_ID):
        if(now.hour != 21 or now.minute != 22):
            await message.delete()
        ignored = False
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
    thread.start()


# Se connecter a la base de donnees
conn = sqlite3.connect('discord.db')
c = conn.cursor()
# Verifier si les tables existent
# Le cas contraire, les creer
c.execute("CREATE TABLE IF NOT EXISTS channels (nom text, id text)")
c.execute("CREATE TABLE IF NOT EXISTS users (nom text, id text)")
c.execute("CREATE TABLE IF NOT EXISTS logs (annee integer, mois integer, jour integer, heure integer, minute integer, seconde integer, auteur text, salon text, message text)")

client.run(TOKEN)