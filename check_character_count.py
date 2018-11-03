"""
Description:
	My fiancée asked me to write the story of my proposal to her,
	as told from my perspective, for our wedding website. However the site
	constrained our entries to at most 2,000 characters.

	I quickly wrote this script so that I can write my story in a text file
	and get a nearly-live character count.

Execution example:
	In command line,
	./check_character_count.py FILE_PATH/mystory.txt
"""

#!/usr/bin/env python

import sys
from time import sleep
from os.path import getsize

def text_counts(text):
	words = text.replace('.', '').replace('\n', '').split(' ')
	character_count = len(text)
	word_count = len(words)
	return {'character_count': character_count, 'word_count': word_count}

def check_length(file_name):
	with open(filename) as file:
		lines = file.readlines()
		text = ' '.join(lines)
		counts = text_counts(text)
		character_count = counts['character_count']
		word_count = counts['word_count']
		print(f"Word count: {word_count}, Character count: {character_count}         ", end='\r')


if __name__ == '__main__':
	filename = './' + sys.argv[1]
	file_size = getsize(filename)
	print(f"Starting file size: {file_size}", end='\r')
	while True:
		temp_file_size = getsize(filename)
		if temp_file_size != file_size:
			check_length(filename)
			file_size = temp_file_size
		sleep(0.5)
