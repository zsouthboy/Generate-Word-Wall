WORDLIST = '/etc/dictionaries-common/words'
TARGETLIST = 'wordlist.txt'

dictionary = open(WORDLIST, 'r')
newfile = open(TARGETLIST, 'w')


for i in dictionary: #i will be one line
	#strip out the lines containing apostrophes
	#uppercase as well
	if i.find("'") == -1:
		newfile.write(i.upper())
		#print "found %s" % i

	