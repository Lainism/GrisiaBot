import discord
import random
import time
from SevensGame import *

'''
@author: Singidava
'''

'''
Global variables
'''
mode = "double"
game = False
sevens = None

'''
Logging in
'''

'''
Debounce: gotten from Dio
def timerfunction():
        global debounce
        debounce = True

    if message.content.startswith('o lol'):
        global debounce
        from threading import Timer
        if debounce == True:
            debounce = False
            client.send_message(message.channel, 'o lol')
            t = Timer(3.0, timerfunction)
            t.start()
'''

# I want to be able to share the code so...
file = open("login.txt", "r")
uinfo = file.read().split(';')
file.close()

client = discord.Client()
client.login(uinfo[0], uinfo[1])

if not client.is_logged_in:
	print("Login failed.")
	exit(1)
	
print("Login successful. Starting the bot...")

'''
Preloading data from files
'''

print("Loading data from files...")

#Profile image
with open("light.png", "rb") as fp:
	lightava = fp.read()

with open("dark.png", "rb") as fp:
	darkava = fp.read()

print("Loading avatars completed.")

#Initial D OST
initiald = {}
with open("initiald.txt") as f:
	initiald = f.readlines()

if len(initiald) < 1:
	print("Loading Initial D OST failed.")
else:
	print("Loading Initial D OST completed.")

'''
Helper functions
'''

# Just because message.startswith(command) is pretty long
# ms stands for "Message Starts"
def ms(message, c):
	command = c.lower()
	content = message.lower()
	if content.startswith(command):
		return True
	return False
	
# Just because message.contains(command) is pretty long
# mc stands for "Message Contains"
def mc(message, c):
	command = c.lower()
	content = message.lower()
	if command in content:
		return True
	return False
	
# Answering based on the mood
# r stands for response
def r(msg, light = "", dark = "", thinking=False):

	# If I've been lazy and only wrote one message...
	if (len(light) > 0 and len(dark) < 1):
		message = light
		if thinking:
			message="(" + light + ")"
		client.send_message(msg.channel, message)
		return
	elif (len(light) < 1 and len(dark) > 0):
		message = dark
		if thinking:
			message = "(" + dark + ")"
		client.send_message(msg.channel, message)
		return
	
	# If there are multiple messages, check the mode setting
	if mode == "double":
		client.send_message(msg.channel, light + "\n(" + dark + ")")
	elif mode == "light":
		client.send_message(msg.channel, light)
	elif mode == "dark":
		client.send_message(msg.channel, dark)        

'''
# Events
'''    

@client.event
def on_ready():
	global client
	global lightava

	client.edit_profile(uinfo[1], avatar=lightava)
	print("The bot is running as the user {}".format(client.user.name))
	
@client.event
def on_message(msg):
	global mode
	global uinfo
	global client
	global lightava
	global darkava
	global initiald
	global game
	global sevens

	# -----------------#
	# General commands #
	# -----------------#

	message = msg.content


	thinking = False
	if mode == "double":
		thinking = True

	command = False
	if ms(message, "!command") and len(message) > 9 and str(msg.author.id) == str(134719938886631424):
		command = True
		message = "!" + message[9:]
		r(msg, "By God of Light I shall swear to carry out my Mistress' wish.", "It's not like I have a choice...")

	if ms(message, "!repeat") and len(message) > 9 and str(msg.author.id) == str(134719938886631424):
		if (mode != "light"):
			r(msg, "Seriously...? Whatever.", thinking=thinking)
		r(msg, message[8:])

	# Bot information
	elif ms(message, "!about"):
		if mode == "light":
			r(msg, "It was Mistress Singidava who called upon God of Light to bring Sun upon this world in order to share the wonders of His glory. Let these eyes also witness and the "  +
			"lips speak of the brilliant of fantasy born from His light. It shall be Sun's highest honor to illuminate even the outer corners of His realm.")
		else:
			r(msg,
			"I was created by Mistress Singi to advertise The Legend of Sun Knight light novel series, though I will also probably end up having some anime related " +
			"commands as well. I *finally* don't need to care about 'the whole continent knows this and the whole continent knows that'! It would be the paradise if only " +
			"I wasn't *still* programmed refer to God of Light in every other sentece. Urgh... Why would you do this to me!?")
		
	# Lazy copy paste code incoming. Might implements proper arguments someday... :)
	# Switching modes
	elif ms(message, "!mode double"):
		client.edit_profile(uinfo[1], avatar=lightava)
		mode = "double"
		r(msg, "God of Light shall bless you with the gift of knowledge even if its brilliance were to blind Sun. Everything shall be as God of Light Himself intended.",
				"I will tell you everything I know, but I hate you for making me spout this nonsense. This is the default mode.")
	elif ms(message, "!mode light"):
		client.edit_profile(uinfo[1], avatar=lightava)
		mode = "light"
		r(msg, "Sun shall preach about the wonders of God of Light.")
	elif ms(message, "!mode dark"):
		if mode != "dark":
			client.edit_profile(uinfo[1], avatar=darkava)
		mode = "dark"
		r(msg, "Much better. Let's just get to the business.")
		
	elif (ms(message, "!shut up") or ms(message, "!shutup")) and (mode == "double" or mode == "light"):
		r(msg, "(Argh, I'm falling asleep listening to my own preaches again... Can't somebody just change me to !mode dark?)")

	elif ms(message, "!channel id") or ms(message, "!channelid"):
		r(msg, str(msg.channel.id))

	elif ms(message, "!server id") or ms(message, "!serverid"):
		r(msg, str(msg.server.id))

	elif mc(message, "Singidiva") or mc(message, "Singing Diva"):
		r(msg, "God of Light shall scorn on those who disrespect others. You must pray for His benevolence and forgiveness to have your soul cleansed.",
				"Mistress' name is Singidava you oaf! Learn to spell unless you want to risk rejoining God of Light early!")

	elif ms(message, "Hi Grisia") or ms(message, "Hi Sun") or ms(message, "Hello Grisia")  or ms(message, "Hello " + client.user.mention()) or ms(message, "Hello Sun") or ms(message, "Hello SingiBot")  or ms(message, "!Hello") or ms(message, "Hi " + client.user.mention()):
		r(msg, "The benevolent God of Light will forgive your sins, " + msg.author.mention() + ".",
				"Yo.")

	elif ms(message, "!Grisia"):
		if str(msg.author.id) == str(134719938886631424):
			r(msg, "As if they came from God of Light Himself, I will heed to any request my Mistress might have.",
				"What is it?")
		else:
			r(msg, "As a humble servant of God of Light, Sun wishes to hear out the earthly troubles of the commoners.",
				"Whaddya want?")

	# -----------------#
	#   LSK commands   #
	# -----------------#

	elif ms(message, "!LSK"):
		r(msg, "The Legend of the Sun Knight is the light novel series I originated from. It's by Yu Wo and can be read in English for free at http://www.princerevolution.org/")

	# -----------------#
	#  Misc. commands  #
	# -----------------#

	elif ms(message, "!kill") or ms(message, "!murder"):
		double = [msg.author.mention() + " Would you like me to contact a necromancer in the case you'll ever regret this?",
					msg.author.mention() + " Just don't come back crying, asking for a ressurrection. I'm not going to do it.",
					msg.author.mention() + " Murder is bad, but getting caught is even worse. Please don't be advertise your plans.",
					msg.author.mention() + " Perhaps you should consult a psychologist before going through with this?"]
		dark = [msg.author.mention() + " Murder? Death? Destruction? Sounds nice.",
				msg.author.mention() + " is boasting about your plans online? What an amateur.",
				msg.author.mention() + " Shut up or you're the one that's gonna end up rejoining God of Light.",
				msg.author.mention() + " If you ever need a necromancer to make them into a zombie, just ask me.",
				msg.author.mention() + " Die.",
				msg.author.mention() + " Sounds like fun. Can I join? -No, don't answer. I'll do it regardless."]
		if mode != "dark":
			r(msg, "God of Light scorns on those seeking to extinguish the light of others. You must pray for His forgiveness and redeem yourself at His mercy.",
				random.choice(double))
		else:
			r(msg, random.choice(dark))
	elif ms(message, "!Whodunnit") or ms(message, "!Whodunit") or ms(message, "!Blackout") or ms(message, "!Black out"):
		r(msg, "http://www.youtube.com/watch?v=OYRknZ-6pRM")
	elif ms(message, "!Initial D") or ms(message, "!InitialD") or ms(message, "!Eurobeat") or ms(message, "!Cars") or ms(message, "!86"):
		if len(initiald) > 0:
			r(msg, random.choice(initiald))
	elif ms(message, "!Tsundere"):
		r(msg, "Dere dere~", "TSUN TSUN!")
	elif ms(message, "!90s") or ms(message, "!running"):
		r(msg, "https://www.youtube.com/watch?v=-gx8kg8BUa0")
	elif ms(message, "!Windows") or ms(message, "!Linux") or ms(message, "!OSX") or ms(message, "!MAC"):
		r(msg, "http://openings.moe/?video=InstallLinux.webm")
	elif ms(message, "!Math"):
		r(msg, "http://openings.moe/?video=1441552323691.webm")
	elif ms(message, "!Maria") or ms(message, "!MaidBot") or ms(message, "!Maid"):
		r(msg, "https://www.youtube.com/watch?v=q2qBEsYtP04")
	elif ms(message, "!congratulations"):
		r(msg, "https://www.youtube.com/watch?v=wDajqW561KM")
	elif ms(message, "!Kero") or ms(message, "!Frog") or ms(message, "!Sgt"):
		options = ["https://www.youtube.com/watch?v=qyJW_n-GY3E",
					"https://www.youtube.com/watch?v=9Xpc1TBCdPo",
					"https://www.youtube.com/watch?v=KUCJ0pfefzI"]
		r(msg, random.choice(options))
	elif ms(message, "!Uninstall") or ms(message, "!bokurano"):
		options = ["https://www.youtube.com/watch?v=05p646nlYS0",
					"https://www.youtube.com/watch?v=TJB0uCERrEQ"]
		r(msg, random.choice(options))
	elif ms(message, "!Puyo"):
		options = ["Ever heard of Puyo Puyo? https://www.youtube.com/watch?v=tt8nU-JqNsk#t=1m20s",
					"Want to try playing some Puyo Puyo yourself? http://www.puyovs.net/index.php",
					"Trying to improve your Puyo skills? http://puyonexus.net/wiki/How_to_Play_Puyo_Puyo"]
		r(msg, random.choice(options))
	elif ((message.lower() == "!go") or ms(message, "!Cosumi") or ms(message, "!Baduk") or ms(message, "!Weiqi") or ms(message, "!Igo")):
		options = ["Looking for a place to play go online? Try https://online-go.com/",
				"Looking for a place to play go online? Try https://www.gokgs.com/",
				"Want to try online go problems? Go to http://goproblems.com/"]
		r(msg, random.choice(options))

	elif ms(message, "!Touya") or ms(message, "!Akira" or ms(message, "!Toya")):
		r(msg, "SHINDOU!!")
	elif ms(message, "!Shindou") or ms(message, "!Hikaru") or ms(message, "!Shindo"):
		r(msg, "TOUYA!!")
	elif ms(message, "!Ship"):
		members = msg.server.members
		if not ms(message, "!Ship all"):
			online = []
			for member in members:
				if member.status == "online":
					online.append(member)
			if len(online) > 0:
				members = online
		member1 = random.choice(members)
		member2 = random.choice(members)
		mn1 = member1.mention()
		mn2 = member2.mention()

		if str(member1.id) == str(134719938886631424):
			mn1 = "my Mistress"
		if str(member2.id) == str(134719938886631424):
			mn2 = "my Mistress"

		if str(member1.id) == str(member2.id):
			r(msg, "It is God of Light's will that " + mn1 + " will become His servant and swear celibacy.")
		else:
			r(msg, "It is God of Light's will that " + mn1 + " and " + mn2 + " will be united in holy matrimony.")

		if mode != "light" and (str(member1.id) == str(client.user.id) or str(member2.id) == str(client.user.id)):
			r(msg, "Y-You must be joking...!", thinking=thinking)
		elif mode != "light" and str(member1.id) == str(member2.id):
			r(msg, "Feel my pain!", thinking=thinking)
		elif mode != "light":
			options = ["Hah! Serves you right!",
						"Naturally, this means you'll be ditching any current lovers you might have.",
						"At least you don't have to be married to your job... Geh.",
						"Ah, young love. *So... jealous...!*",
						"Church of God of Light doesn't allow divorces."]
			r(msg, random.choice(options) , thinking=thinking)


	# -----------------#
	#      Sevens      #
	# -----------------#

	elif ms(message, "!sevens commands"):
		client.send_message(msg.author, "Commands for game of sevens:\n" +
			"!Sevens game - Creates a new game instance.\n" +
			"!Sevens help - Displays the rules of the game.\n" +
			"!Sevens commands - Displays the list of commands for game of sevens.\n" +
			"!Join sevens - Join to game of sevens.\n" +
			"!Set max time [time in seconds] - Set maximum turn length in seconds. The value must be between 5 and 200. The default is 60 seconds.\n" +
			"!Start game - Starts the game and the game clock. To start a game you need at least two players.\n" +
			"!Check hand - Check what cards you have in your hand.\n" +
			"!Play [card name] - Plays the card from your hand to the field.\n" +
			"!Play empty - If you don't have a card you can play your turn will be skipped and you are given penalty to hold.\n" +
			"!End game - Ends the current game.")
	elif ms(message, "!sevens help"):
		client.send_message(msg.author, "~ Rules of sevens ~\n" +
			"You can play card that's either directly above or below a card on the field. Ace is below 2.\n" +
			"If you don't have a card you are given a penalty to hold. The player who holds this at the end of the game will receive 15 extra penalty points.\n" +
			"The game ends when one of the players runs out of their cards.\n" + 
			"At the end of the game player's all the remaining cards are summed together. Ace counts for 14 points.\n" +
			"The player with least amount of penalty points at the end of the game wins.")
	elif ms(message, "!Sevens game"):
		if game:
			r(msg, "There can be only one game at the time. To end the current game, please use command !end game.")
			return
		if msg.channel.is_private:
			r(msg, "Can't play on a private channel. Please use a public one instead.")
		sevens = SevensGame(client, msg)
		game = True
	elif ms(message, "!Join sevens") and game:
		sevens.join(msg.author)
	elif ms(message, "!Start game") and game:
		sevens.start_game(msg.channel)
	elif ms(message, "!check hand") and game:
		sevens.check_hand(msg.author)
	elif ms(message, "!play ") and game:
		sevens.play_card(message[6:], msg.author, msg.channel)
	elif ms(message, "!set max time ") and game:
		try:
			secs = int(message[14:].strip())
			sevens.set_max_time(msg.author, secs)
		except:
			r(msg, "Please specify the number of seconds.")
	elif ms(message, "!end game") and game:
		game = not sevens.end_game(msg.author)
		if not game:
			sevens = None
			r(msg, "The game of sevens has concluded.")

	# -----------------#
	#   Outside AAO    #
	# -----------------#

	elif (msg.channel.is_private or str(msg.server.id) != str(137392287108825088)):
		if (mc(message, "I don't understand") or mc(message, "Wakaranai")) and not mc(message, "webm"):
			r(msg, "http://openings.moe/?video=Wakaranai.webm")
		elif ms(message, "!NC17"):
			r(msg, "Hopefully you don't see this in AAO.")

	# -----------------#
	#      Command     #
	# -----------------#

	elif command:
		r(msg, message)
	
	
'''
# Run client
'''

client.run()