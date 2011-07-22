#!/usr/bin/python
# Filename: generator.py

import sys
import random
import re
import string
from itertools import groupby

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
	solutions = record_duplicates(previous + sequence[0][0], sequence[1:], allowed=allowed)
	if sequence[0][0] in allowed and sequence[0][1]:
		solutions += record_duplicates(previous + sequence[0][0] * 2, sequence[1:], allowed=allowed)
	return solutions

def find_duplicates( string ):
	group = groupby( string )
	sequence = [(k, len(list(g)) >= 7) for k, g in group]
	allowed = ('aeioupt')
	return record_duplicates('', sequence, allowed=allowed)

def make_caps( splits ):
	caps = []
	for a, b in splits:
		b = b.upper()
		caps.append( b )
	return caps

def edits( word ):
	splits = splitter( word )
	replaces = replacer( splits )
	duplicates = find_duplicates( word )
	caps = make_caps( splits )
	return set( duplicates + replaces + caps )

def generate( per = 10 ):
	generates = []
	generates_return = []
	dictionary = file( '/usr/share/dict/words' ).readlines( )
	random_dict = random.randint( 0, len( dictionary ) )
	for i in range( 0, per ):
		generates.append( dictionary[random_dict] )
		for j in range( 0, per ):
			generates += edits( generates[j] )
		random_return = random.randint( 0, len( generates )-1 )
		generates_return.append( generates[random_return] )
	exclude = set( string.punctuation )
	stringify = ' '.join( generates_return )
	stringify = ''.join(ch for ch in stringify if ch not in exclude)
	return stringify.replace( '\n ', ' ' )

if len( sys.argv ) > 1:
	if len( sys.argv ) > 2:
		print "Only using the first parameter"

	message = int( sys.argv[1] )
	print generate( per=message )
else:
	print generate( )

