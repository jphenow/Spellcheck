# Spellcheck

Relatively simple spellchecker packed with a super mini library of tools, a misspelled-word generator and some sample words

## Running

### Spellchecker
	
The prompt:
    ./spellchecker.py
or
    python spellchecker.py

Pipe:
    cat standard_words | ./spellchecker.py
or
    ./generator | ./spellchecker.py

### Generator
	
Standard 10 word output:
    ./generator.py
or
    python generator.py

May use a parameter for more words:
    ./generator.py 100
or
    python generator.py 100

## General info
	
Author: Jon Phenow <j.phenow@gmail.com>
Quickly achieves a spellcheck for any errors of the following:

- Mis-capitalized
- Repeated letters
- Incorrect vowels

Currently set to utilze the Unix /usr/share/dict/words for a dictionary

