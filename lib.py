#!/usr/bin.python
"""	Filename: lib.py
	Author: Jon Phenow <j.phenow@gmail.com>
	Description: Simple library of some important functions for spellchecking
"""

import re
import string

"""Slice the word at each char so we have a cursor for working edits"""
def splitter( word ):
	splits = []
	for i in range( len( word ) + 1 ):
		splits.append( ( word[:i], word[i:] ) )
	return splits

"""Since we're only worried about vowels check each letter to be a vowel,
	then create a list of words with every vowel tried
"""
def replacer( splits ):
	vowel= "aeiou"
	replaces = []
	for a, b in splits:
		if len(b) > 0 and b[0] in vowel:
			for c in vowel:
				replaces.append( a + c + b[1:] )
	return replaces

"""Yes, it actually cycles through a set of words and checks if one is in the dictionary."""
def known( words ):
	for word in words:
		if word in dictionary:
			return [word]

"""Recursive function to grab each acceptable letter and return a list of words that have
	a certain number of duplicated, acceptable letters.
"""
def record_duplicates( previous,						# Previously checked sequence
					sequence, 							# To be checked
					amount, 							# A range for allowable duplicates
					allowed = string.letters,			# Letters allowed to be duplicated 
					check_dup = False):					# Necessary for spellcheck speed (not generator)
	if not sequence:
		return [previous]
	solutions = []
	if check_dup:
		solutions += record_duplicates( previous + sequence[0][0],
									sequence[1:],
									amount,
									allowed = allowed,
									check_dup = check_dup )
	for i in amount:
		if sequence[0][0] in allowed and ( ( check_dup and sequence[0][1] ) or not check_dup ): 
			solutions += record_duplicates( previous + sequence[0][0] * i,
										sequence[1:],
										amount,
										allowed=allowed,
										check_dup = check_dup )
	return solutions

"""Remove the punctuation we don't want to deal with and make sure to get words above length 2"""
def words_only( text ):
	exclude = set( string.punctuation )
	no_punctuation = ''.join( ch for ch in text if ch not in exclude )
	return set( re.findall( '[a-z]{2,}', no_punctuation.lower( ) ) )

"""Switches the second element in the parameter to uppercase"""
def make_caps( splits ):
	caps = []
	for a, b in splits:
		b = b.upper()
		caps.append( a + b )
	return caps

"""Retrieve the dictionary being used throughout the library"""
def get_dictionary( ):
	return dictionary

dictionary = set( words_only( file( '/usr/share/dict/words' ).read( ) ) )
