#!/usr/bin/python
# Filename: generator.py

import sys
import random
import re
import string

def generate( per = 3 ):
	generates = []
	dictionary = file( '/usr/share/dict/words' ).readlines( )
	for i in range(0, per):
		r = random.randint( 0, len( dictionary ) )
		generates.append( dictionary[r] )
	exclude = set(string.punctuation)
	stringify = ' '.join( generates )
	stringify = ''.join(ch for ch in stringify if ch not in exclude)
	return stringify.replace( '\n ', ' ' )

if len( sys.argv ) > 1:
	if len( sys.argv ) > 2:
		print "Only using the first parameter"

	message = int( sys.argv[1] )
	print generate( per=message )
else:
	print generate( )

