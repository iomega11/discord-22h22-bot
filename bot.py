
import os
import discord
from threading import Thread, Event
from datetime import datetime
import asyncio
import schedule

import utils
import emoji


OWNERID = os.environ['OWNERID']
CHANNEL_22H22_ID = os.environ['CHANNEL_22H22_ID']

LOOP = asyncio.new_event_loop()
asyncio.set_event_loop(LOOP)

conn,c = utils.initDBlite()

# pleinDetoiles = "°˖✧◝(⁰▿⁰)◜✧˖°"
pleinDetoiles = "Cyrielle, c'est moi !"
msg22h22 = "Il est 22h22, c'est parti ! Qui aura le temps de poster un message ?"
msg22h23 = "Et c'est fini pour aujourd'hui ! A demain !"

est_22h22 = False

hour22h22 = "22:22"
hour22h23 = "22:23"

def estDoublon(client, channel_id, text_to_compare):
	'''
	Retourne True si le message en parametre a envoye a deja
	ete envoye sur le channel passe en parametre
	'''
	c.execute("SELECT message FROM logs WHERE salon = %s AND auteur = %s", [str(channel_id), str(client.user)])
	result = c.fetchall()
	if not len(result):
		return False
	last_message = result[len(result)-1][0]
	return last_message == text_to_compare


def message22h22(client):
	if not estDoublon(client, int(CHANNEL_22H22_ID), msg22h22):
		co = asyncio.run_coroutine_threadsafe(
			client.get_channel(int(CHANNEL_22H22_ID)).send(msg22h22),
			LOOP)
		co.result()
	
def message22h23(client):
	if not estDoublon(client, int(CHANNEL_22H22_ID), msg22h23):
		co = asyncio.run_coroutine_threadsafe(
			client.get_channel(int(CHANNEL_22H22_ID)).send(msg22h23),
			LOOP)
		co.result()

def peutSupprimer(channel):
	return ((type(channel)!=discord.DMChannel) and (type(channel)!=discord.GroupChannel))

def doitEtreIgnore(channel_actuel):
	return utils.isPresent(channel_actuel, "ignoredchannels", c)

def ajouterSalonAignorer(channel_a_ignorer):
	utils.add(channel_a_ignorer, "ignoredchannels", c)
	conn.commit()

def afficherSalonsIgnores(client):
	result = 'Liste des salons que le bot ignore : \n'
	liste = utils.show("ignoredchannels", c)
	for i in range(len(liste)):
		channel = client.get_channel(int(liste[i][0]))
		result += str(channel) + '\n'
	return result

class Bot(discord.Client):
	async def on_ready(client):
		print('Connecté.')
		print('Nom : ',client.user.name)
		print('ID : ',client.user.id)
		print('------')
		#c.execute("SELECT COUNT(*) FROM ignoredchannels")
		#print("La base de donnees contient ", c.fetchone()[0], "entrees.")
		schedule.every().day.at(hour22h22).do(message22h22, client=client)
		schedule.every().day.at(hour22h23).do(message22h23, client=client)
		user = await client.fetch_user(OWNERID)
		await user.send("Le bot vient d'être lancé.")

	async def on_message(client,message):
		global conn,c
		try:
			ignored = True
			
			now = datetime.now()
			#ligne = [now.year,now.month,now.day,now.hour,now.minute,now.second,str(message.author),str(message.channel.id),message.content]
			#c.execute("INSERT INTO logs VALUES (?,?,?,?,?,?,?,?,?)",ligne)
			#(annee, mois, jour, heure, minute, seconde, auteur, salon, message)
			#c.execute("INSERT INTO logs(annee, mois, jour, heure, minute, seconde, auteur, salon, message) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",ligne)
			#conn.commit()
			
			# on ne veut pas (encore) que le bot se reponde a lui meme
			if (message.author == client.user or message.author.bot):
				# On stocke les messages envoyés par le bot, notamment pour éviter les doublons à 22h22
				utils.insertEntryInDB(now, str(message.author), str(message.channel.id), message.content, conn, c)
				return
			if doitEtreIgnore(str(message.channel.id)):
				print("Message posté dans un salon ignoré.")
				ignored = True
			#print(emoji.remove_emojis(message.content))
			elif str(message.channel.id) == CHANNEL_22H22_ID:
				if now.hour != int(hour22h22[:2]) or now.minute != int(hour22h22[3:]):
					print(now.hour, ":", now.minute, " != ", hour22h22[:2], ":", hour22h22[3:])
					await message.delete()
				ignored = False	
			elif message.content.lower().startswith('.ignorechannel') and str(message.author.id) == OWNERID:
				ajouterSalonAignorer(message.content[14:])
				await message.channel.send('Salon ajouté à la liste des salons à ignorer.')
				ignored = False	
			elif message.content.lower().startswith('.showignoredchannels') and str(message.author.id) == OWNERID:
				await message.channel.send(afficherSalonsIgnores(client))
				ignored = False	
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
			elif ((" tg " in message.content.lower()
				or " tg" in message.content.lower()
				or "tg " in message.content.lower()
				or message.content.lower() == "tg") and str(message.channel.id)):
				await message.channel.send(utils.tg())
				ignored = False
			elif ("ping" in message.content.lower() and not emoji.message_contains_emoji_with_ping(message.content.lower()) and str(message.channel.id)):
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
				
			if(ignored):
				print("Message ignored :")
				print("Id du channel : ",message.channel.id)
				print("Auteur : ",message.author.name," (",message.author.id,")")
				print("Message : ",message.content)		

		except Exception as exception:
			print(exception)
			user = await client.fetch_user(OWNERID)
			await user.send(exception)
