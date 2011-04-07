#!/usr/bin/python
from main import TRIES, WORDLIST
from wordlist import wordlist
DEBUG = True

class wordwall(object):
	def __init__(self, chars, startword=""):		
		#this object will keep track of how much work has been done on itself
		#so we don't have to track iterations in many places
		self.iterations = 0
		self.maxiterations = TRIES
		self.mirrored = False		
		self.list = []
		self.specific_word = False
		if startword:
			self.specific_word = True
		self.set_new_size(chars, startword)

	def initialize_dictionary(self):
		#instantiate a word dictionary containing n letter words
		self.dictionary = wordlist(WORDLIST)
		self.dictionary.filter_n_chars(self.width)
		if not self.startword:
			self.startword = self.dictionary.get_random()
		else:
			#check validity of our starting word
			if not self.dictionary.in_dictionary(self.startword):
				raise ValueError("startword must already be in the dictionary file you chose.")

	def set_new_size(self, chars, startword=""):
		"""
		Initializes the wordwall with chars width, 
		and optional startword.
		"""
		#todo check for invalid input
		if startword and len(startword) != chars:
			raise ValueError("Chars must match the length of startword.")
		if chars < 2:
			raise ValueError("Chars must be non-negative and at least 2")
		self.width = chars
		self.startword = startword.upper()
		self.initialize_dictionary()
		self.list = []
		self.iterations = 0
		#clean our matrix, or set it up if it didn't exist
		self.make_matrix_clean()

	def set_row(self, row, word):
		#todo: bounds checking
		for i,j in enumerate(word):
			self.matrix[row][i] = j

	def set_column(self, column, word):
		#todo: bounds checking
		for i,j in enumerate(word):
			self.matrix[i][column] = j

	def get_row(self, row):
		temp = ""
		for i in self.matrix[row]:
			temp += i
		return temp

	def get_column(self, column):
		temp = ""
		for i in self.matrix:
			temp += i[column]
		return temp

	def make_matrix_clean(self):
		#better to represent this as a matrix?
		self.matrix = [["" for i in xrange(self.width)] for i in xrange(self.width)]
		self.set_row(0, self.startword)
		self.set_column(0, self.startword)
		
	def generate(self):
		#TODO crap, naive
		self.make_matrix_clean()
		self.iterations = 0
		for i,j in enumerate(self.startword):
			#for each letter
			if i == 0: 
				continue
			print i,j
			self.set_row(i, self.dictionary.get_random_by_letters(j))
			for k in xrange(self.width):
				if k == 0:
					continue
				while not self.is_legal_column(k):
					#print "column is %s" % self.get_column(k)
					self.set_row(i, self.dictionary.get_random_by_letters(j))
					self.iterate()
	def prepare_for_make(self):
		self.make_matrix_clean()
		self.master_list = [[] for i in xrange(self.width)]
		self.working_list = [[] for i in xrange(self.width)]
		self.chosen_word = [[] for i in xrange(self.width)]
		print "Starting with", self.startword
		if not self.specific_word:
			self.startword = self.dictionary.get_random()
		for i,j in enumerate(self.startword):
			if i == 0:
				continue
			else:
				self.master_list[i] = self.dictionary.get_words_by_letters(j)
				self.working_list[i] = self.dictionary.get_words_by_letters(j)
		
	def make(self):
		
		#already have a start_word
		#skip step 1 in procedure .txt
		#step 2 - make master list for each letter in start_word
		self.prepare_for_make()
		#now start looping
		i = 1 #i starting one row down from 0th, our start_word
		self.iterations = 0
		while i < self.width: #ordinal numbers vs counting
			self.iterate() #just increments a counter and bails us out
			if DEBUG: print "Level %i" % i
			#step 3 - pick a word
			if i <= 0:
				if self.specific_word:
					print "%i/%i iterations" % (self.iterations, self.maxiterations)
					#BAIL! we can't satisfy the requirements
					raise RuntimeError("Failed back to level 0 - %s. Bailing!" % self.startword)
				if DEBUG: print "iterations: %i" % self.iterations
				i = 1
				self.prepare_for_make()
				continue
			#randomly pop a word from the working list at this row
			try:
				self.chosen_word[i] = self.dictionary.pop_random_from_wordlist(\
									self.working_list[i])
				if DEBUG: print "i=%i chosen_word=%s" % (i, self.chosen_word)
			except IndexError:
				raise IndexError("Oh crap can't pop an empty list i=%iword=%slist=%s" % \
					(i,self.chosen_word,self.working_list))
			if self.chosen_word[i] is None:
				#empty working set; go up a level
				i -= 1
				continue
			#end of step 3, copy word to our wall at the row i
			self.set_row(i, self.chosen_word[i])
			#step 4 - check following columns for validity
			if i == self.width:
				#safety, shouldn't happen
				raise RuntimeError("Completed the wordwall but boned the logic somewhere.")
			else:
				j = i + 1
				
				while j < self.width:
					if DEBUG: print "Sublevel %i" % j
					#check that the current letters of column j
					#are contained in words in the working_list
					if DEBUG: print "check column ",self.get_column(j)
					chars = len(self.get_column(j))
					newlist = []
					for word in self.working_list[j]:
						if word[:chars] == self.get_column(j):
							newlist.append(word)
					#filter the working_list to only contain possible
					#words
					self.working_list[j] = newlist
					if len(self.working_list[j]) == 0:
						#the most recent chosen_word makes the
						#word wall impossible
						#go back one level
						if DEBUG: print "%s impossible, going back a level" % self.chosen_word[i]
						self.master_list[i].remove(self.chosen_word[i])
						#if len(self.master_list[1]) == 0:
						#	raise RuntimeError("Bailing, can't use any words to complete this wordwall.")
						self.working_list[i] = self.master_list[i][:]
						i -= 1 #start this level over
						break
					j += 1
					if DEBUG: print "OK"

				#made it through our rules successfully, let's go to the
				#next row
				i += 1
				

	def negenerate(self):
		self.make_matrix_clean()
		self.iterations = 0
		i = 0
		self.column_wordlist = []
		self.row_wordlist = [[] for word in xrange(self.width)]
		#row wordlist stores our attempted words
		#store our attempts to make sure we don't get stuck forever
		#if selecting fails
		#eventually, the tried words and the wordlist (possible words)
		#will match, and we should either bail out a level,
		#or bail completely
		while i < self.width:
			#might be off by one here, check
			self.iterate()
			print "Level %i" % i
			if i == -1:
				raise RuntimeError("Complete failiure from starting word. Try again with a different word.")
			elif i == 0:
				for j in self.startword[1:]:
					self.column_wordlist.append(\
					self.dictionary.get_words_by_letters(j))
					#SOMETHING WRONG EHRE
					if len(self.column_wordlist[i]) == 0:
						raise RuntimeError(\
						"No dictionary words with length %i start with %s" %\
						(self.width, j))
						i += 1
						break
			else:
				#no, get this from the column_wordlist
				#chosen_word = self.dictionary.get_words_by_letters(self.get_row(i))
				chosen_word = self.dictionary.get_random_from_wordlist(\
								self.column_wordlist[i])
				print "Let's try %s" % chosen_word

			#since we're only looking down and to the right
			#our index is one greater
			#check that the random word fits so far:
			#refer to part 2 in procedure for generating wordwall.txt
			for k in xrange(i-1, self.width):
				#might be off by one at self.width, check
				if i == 0:
					#first word in the matrix has already been
					#checked by now, don't check again
					#TODO might be dead code
					i += 1
					break
				#filter the column wordlists further
				#if there are no results when filtering,
				#go back one step, as there aren't any solutions
				filtered_list = []
				chars = len(self.get_column(k))
				#print k, self.column_wordlist
				try:
					print self.column_wordlist[k]
					for word in self.column_wordlist[k]:
						print "word, column",word[:chars], self.get_column(k)
						if word[:chars] == self.get_column(k):
							print word," was found"
							filtered_list.append(word)
				except IndexError:
					print k, self.column_wordlist
				if len(filtered_list) == 0:
					#we can't continue with that word since there
					#were no results, bail up one level and try
					#again
					print "Had to go back a level since list was empty"
					i -= 1
					break
				#keep the filtered list for the next round,
				#in order to save time
				print len(self.column_wordlist[k]), len(filtered_list)
				self.column_wordlist[k] = filtered_list
			i += 1

	def is_legal_column(self, column):
		if self.dictionary.in_dictionary(self.get_column(column)):
			return True
		return False

	def iterate(self):
		self.iterations += 1
		if self.iterations > self.maxiterations:			
			raise RuntimeError("took too many iterations, bailing")		

	def flatten(self):
		"""
		Returns a string representing the word wall matrix.
		"""
		temp = ""
		for i in self.matrix:			
			for j in i:
				temp += j
			temp += "\n"
		return temp[:-1] #nix the following newline
	
	def __repr__(self):
		return "Wordwall (%ix%i):\n%s" \
			% (self.width, self.width, self.flatten())
