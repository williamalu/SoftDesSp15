""" Analyzes the word frequencies in a book downloaded from
	Project Gutenberg """

import string

def get_word_list(file_name):
	""" Reads the specified project Gutenberg book.  Header comments,
		punctuation, and whitespace are stripped away.  The function
		returns a list of the words used in the book as a list.
		All words are converted to lower case.
	"""
	input_book = open(file_name,'r')

	#turns book's text file into list of strings
	input_book_lines = input_book.readlines()
	
	#strips newline characters from input_book_lines
	for line in range(len(input_book_lines)):
		input_book_lines[line] = input_book_lines[line].strip()
	
	#removes empty strings from input_book_lines
	input_book_lines = filter(None, input_book_lines)
	
	#removes Project Gutenberg header
	lines = strip_gutenberg_header(input_book_lines)

	#strips punctuation marks and whitespace from each line
	for line in range(len(lines)):
		lines[line] = lines[line].translate(None, string.punctuation)

	#separates words from strings
	all_words = []
	for line in lines:
		all_words += line.split()

	#makes all words lowercase and strips whitespace
	for word in range(len(all_words)):
		all_words[word] = all_words[word].translate(None, string.whitespace)
		all_words[word] = all_words[word].lower()

	return all_words

def strip_gutenberg_header(input_book_lines):
	"""
	Strips Gutenberg Project header from book text files.
	"""
	lines = input_book_lines
	curr_line = 0
	while lines[curr_line].find('START OF THIS PROJECT GUTENBERG EBOOK') == -1:
		curr_line += 1
	return lines[curr_line+1:]

def get_top_n_words(word_list, n):
	""" Takes a list of words as input and returns a list of the n most frequently
		occurring words ordered from most to least frequently occurring.

		word_list: a list of words (assumed to all be in lower case with no
					punctuation
		n: the number of words to return
		returns: a list of n most frequently occurring words ordered from most
				 frequently to least frequentlyoccurring
	"""
	word_count = {}

	for word in word_list:
		if word not in word_count:
			word_count[word] = 1
		else:
			word_count[word] += 1

	ordered_by_frequency = sorted(word_count, key=word_count.get, reverse=True)

	return ordered_by_frequency[0:n]

if __name__ == "__main__":
	word_list = get_word_list('hound_of_baskervilles.txt')
	print get_top_n_words(word_list, 10)