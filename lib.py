#!/usr/bin.python
# Filename: lib.py
# Author: Jon Phenow <j.phenow@gmail.com>

import re
import collections
import string
import sys
from itertools import groupby

global exclude
global dictionary
global attempted

def splitter( word ):
	splits = []
	for i in range( len( word ) + 1 ):
		splits.append( ( word[:i], word[i:] ) )
	return splits

def replacer( splits ):
	vowel= "aeiou"
	replaces = []
	for a, b in splits:
		if len(b) > 0 and b[0] in vowel:
			for c in vowel:
				replaces.append( a + c + b[1:] )
	return replaces

def known( words ):
	for word in words:
		if word in dictionary:
			return [word]
		elif word not in attempted:
			attempted.add( word )

def record_duplicates( previous,		# Previously checked sequence
					sequence, 			# To be checked
					amount, 			# A range for allowable duplicates
					allowed ):			# Letters allowed to be duplicated 
	if not sequence:
		return [previous]
	solutions = record_duplicates( previous + sequence[0][0], sequence[1:], amount, allowed=allowed )
	for i in amount:
		if sequence[0][0] in allowed and sequence[0][1]:
			solutions += record_duplicates( previous + sequence[0][0] * i, sequence[1:], amount, allowed=allowed )
	return solutions

def words_only( text ):
	no_punctuation = ''.join( ch for ch in text if ch not in exclude )
	return set( re.findall( '[a-z]{1,}', no_punctuation.lower( ) ) )

def make_caps( splits ):
	caps = []
	for a, b in splits:
		b = b.upper()
		caps.append( a + b )
	return caps

exclude = set( string.punctuation )
dictionary = set( words_only( file( '/usr/share/dict/words' ).read( ) ) )
attempted = set()
