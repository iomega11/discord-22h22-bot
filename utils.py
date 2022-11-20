import random

POSTGRES = 'POSTGRES'
SQLITE = 'SQLITE'
dbtype = ''

def help():
	fichierHelp = open("help.txt","r") # Fichier contenant les commandes possibles et la version du bot
	help = fichierHelp.read()
	fichierHelp.close()
	return help

def version():
	fichierHelp = open("help.txt","r") # Fichier contenant les commandes possibles et la version du bot
	version = fichierHelp.readline()
	fichierHelp.close()
	return version

def tg():
	nb = len(open("repartie.txt").readlines(  ))
	fichierRepartie = open("repartie.txt","r") # Fichier contenant les reponses possibles a un 'tg'
	choix = random.randint(0,nb-1)
	for i in range(choix):
		fichierRepartie.readline()
	repartie = fichierRepartie.readline()
	fichierRepartie.close()
	return repartie

def initDBpostgres():
	dbtype = POSTGRES
	import os
	import psycopg2
	# Se connecter a la base de donnees
	DATABASE_URL = os.environ['DATABASE_URL']
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	return initDB(conn)

def initDBlite():
	dptype = SQLITE
	import sqlite3
	# Se connecter a la base de donnees
	conn = sqlite3.connect('discord.db')
	return initDB(conn)

def initDB(conn):
	c = conn.cursor()
	# Verifier si les tables existent
	# Le cas contraire, les creer
	c.execute("CREATE TABLE IF NOT EXISTS channels (nom text, id text)")
	c.execute("CREATE TABLE IF NOT EXISTS users (nom text, id text)")
	c.execute("CREATE TABLE IF NOT EXISTS logs (annee integer, mois integer, jour integer, heure integer, minute integer, seconde integer, auteur text, salon text, message text)")
	c.execute("CREATE TABLE IF NOT EXISTS ignoredchannels (id text)")
	return conn,c

def insertEntryInDB(date, author, channelId, content, conn, c):
	ligne = [date.year,date.month,date.day,date.hour,date.minute,date.second,author,channelId,content]
	if dbtype == POSTGRES:
		c.execute("INSERT INTO logs(annee, mois, jour, heure, minute, seconde, auteur, salon, message) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",ligne)
	elif dbtype == SQLITE:
		c.execute("INSERT INTO logs VALUES (?,?,?,?,?,?,?,?,?)",ligne)
	conn.commit()

def show(channel, c):
	requete = 'SELECT * FROM ' + channel
	c.execute(requete)
	return c.fetchall()

def isPresent(id, channel, c):
	result = show(channel, c)
	for i in range(len(result)):
		if result[i][0] == id:
			return True
	return False

def add(id, channel, c):
	requete = 'INSERT INTO ' + channel + ' VALUES (' + id + ')'
	c.execute(requete)
