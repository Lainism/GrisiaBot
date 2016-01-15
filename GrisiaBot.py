import discord
import random
import time

'''
@author: Singidava
'''

'''
Global variables
'''
mode = "double"

'''
Logging in
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
def r(msg, light = "", dark = ""):

	# If I've been lazy and only wrote one message...
	if (len(light) > 0 and len(dark) < 1):
		client.send_message(msg.channel, light)
		return
	elif (len(light) < 1 and len(dark) > 0):
		client.send_message(msg.channel, dark)
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
	print("The bot is running as the user {}".format(client.user.name))
	
@client.event
def on_message(msg):
	global mode
	global uinfo
	global client
	global lightava
	global darkava
	global initiald

	# -----------------#
	# General commands #
	# -----------------#

	message = msg.content

	command = False
	if ms(message, "!command") and len(message) > 9 and str(msg.author.id) == str(134719938886631424):
		command = True
		message = "!" + message[9:]
		r(msg, "By God of Light I shall swear to carry out my Mistress' wish.", "It's not like I have a choice...")

	if ms(message, "!repeat") and len(message) > 9 and str(msg.author.id) == str(134719938886631424):
		if (mode == "dark"):
			r(msg, "Seriously...? Whatever.")
		elif (mode == "double"):
			r(msg, "(Seriously...? Whatever.)")
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

	elif mc(message, "Singidiva") or mc(message, "Singing Diva"):
		r(msg, "God of Light shall scorn on those who disrespect others. You must pray for His benevolence and forgiveness to have your soul cleansed.",
				"Mistress' name is Singidava you oaf! Learn to spell unless you want to risk rejoining God of Light early!")

	elif ms(message, "Hi Grisia") or ms(message, "Hi Sun") or ms(message, "Hello Grisia") or ms(message, "Hello Sun") or ms(message, "Hello SingiBot")  or ms(message, "!Hello"):
		r(msg, "The benevolent God of Light will forgive your sins.",
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

	elif ms(message, "!Whodunnit") or ms(message, "!Whodunit") or ms(message, "!Blackout") or ms(message, "!Black out"):
		r(msg, "http://www.youtube.com/watch?v=OYRknZ-6pRM")
	elif ms(message, "!Initial D") or ms(message, "!InitialD") or ms(message, "!Eurobeat") or ms(message, "!Cars") or ms(message, "!86"):
		if len(initiald) > 0:
			r(msg, random.choice(initiald))
	elif ms(message, "!Tsundere"):
		r(msg, "Dere dere~", "TSUN TSUN!")

	elif (mc(message, "I don't understand") or mc(message, "Wakaranai")) and not mc(message, "webm"):
		r(msg, "http://openings.moe/?video=Wakaranai.webm")
	elif ms(message, "!Windows") or ms(message, "!Linux") or ms(message, "!OSX") or ms(message, "!MAC"):
		r(msg, "http://openings.moe/?video=InstallLinux.webm")
	elif ms(message, "!Math"):
		r(msg, "http://openings.moe/?video=1441552323691.webm")
	elif ms(message, "!Maria") or ms(message, "!MaidBot") or ms(message, "!Maid"):
		r(msg, "https://www.youtube.com/watch?v=q2qBEsYtP04")
	elif ms(message, "!Kero") or ms(message, "!Frog") or ms(message, "!Sgt"):
		options = ["https://www.youtube.com/watch?v=qyJW_n-GY3E",
					"https://www.youtube.com/watch?v=9Xpc1TBCdPo",
					"https://www.youtube.com/watch?v=KUCJ0pfefzI"]
		r(msg, random.choice(options))
	elif ms(message, "!Puyo"):
		options = ["Ever heard of Puyo Puyo? https://www.youtube.com/watch?v=tt8nU-JqNsk#t=1m20s",
					"Want to try playing some Puyo Puyo yourself? http://www.puyovs.net/index.php",
					"Trying to improve your Puyo skills? http://puyonexus.net/wiki/How_to_Play_Puyo_Puyo"]
		r(msg, random.choice(options))
	elif ms(message, "!Go" or ms(message, "!Cosumi") or ms(message, "!Baduk") or ms(message, "!Weiqi") or ms(message, "!Igo")):
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

		if mode == "double" and (str(member1.id) == str(client.user.id) or str(member2.id) == str(client.user.id)):
				r(msg, "(Y-You must be joking...!)")
		elif mode == "dark" and (str(member1.id) == str(client.user.id) or str(member2.id) == str(client.user.id)):
				r(msg, "Y-You must be joking...!")
		elif mode == "double":
				r(msg, "(Hah! Serves you right!)")
		elif mode == "dark":
				r(msg, "Hah! Serves you right!")


	elif command:
		r(msg, message)
	
	
'''
# Run client
'''

client.run()