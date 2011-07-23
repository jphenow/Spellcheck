#!/usr/bin/python
# Filename: spellcheck.py

import re
import collections
import string
import sys
from itertools import groupby
import timeit

attempted = []
exclude = set(string.punctuation)

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
	allowed = ('aeioupt')
	return record_duplicates('', sequence, allowed=allowed)

def words_only( text ):
	no_punctuation = ''.join( ch for ch in text if ch not in exclude )
	return set( re.findall( '[a-z]{1,}', no_punctuation.lower( ) ) )

def prep( features ):
	model = collections.defaultdict( lambda: 1 )
	for f in features:
		model[f] += 1
	return model

def spellcheck( word ):
	print word
	word = word.lower()
	english_only = words_only( word )
	if not english_only:
		return "NO SUGGESTION: English letters only"
	if word in dictionary:
		return word
	words = find_duplicates( word )
	candidates = known(words) or edits( words ) or edits( attempted ) 
	if candidates:
		max_return = candidates[0] #max(candidates, key=lambda w: dictionary[w])
		return max_return
	else:
		return "NO SUGGESTION"

dictionary = set( prep( words_only( file( '/usr/share/dict/words' ).read( ) ) ) )

if sys.stdin.isatty():
	print """
	Welcome to the Spell Checker!
	This spell checker currently checks for:
	* A-Z english words
	* capitalization errors
	* duplicate letters
	* misspelled vowels

	It currently picks the first close-spelling word for speed
	"""
	while 1 == 1: 
		word = raw_input( '> ' )
		print spellcheck( word )
else:
	message = sys.stdin.read().split( ' ' )
	print "Running batch using:\n", ', '.join( message )
	for word in message:
		word = word.replace( '\n', '' )
		print spellcheck( word )
