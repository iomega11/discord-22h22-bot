
import sqlite3

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
	
def initDB():
	# Se connecter a la base de donnees
	conn = sqlite3.connect('discord.db')
	c = conn.cursor()
	# Verifier si les tables existent
	# Le cas contraire, les creer
	c.execute("CREATE TABLE IF NOT EXISTS channels (nom text, id text)")
	c.execute("CREATE TABLE IF NOT EXISTS users (nom text, id text)")
	c.execute("CREATE TABLE IF NOT EXISTS logs (annee integer, mois integer, jour integer, heure integer, minute integer, seconde integer, auteur text, salon text, message text)")
	return conn,c