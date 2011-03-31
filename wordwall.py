#!/usr/bin/python
from main import TRIES

class wordwall(object):
	def __init__(self, dictionary, startword=""):
		self.length = 0
		#this object will keep track of how much work has been done on itself
		#so we don't have to track iterations in many places
		self.iterations = 0
		self.maxiterations = TRIES
		self.mirrored = False
		self.dictionary = dictionary
		self.list = []
		if not startword:
			startword = self.dictionary.
		self.initialize(startword)

	def initialize(self, word):
		"""
		Initializes the wordwall object, using the 