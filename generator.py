#!/usr/bin/python
# Filename: generator.py
# Author: Jon Phenow <j.phenow@gmail.com>
# Description: A relatively slow misspelled word generator

import sys
import random
import re
import string
from itertools import groupby
from lib import *

# Using a less nice dictionary - we don't want to cut out the 'hard' stuff for the spellcheck
dictionary = set( re.findall( '.{2,}', file( '/usr/share/dict/words' ).read( ) ) )

def find_duplicates( word ):
	group = groupby( word )
	sequence = [( k, len( list( g ) ) <= 7 ) for k, g in group]
	allowed = string.letters
	return record_duplicates( '', sequence, range( 2, 3 ), allowed=allowed )

def edits( word ):
	splits = splitter( word )
	replaces = replacer( splits )
	duplicates = find_duplicates( word )
	caps = make_caps( splits )
	return set( duplicates + replaces + caps )

def generate( per = 10 ):
	generates = set()
	generates_return = set()
	random_dict = random.randrange( len( dictionary ) )
	while len( generates ) < per:
		word = random.sample( dictionary, 1 )[0]
		dictionary.add( word )
		if word not in generates:
			generates.add( word )
		for i in range( 0, 3 ): # Should consider making a param
			# Not the most efficient, but reusing word variable can cause overuse of word for edits for parameters of over 10
			random_edits = random.sample( edits( random.sample( dictionary, 1 )[0] ), 1 )[0] 
			if random_edits not in generates:
				generates.add( random_edits )
	exclude = set( string.punctuation )
	stringify = ' '.join( generates )
	stringify = ''.join(ch for ch in stringify if ch not in exclude)
	return stringify.replace( '\n ', ' ' ).replace( ' ', '\n' )

if len( sys.argv ) > 1:
	message = int( sys.argv[1] )
	sys.stdout.write( generate( per=message ) )
	print
else:
	sys.stdout.write( ( generate( ) ) )
	print
