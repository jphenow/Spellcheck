#!/usr/bin/python
# Filename: spellcheck.py
# Author: Jon Phenow <j.phenow@gmail.com>

import re
import collections
import string
import sys
from itertools import groupby
import timeit
from lib import * # Personal lib to simplify creation of generator

def distances( word ):
	splits     = splitter( word )
	replaces   = replacer( splits )
	return set( replaces )

def edits( words ):
	add_to_attempted = set()
	for word in words:
		for edit in distances( word ):
			if edit in dictionary:
				return [edit]
			elif edit not in attempted and edit not in add_to_attempted:
				add_to_attempted.add( edit )
	attempted.union( add_to_attempted )

def find_duplicates( string ):
	group = groupby( string )
	sequence = [(k, len(list(g)) >= 2) for k, g in group]
	allowed = set('aeioptslmfrcgktnbdzhu') 	# Sort of ordered in hopes that earlier letters occur more often, and some letters don't repeat
	return record_duplicates( '', sequence, range( 2, 3 ), allowed=allowed ) # '1' is taken care of - seems silly

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
		attempted.clear( )
else:
	message = set( sys.stdin.readlines( ) )
	for word in message:
		word = word.replace( '\n', '' ).strip( )
		sys.stdout.write( "Checking '" + word + "': " )
		sys.stdout.flush()
		sys.stdout.write( spellcheck( word ) + '\n' )
		attempted.clear( )
