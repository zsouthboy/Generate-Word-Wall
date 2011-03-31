#!/usr/bin/python
import random

class wordlist(object):
	def __init__(self, initial_words_file):
		self.file = initial_words_file
		self.list = []
		self.list_width = 0
		self.load_list()
		random.seed() #this shouldn't be done here

	def load_list(self):
		try:
			self.file = open(self.file, 'r')
			self.list = self.file.readlines()
			self.file.close()
		except IOError:
			print "Couldn't open %s, bailing!" % self.file
			exit(-1)

	def filter_n_chars(self, number_of_chars):		
		self.newlist = []
		for i in self.list:
			j = i.strip()
			if len(j) == number_of_chars:
				self.newlist.append(j)
		self.list = self.newlist
		self.set_list_width(number_of_chars)

	def set_list_width(self, number_of_chars):
		#todo check validity
		self.list_width = int(number_of_chars)

	def get_list_width(self):
		return self.list_width
		
	def get_random(self):
		return random.sample(self.list, 1)[0]

	def get_random_by_letters(self, start_letters):
		#VERY naive, can be trivially improved
		#memoization would be a possibly huge gain
		filtered = []
		letters = len(start_letters)
		#print start_letters
		for i in self.list:
			if i[:letters] == start_letters:
				filtered.append(i)
		return random.sample(filtered, 1)[0]

	def in_dictionary(self, word):
		#checks for first letters of each word
		#and whole words by extension
		if self.list_width == len(word):
			return word in self.list
		found = False
		for i in self.list:
			if i.find(word, 0, len(word)):
				found = True
				break

		return found

	def __len__(self):
		return len(self.list)