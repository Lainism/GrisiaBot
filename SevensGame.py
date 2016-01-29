from threading import Timer
from discord import PrivateChannel
import discord
import random

class SevensGame(object):

	END_CARDS = ["AH", "AD", "AS", "AC", "KH", "KD", "KS", "KC"]
	HIGH_CARDS = ["7H", "8H", "9H", "10H", "KnH", "QH", "KH", "7D", "8D", "9D", "10D", "KnD", "QD", "KD",
					"7S", "8S", "9S", "10S", "KnS", "QS", "KS", "7C", "8C", "9C", "10C", "KnC", "QC", "KC"]
	LOW_CARDS = ["AH", "2H", "3H", "4H", "5H", "6H", "7H", "AD", "2D", "3D", "4D", "5D", "6D", "7D",
					"AS", "2S", "3S", "4S", "5S", "6S", "7S", "AC", "2C", "3C", "4C", "5C", "6C", "7C"]

	def __init__(self, client, msg):
		self.channel = msg.channel
		self.client = client
		self.players = [msg.author]
		self.deck = []
		self.hands = {}
		self.max_time = 60
		self.active = False
		self.free = []
		self.penalty = None
		self.turn = msg.author
		self.t = Timer(self.max_time, self.force_card, [])

		client.send_message(msg.channel, "Would anyone like to join us for a game of sevens? If you'd like to enter, use command !Join sevens.")

	def join(self, player):
		if self.active:
			self.client.send_message(self.channel, "The registering period for the current game has already ended.")
			return
		elif len(self.players) > 5:
			self.client.send_message(self.channel, "There can't be more than six players.")
			return

		if player in self.players:
			self.client.send_message(self.channel, player.mention() + " has already been registered as a player.")
			return

		self.players.append(player)
		self.client.send_message(self.channel, player.mention() + " has been registered as a player.")

	def get_next_card(self, card):
		if not self.active:
	#		print("Can't get the next card if the game is not running.")
			return []

		if card in self.END_CARDS:
	#		print("Card is in end cards.")
			return []

		new_cards = []

		if card in self.HIGH_CARDS:
			next_card = self.HIGH_CARDS[self.HIGH_CARDS.index(card) + 1]
			new_cards.append(next_card)
	#		print("Card is high.")
	#		print(self.HIGH_CARDS.index(card))

		if card in self.LOW_CARDS:
			next_card = self.LOW_CARDS[self.LOW_CARDS.index(card) - 1]
			new_cards.append(next_card)
	#		print("Card is low.")
	#		print(self.LOW_CARDS.index(card))

	#	print("Returning " + str(new_cards))
		return new_cards

	def get_next_player(self, player):
		pid = self.players.index(player)
		if pid >= (len(self.players) - 1):
			return self.players[0]
		return self.players[pid + 1]

	def get_turn(self):
		return turn.mention()

	def set_max_time(self, player, time):

	#	if self.active:
	#		self.client.send_message(self.channel, "Turn maximum time can't be set when the game is active.")
	#		return

		if not((player in self.players) or (str(player.id) == str(134719938886631424))):
			self.client.send_message(self.channel, "Only my Mistress or the players can change the game settings.")
			return

		if (time > 200) or (time < 5):
			self.client.send_message(self.channel, "Please select a value between 5 and 200.")
			return

		self.max_time = time
		self.client.send_message(self.channel, "Turn maximum time has been set to " + str(self.max_time) + " seconds.")

	def create_deck(self):
		self.deck = ["AH", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "KnH", "QH", "KH",
						"AD", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "KnD", "QD", "KD",
						"AS", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "KnS", "QS", "KS",
						"AC", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "KnC", "QC", "KC"]

	def check_hand(self, player):

		if player not in self.players:
			self.client.send_message(player, "You don't have any cards.")
			return
		
		if not self.active:
			self.client.send_message(player, "The game hasn't started yet.")
			return
			
		hand = self.hands.get(player.id)
		hand.sort()
		
		h = ""
		for card in hand:
			h += " " + card

		a = ""
		for card in hand:
			if card in self.free:
				a += " " + card

		self.client.send_message(player, "Your current cards are:" + h)
		self.client.send_message(player, "Currently playable cards in your hand are:" + a)

	def check_available_cards(self, player):
		hand = self.hands.get(player.id)
		available = []
		for card in hand:
			if card in self.free:
				available.append(card)
		return available

	def check_penalty(self, player, ch):
		self.client.send_message(ch, "The player currently holding the penalty is " + self.penalty.mention() + ".")

	def calculate_penalties(self):
		scores = []
		for player in self.players:
			hand = self.hands.get(player.id)
			points = 0
			for card in hand:
				if card[0] == 'A':
					points += 14
				elif (card[0] == 'K') and (len(card) < 3):
					points += 13
				elif card[0] == 'Q':
					points += 12
				elif card[0] == 'K':
					points += 11
				elif card[0] == '1':
					points += 10
				else:
					points += int(card[0])
	#			print(points)

			if self.penalty == player:
				points += 15

			scores.append((player, points))

		try:
			self.client.send_message(self.channel, "The player who got the penalty is " + self.penalty.mention() + ".")
		except:
			self.client.send_message(self.channel, "No one got the penalty in this game.")

		scores.sort(key=lambda tup: tup[1])
		self.client.send_message(self.channel, "Final scores:")
		for score in scores:
			self.client.send_message(self.channel, score[0].mention() + ": " + str(score[1]) + " points")

		self.client.send_message(self.channel, "Congratulations for the winner and thank you for playing. To end the current game, please say !end game.")
		self.active = False

	def win_game(self, player):
		self.t.cancel()
		self.client.send_message(self.channel, player.mention() + " has no more cards left and therefore the round has ended. The person with the least penalty points is the victor.")
		self.client.send_message(self.channel, "Calculating penalty points...")
		self.calculate_penalties()

	def force_card(self):
		self.client.send_message(self.channel, "Time is up. Sun will play a card for " + self.turn.mention() + ".")

		self.grisia_plays()

	def grisia_plays(self):
		available = self.check_available_cards(self.turn)
		if len(available) < 1:
			self.play_card("empty", self.turn, self.channel)
			return
		self.play_card(random.choice(available), self.turn, self.channel)

	def play_card(self, card, player, ch):
		if player != self.turn:
			self.client.send_message(ch, "It is not your turn.")
			return

		hand = self.hands.get(player.id)

		if card == "empty":
			if len(self.check_available_cards(player)) > 0:
				self.client.send_message(ch, "You still have cards that fit.")
				return
			self.penalty = player
			self.client.send_message(self.channel, player.mention() + " took the penalty.")

		elif card not in self.free:
			self.client.send_message(ch, "This card does not fit.")
			return

		elif card not in hand:
			self.client.send_message(ch, "You don't have that card.")
			return
		else:
			hand.remove(card)
			self.free.remove(card)

			self.client.send_message(self.channel, player.mention() + " played card " + card + ".")

			new_cards = self.get_next_card(card)
			for card in new_cards:
				self.free.append(card)

		if len(hand) < 1:
			self.win_game(player)
			return

		self.free.sort()

		s = ""
		for f in self.free:
			s += f + " "

		self.client.send_message(self.channel, "The current free slots are: " + s + "")
		self.turn = self.get_next_player(player)
		self.client.send_message(self.channel, self.turn.mention() + " plays next. You have " + str(self.max_time) + " seconds to play your card.")

		if str(self.turn.id) == str(self.client.user.id):
	#		print("Sun's turn.")
			self.t = Timer(5.0, self.grisia_plays, [])
		else:
			# Start next turn timer
			self.t = Timer(self.max_time, self.force_card, [])
		self.t.start()

	def deal_cards(self):
		self.create_deck()

		random.shuffle(self.players)

		# Deal the cards
		for player in self.players:
			hand = []
			for i in range (0, int(52/len(self.players))):
				card = random.choice(self.deck)
				self.deck.remove(card)
				hand.append(card)
			self.hands[player.id] = hand

		# Share the remaining cards
		counter = 0
		next_player = self.turn
		for card in self.deck:
			self.hands.get(next_player.id).append(card)
			next_player = self.get_next_player(next_player)
			counter += 1

		self.create_deck()
		self.free = ["7H", "7D", "7S", "7C"]

	def start_game(self, ch):
		if len(self.players) == 2 and (self.client.user not in self.players):
			self.client.send_message(self.channel, "Because there are only two players Sun will join as the third player.")
			self.join(self.client.user)

		if len(self.players) < 2:
			self.client.send_message(ch, "The game needs at least two players.")
			return
		

		self.active = True
		self.client.send_message(self.channel, "Stating the game of sevens...")

		self.deal_cards()

		for player in self.players:
			hand = self.hands.get(player.id)
			if "7C" in hand:
				self.turn = player
				self.play_card("7C", player, self.channel)
				break

	def end_game(self, player):
		if not self.active:
			self.t.cancel()
			return True
		elif (player in self.players) or (str(player.id) == str(134719938886631424)):
			self.t.cancel()
			return True

		self.client.send_message(self.channel, "Only my Mistress or players can end the current game.")
		return False
