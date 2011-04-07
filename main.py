#!/usr/bin/python
VERSION = "generate word wall 0.1 (2011-03-30)"
WORDLIST = "wordlist.txt"
TRIES = 10000000
MIRRORED = False #TODO this is terrible
import sys, os
from wordlist import *

#Steps:
#For a size n passed on command line
#Filter wordlist.txt for n letter long words
#randomly select a word from filtered list
#next, for each letter following the first,
#randomly select a word that starts with that letter
#check for valid words in left to right
#and top to bottom
#on failiure, do random selection again

def print_usage():
	usage = """
	USAGE: python main.py (starting_word | number_of_characters) {mirrored}

	The script will attempt to build a word wall
	with either the word passed (if in the dictionary)
	or the desired number of characters, naively.
	Pass 1 for mirrored to search only for mirror word walls."""

	print VERSION
	print usage
	exit(-1)

def main(number_of_characters, word=""):
	#get a filtered wordlist for the number
	words = build_wordlist(number_of_characters)
	#check that the word we were passed, if any,
	#exists in the set
	if word:
		if not words.in_dictionary(word.upper()):
			print "%s wasn't found in the dictionary, bailing!" % word
			exit(-1)

	#print "length is %i!" % len(words)
	#print "list width is now %i" % words.get_list_width()
	#print "a random word is now %s" % words.get_random()

		wall = build_wordwall(words, word.upper())
	else:
		wall = build_wordwall(words)
	for i in wall:
		print i


def build_wordlist(number_of_characters):
	words = wordlist(WORDLIST)
	words.filter_n_chars(number_of_characters)
	return words

def build_wordwall(words, firstword=""):
	#for width of the wall, grab one word
	if not firstword:
		firstword = words.get_random()

	wordwall = generate_wordwall_randomly(firstword, words)	
	#print "wordwall is %i long" % len(wordwall)
	

	#we now have a list with n words in it
	#list is aligned by first column
	
	#check each column past the first for word existence
	#if no, do this ALL over again from the first word
	iterations = 0
	while not wordwall_columns_are_words(wordwall, words):
		wordwall = generate_wordwall_randomly(firstword, words)	
		iterations += 1
		if iterations > TRIES:
			#couldn't find a matching set of words
			#bail for now, TODO NAIVE
			print "Couldn't match after %i tries, bailing!" % TRIES
			exit(-1)

	return wordwall

def generate_wordwall_randomly(firstword, words):
	#TODO NAIVE CRAP POOR
	#for each letter of the wall after 0,
	#grab words until obtaining word that starts
	#with the letter at n
	#check that the word selected's prefixes exist in the
	#dictionary. if not, choose another word

	wordwall = [firstword]
	for i,j in enumerate(firstword):
		if i == 0:
			pass
		else:
			#for each word in word wall
			#check columns
			#if a column prefix isn't in dictionary
			#bail and try again

			wordwall.append(words.get_random_by_letters(firstword[i]))
			#print wordwall
			iterations = 0
			while not wordwall_columns_are_words(wordwall, words):
				del wordwall[-1]
				wordwall.append(words.get_random_by_letters(firstword[i]))
				iterations += 1
				if iterations > TRIES:
					print "Couldn't find words in %i tries, bailing!" % TRIES
					exit(-1)
		
	return wordwall

def wordwall_columns_are_words(wordwall, word_dictionary):
	"""Returns a boolean indicating the words/prefixes formed
	by the columns of the wall are in the dictionary
	"""
	#TODO NAIVE CRAP POOR
	newlist = []
	length = len(wordwall)
	for i in xrange(length):
		newword = ""
		for j in xrange(length):
			newword += wordwall[j][i]		
		newlist.append(newword)

	for i in newlist:
		if not word_dictionary.in_dictionary(i):
			return False

	return True

if __name__ == "__main__":
	if sys.argv < 2:
		print_usage()
	else:
		try:
			MIRRORED = bool(sys.argv[2])
		except IndexError:
			pass
		if sys.argv[1].isalpha():
			#if this is a word, detect so
			main(len(sys.argv[1]), sys.argv[1])
		else:
			main(int(sys.argv[1]))