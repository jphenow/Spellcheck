#!/usr/bin/python
# Filename: generator.py

import sys
import random
import re
import string
from itertools import groupby

dictionary = set( re.findall( '.{2,}', file( '/usr/share/dict/words' ).read( ) ) )

def splitter( word ):
	splits = []
	for i in range( len( word ) + 1 ):
		splits.append( ( word[:i], word[i:] ) )
	return splits

def replacer( splits ):
	vowel= "aeiou"
	replaces = []
	for a, b in splits:
		for c in vowel:
			if b:
				replaces.append( a + c + b[1:] )
	return replaces

def known( words ):
	for word in words:
		if word in dictionary:
			return [word]
		elif word not in attempted:
			attempted.append( word )

def record_duplicates( previous, sequence, allowed='aeiou' ):
	if not sequence:
		return [previous]
	solutions = []
	for i in range( 2, 4 ): # 7 is arbitrary, just something to show duplicated letters
		if sequence[0][0] in allowed and sequence[0][1]:
			solutions += record_duplicates( previous + sequence[0][0] * i, sequence[1:], allowed=allowed )
	return solutions

def find_duplicates( word ):
	group = groupby( word )
	sequence = [( k, len( list( g ) ) <= 7 ) for k, g in group]
	allowed = string.lowercase
	return record_duplicates( '', sequence, allowed=allowed )

def make_caps( splits ):
	caps = []
	for a, b in splits:
		b = b.upper()
		caps.append( a + b )
	return caps

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
	return stringify.replace( '\n ', ' ' )

if len( sys.argv ) > 1:
	if len( sys.argv ) > 2:
		print "Only using the first parameter... "
	message = int( sys.argv[1] )
	print generate( per=message )
else:
	print generate( )
