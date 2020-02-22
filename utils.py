import random

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

def initDB():
	import os
	import psycopg2
	# Se connecter a la base de donnees
	DATABASE_URL = os.environ['DATABASE_URL']
	conn = psycopg2.connect(DATABASE_URL, sslmode='require')
	c = conn.cursor()
	# Verifier si les tables existent
	# Le cas contraire, les creer
	c.execute("CREATE TABLE IF NOT EXISTS channels (nom text, id text)")
	c.execute("CREATE TABLE IF NOT EXISTS users (nom text, id text)")
	c.execute("CREATE TABLE IF NOT EXISTS logs (annee integer, mois integer, jour integer, heure integer, minute integer, seconde integer, auteur text, salon text, message text)")
	return conn,c
    
def initDBlite():
	import sqlite3
	# Se connecter a la base de donnees
	conn = sqlite3.connect('discord.db')
	c = conn.cursor()
	# Verifier si les tables existent
	# Le cas contraire, les creer
	c.execute("CREATE TABLE IF NOT EXISTS channels (nom text, id text)")
	c.execute("CREATE TABLE IF NOT EXISTS users (nom text, id text)")
	c.execute("CREATE TABLE IF NOT EXISTS logs (annee integer, mois integer, jour integer, heure integer, minute integer, seconde integer, auteur text, salon text, message text)")
	return conn,c