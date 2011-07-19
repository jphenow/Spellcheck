#!/usr/bin/python
# spellcheck.py

import re
import collections
import string
from itertools import groupby

attempted = []

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

def words_only( text ): return re.findall( '[a-z]{2,}', text.lower( )) 

def prep( features ):
	model = collections.defaultdict( lambda: 1 )
	for f in features:
		model[f] += 1
	return model

def spellcheck(word):
	word = word.lower()
	words = find_duplicates( word )
	candidates = known(words) or edits( words ) or edits( attempted ) or edits( attempted.reverse() )
	if candidates:
		max_return = candidates[0] #max(candidates, key=lambda w: dictionary[w])
		return max_return
	else:
		return "NO SUGGESTION"

dictionary = prep( words_only( file( '/usr/share/dict/words' ).read( ) ) )

while 1 == 1: 
	word = raw_input( '> ' )
	print spellcheck( word )
	attempted = []

