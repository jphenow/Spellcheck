#!/usr/bin/python
# Filename: spellcheck.py
# Author: Jon Phenow

import re
import collections
import string
import sys
from itertools import groupby
import timeit

attempted = []
exclude = set( string.punctuation )

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

def distances( word ):
	splits     = splitter( word )
	replaces   = replacer( splits )
	return set( replaces )

def edits( words ):
	for word in words:
		for edit in distances( word ):
			if edit in dictionary:
				return [edit]
			elif edit not in attempted:
				attempted.append( edit )

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
	sequence = [(k, len(list(g)) >= 2) for k, g in group]
	allowed = set('aeioptslmfrcgktnbdzhu') 	# Sort of ordered in hopes that earlier 
											# letters occur more often, and some letters don't repeat
	return record_duplicates('', sequence, allowed=allowed)

def words_only( text ):
	no_punctuation = ''.join( ch for ch in text if ch not in exclude )
	return set( re.findall( '[a-z]{1,}', no_punctuation.lower( ) ) )

def spellcheck( word ):
	word = word.lower()
	word = words_only( word ).pop()
	if word in dictionary:
		return word
	words = find_duplicates( word )
	candidates = known( words ) or edits( words ) or edits( attempted ) 
	if candidates:
		return candidates[0]
	else:
		return "NO SUGGESTION"

dictionary = set( words_only( file( '/usr/share/dict/words' ).read( ) ) )

if sys.stdin.isatty():
	print """
	Welcome to the Spell Checker!
	This spell checker currently checks for:
	* A-Z english words
	* capitalization errors
	* duplicate letters
	* misspelled vowels

	- It currently picks the first close-spelling
		word for speed
	- Punctuation and non A-Z characters are omitted
	"""
	while 1 == 1: 
		word = raw_input( '> ' )
		print spellcheck( word )
		del attempted[:]
else:
	message = set( sys.stdin.readlines( ) )
	for word in message:
		word = word.replace( '\n', '' ).strip( )
		sys.stdout.write( "Checking '" + word + "': " )
		sys.stdout.flush()
		sys.stdout.write( spellcheck( word ) + '\n' )
		del attempted[:]
