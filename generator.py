#!/usr/bin/python
""" Filename: generator.py
    Author: Jon Phenow <j.phenow@gmail.com>
    Description: A simple misspelled word generator
"""

import sys
import random
import re
import string
from itertools import groupby
from lib import *

# Using a less nice dictionary - we don't want to cut out the 'hard' stuff for the spellcheck
set_dictionary( set( re.findall( '.{2,}', file( '/usr/share/dict/words' ).read( ) ) ) )

"""Prepare an input word to be given random duplicate letters"""
def find_duplicates( word ):
    group = groupby( word )
    sequence = [( k, len( list( g ) ) <= 4 ) for k, g in group]
    allowed = string.letters
    return record_duplicates( '', sequence, range( 3, 4 ), allowed=allowed )

"""Run the lib editor functions and return the set of skrewed-up words"""
def edits( word ):
    splits = splitter( word )
    replaces = replacer( splits )
    caps = make_caps( splits )
    return set( replaces + caps )

"""Return a string of randomly editted words from the dictionary

per = number of random words to grab

"""
def generate( per = 10 ):
    generates = set()
    generates_return = set()
    random_dict = random.randrange( len( get_dictionary( ) ) )
    while len( generates ) < per:
        words = random.sample( get_dictionary( ), 10 )
        for i in range( 0, 3 ):         # Number of edit revisions for skrewing with words
            random_edits = random.sample( edits( random.sample( words, 1 )[0] ), 1 )[0]
            for a, b in splitter( random_edits ):
                if len( a ) <= len( a + b ) / 2 and len( a ) >= len( a + b ) / 2 - 2:
                    dups = find_duplicates( a )
                    generates.add( dups[len( dups ) / 2] + b )
    exclude = set( string.punctuation )
    stringify = ' '.join( generates )
    stringify = ''.join( char for char in stringify if char not in exclude )
    return stringify.replace( '\n ', ' ' ).replace( ' ', '\n' )

if "__name__" == "__main__":
    pass
else:
    try:
        if len( sys.argv ) > 1:
            message = int( sys.argv[1] )
            sys.stdout.write( generate( per=message ) )
            print
        else:
            sys.stdout.write( ( generate( ) ) )
            print
    except ValueError:
        print "Generator: Please use integer parameters only." 
