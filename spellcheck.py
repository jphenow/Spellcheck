#!/usr/bin/python
""" Filename: spellcheck.py
 Author: Jon Phenow <j.phenow@gmail.com>
 Description: 
    Quickly achieves a spellcheck for any errors of the following:

        * Mis-capitalized
        * Repeated letters
        * Incorrect vowels
    Currently set to utilze the Unix /usr/share/dict/words for a dictionary
    Simply run "python spellcheck.py" or "./spellcheck.py" for a prompt-based check
    or use a command line pipe such as "echo misspelled.txt | ./spellcheck.py"
"""

import re
import string
import sys
from itertools import groupby
from lib import * # Personal lib to simplify creation of generator

attempted = [] # Running list of words to reiterate through if necessary

"""Mess with a word and return candidates"""
def jumble_word( word ):
    splits = splitter( word )
    replaces = replacer( splits )
    return set( replaces )

"""Run through jumble_word() and check its given list of edits to be in the dictionary"""
def edits( words ):
    for word in words:
        for edit in jumble_word( word ):
            if edit in get_dictionary( ):
                return [edit]
            elif edit not in attempted:
                attempted.append( edit )

"""Prep to check if there's acceptable duplication going on (less than two in a row)
	and return all possible alternatives to the word with duplications "fixed"
"""
def find_duplicates( word ):
    group = groupby( word )
    sequence = [( k, len(list( g ) ) >= 2 ) for k, g in group]
    allowed = set('aeioptslmfrcgktnbdzhuy')
    return record_duplicates( '', sequence, range( 2, 3 ), allowed = allowed, check_dup = True )

"""Process the word for an early check then do the real processing, while continuing to
	check in hopes of a quick answer
"""
def spellcheck( word ):
    word = word.lower()
    word = words_only( word ).pop()
    if word in get_dictionary( ):
        return word
    words = set( find_duplicates( word ) ).union( [word] )
    candidates = known( words ) or edits( words ) or edits( attempted )
    if candidates:
        return candidates[0]
    else:
        return "NO SUGGESTION"

if "__name__" == "__main__":
	pass
else:
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
            if len( word ) > 0:
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
