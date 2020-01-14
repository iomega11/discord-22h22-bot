
import os
import discord
from threading import Thread, Event
from datetime import date, datetime, timedelta
import asyncio
import schedule

import utils


OWNERID = os.environ['OWNERID']
CHANNEL_22H22_ID = os.environ['CHANNEL_22H22_ID']
CHANNEL_ANNONCES_SOIREVISIONS_ID = os.environ['CHANNEL_ANNONCES_SOIREVISIONS_ID']

LOOP = asyncio.new_event_loop()
asyncio.set_event_loop(LOOP)

conn,c = utils.initDB()

pleinDetoiles = "°˖✧◝(⁰▿⁰)◜✧˖°"
msg22h22 = "Il est 22h22, c'est parti ! Qui lancera les hostilités ?"
msg22h23 = "Et c'est fini pour aujourd'hui ! A demain !"

hour22h22 = os.environ['HOUR_22']
hour22h23 = os.environ['HOUR_23']

def message22h22(client):
	co = asyncio.run_coroutine_threadsafe(
			client.get_channel(int(CHANNEL_22H22_ID)).send(msg22h22),
			LOOP)
	co.result()
	
def message22h23(client):
	co = asyncio.run_coroutine_threadsafe(
			client.get_channel(int(CHANNEL_22H22_ID)).send(msg22h23),
			LOOP)
	co.result()

def peutSupprimer(channel):
	return ((type(channel)!=discord.DMChannel) and (type(channel)!=discord.GroupChannel))

class Bot(discord.Client):
	async def on_ready(client):
		print('Connecté.')
		print('Nom : ',client.user.name)
		print('ID : ',client.user.id)
		print('------')
		schedule.every().day.at(hour22h22).do(message22h22, client=client)
		schedule.every().day.at(hour22h23).do(message22h23, client=client)
		user = await client.fetch_user(OWNERID)
		await user.send("Le bot vient d'être lancé.")

	async def on_message(client,message):
		ignored = True
        
		# on ne veut pas (encore) que le bot se reponde a lui meme
		if (message.author == client.user or message.author.bot):
			return
            
            
		now = datetime.now()
		ligne = [now.year,now.month,now.day,now.hour,now.minute,now.second,str(message.author),str(message.channel),message.content]
		#c.execute("INSERT INTO logs VALUES (?,?,?,?,?,?,?,?,?)",ligne)
		#(annee, mois, jour, heure, minute, seconde, auteur, salon, message)
		c.execute("INSERT INTO logs(annee, mois, jour, heure, minute, seconde, auteur, salon, message) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",ligne)
		if (message.content.startswith('.ninja')):
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
			command = message.content[6:]
			print("Execution du code : ",message.content[6:])
			exec(command)
			ignored = False
		elif(message.content.startswith('.help')):
			print('Demande de help par  : {0.author.mention}. '.format(message))
			await message.channel.send(utils.help())
			ignored = False
		elif(message.content.startswith('.version')):
			print('Demande de version par  : {0.author.mention}. '.format(message))
			await message.channel.send(utils.version())
			ignored = False
		elif ("ping" in message.content.lower() and str(message.channel.id) != CHANNEL_ANNONCES_SOIREVISIONS_ID):
			await message.channel.send("pong")
			ignored = False
		elif ((":weshalors:" in message.content.lower()) or ("wesh alors" in message.content.lower())):
			msg = 'Wesh alors' + ' {0.author.mention} !'.format(message)
			await message.channel.send(msg)
			ignored = False
		elif ((str(message.author.id) == OWNERID) and (message.content.startswith('.close') or message.content.startswith('.stop') or message.content.startswith('.logout'))):
			conn.commit()
			conn.close()
            # a changer pour fonctionner avec postgresql
			#fichierAtransmettre = discord.File('discord.db')
			#await message.channel.send("Le bot va s'arreter. Voila les logs :",file=fichierAtransmettre)
			await message.channel.send("Au revoir :)")
			await client.close()
			ignored = False
		elif (client.user.mentioned_in(message) and not message.mention_everyone):
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
