# returns the list of emojis used in the message
def get_emojis(message):
	liste = []
	for word in message.split(':'):
		if not " " in word:
			liste.append(word)
	return liste

# checks if an emoji has been named with the word "ping"
def message_contains_emoji_with_ping(message):
	liste_emojis = get_emojis(message)
	print(liste_emojis)
	for i in range(len(liste_emojis)):
		if "ping" in liste_emojis[i] and liste_emojis[i-1] == "<" and liste_emojis[i+1][len(liste_emojis[i+1])-1] == ">":
			return True
	return False