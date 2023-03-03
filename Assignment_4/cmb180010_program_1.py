"""
CS 4395.001 Human Language Technologies
Portfolio Chapter 8: Ngrams Program 1
Cady Baltz (cmb180010)
3/3/2023
"""

import pickle
import os
import re
from nltk import word_tokenize
from nltk.util import ngrams

# Hardcoding constant values for file paths used in this program
DATA_FILES = ['data/LangId.train.English', 'data/LangId.train.French', 'data/LangId.train.Italian']

def create_dictionaries(filename):
    """
      Processes an input file to extract its unigrams and bigrams, then returns a dictionary containing their counts
      Args:
          filename: Relative path to the user's data file
      Returns:
          unigram_dict: A dictionary mapping a unigram (e.g. 'token') to its integer count in the text
          bigram_dict: A dictionary mapping a bigram (e.g. 'token1 token2') to its integer count in the text
      Example:
        Assume "file" contains the text "example text here example text"

        >>> create_dictionaries("file")

        >>> { 'example': 2, 'text': 2, 'here': 1}
        >>> { 'example text': 2, 'text here': 1, 'here example': 1}
    """

    # try opening the file with the given filename
    try:
        # use utf8 encoding to handle foreign languages
        file = open(filename, "r", encoding="utf8")
    except IOError:
        print('Error: The specified relative file path is not valid')
        return None

    # read in the text and remove new lines
    text = file.read()
    text = re.sub('\n', '', text)

    # use NLTK to tokenize the text
    tokens = word_tokenize(text)

    # use NLTK to create a unigrams list
    unigrams = list(ngrams(tokens, 1))

    # use NLTK to create a bigrams list
    bigrams = list(ngrams(tokens, 2))

    # use the unigram list to create a dictionary of unigrams and counts
    # data format: ['token'] -> count
    unigram_dict = {t[0]: unigrams.count(t) for t in set(unigrams)}

    # use the bigram list to create a dictionary of bigrams and counts
    # data format: ['token1 token2'] -> count
    bigram_dict = {b[0] + ' ' + b[1]:bigrams.count(b) for b in set(bigrams)}

    return unigram_dict, bigram_dict


if __name__ == '__main__':
    """
      Creates and pickles unigram and bigram dictionaries for all input files specified in the DATA_FILES constant
      Args: None
      Returns: None
    """

    # call the create_dictionaries() for each input file
    for file in DATA_FILES:
        result = create_dictionaries(file)
        if result is not None:

            # create two files with appropriate filenames
            unigram_filename = 'pickle_output/' + os.path.basename(file) + '_unigrams' + '.p'
            bigram_filename = 'pickle_output/' + os.path.basename(file) + '_bigrams' + '.p'

            os.makedirs(os.path.dirname(unigram_filename), exist_ok=True)
            os.makedirs(os.path.dirname(bigram_filename), exist_ok=True)

            # use pickle to dump the returned unigram and bigram dictionaries for later use
            pickle.dump(result[0], open(unigram_filename, 'wb'))
            pickle.dump(result[1], open(bigram_filename, 'wb'))