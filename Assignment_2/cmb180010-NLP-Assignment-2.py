"""
CS 4395.001 Human Language Technologies
Portfolio Chapter 5: Word Guess Game
Cady Baltz (cmb180010)
2/18/2022
"""

import sys
from nltk import pos_tag
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from random import randint


def calculate_lexical_diversity(text):
    '''
      Calculates and outputs the lexical diversity (number of unique tokens divided by the total number of tokens) of a given text
      Args:
        text: string to be processed 
      Returns: None
      Example:
        >>> calculate_lexical_diversity('hi hello hi bye')
        >>> Lexical diversity: 0.75
    '''

    # use NLTK to tokenize the given text (with no pre-processing)
    all_tokens = word_tokenize(text)

    # keep track of tokens you have already encountered
    unique_tokens = set()

    # calculate the sum of unique tokens
    total_unique_tokens = 0

    # iterate through every token once
    for token in all_tokens:

        # if this is your first time encountering this token, increment the number of unique tokens
        if token not in unique_tokens:
            total_unique_tokens += 1
        unique_tokens.add(token)
        
    # lexical diversity = number of unique tokens / total number of tokens
    diversity = total_unique_tokens / len(all_tokens)

    # print the result, formatted to two decimal places
    print()
    print("Lexical diversity: " + str(round(diversity, 2)))
    print()


def preprocess_raw_text(text):

    '''
      Preprocesses raw text using NLTK. Prints out the first twenty part-of-speech tags assigned to lemmas. Prints the number of tokens and the number of nouns, and returns these two lists.
      Args:
        text: string of raw text to be processed 
      Returns:
        tokens: list of tokens (strings) that are lowercase, alphabetic, have length > 5, and are not stopwords
        nouns: list of lemmas that were tagged as nouns by NLTK
      Example:
        >>> preprocess_raw_text('The children happily went to the stadium.')
        >>>
        >>> First twenty part-of-speech tags:
        >>> ('happily', 'RB')
        >>> ('stadium', 'NN')
        >>> ('child', 'NN')
        >>>
        >>> Number of tokens: 3
        >>> Number of nouns: 2
        >>>
        >>> (['children', 'happily', 'stadium'], ['stadium', 'child'])
    '''

    # convert the raw text to lowercase
    text = text.lower()

    # use NLTK to tokenize the lower-case raw text
    all_tokens = word_tokenize(text)

    reduced_tokens = []
    stop_words = set(stopwords.words('english'))

    # iterate through all of the tokens
    for token in all_tokens:

        # reduce the tokens to only those that:
        #   1) are alphabetic characters
        #   2) are not in the NLTK english stopword list
        #   3) have a length greater than 5
        if token.isalpha() and token not in stop_words and len(token) > 5:
            reduced_tokens.append(token)
    
    # use NLTK to lemmatize the reduced tokens
    wnl = WordNetLemmatizer()
    lemmatized = [wnl.lemmatize(t) for t in reduced_tokens]

    # use set() to make a list of unique lemmas
    unique_lemmas = set(lemmatized)

    # use NLTK to do part-of-speech tagging on the unique lemmas
    pos_tags = pos_tag(unique_lemmas)

    
    num_printed = 0

    # create a list of only those lemmas that are nouns
    nouns = []

    print()
    print("First twenty part-of-speech tags:")

    # iterate through all of the POS tags
    for tagged_lemma in pos_tags:

        # only print the first 20 tagged tokens
        if num_printed < 20:
            print(tagged_lemma)
            num_printed += 1
        
        # if the current lemma's tag starts with N, add it to the list of nouns
        if tagged_lemma[1][0] == 'N':
            nouns.append(tagged_lemma[0])

    # return the list of reduced tokens and the list of nouns after printing their values
    print()
    print("Number of tokens: " + str(len(reduced_tokens)))
    print("Number of nouns: " + str(len(nouns)))
    print()
    
    return (reduced_tokens, nouns)


def create_noun_count_dictionary(nouns, tokens):
    '''
      Finds and prints the fifty most common nouns based on how many times they appear in the list of tokens
      Args:
        nouns: list of strings representing the nouns in the processed text
        tokens: list of strings representing all of the tokens in the processed text
      Returns: 
        sorted list of strings representing the fifty most common nouns in the text
      Example:
        >>> create_noun_count_dictionary(['house', 'road'], ['road', 'green', 'house', 'road'])
        >>> Most Common Nouns:
        >>> 1. road - 2
        >>> 2. house - 1
        >>> ['road', 'house']
    '''

    noun_dict = {}
    for noun in nouns:
        count = tokens.count(noun)
        noun_dict[noun] = count
    
    # sort the dictionary by count
    sorted_nouns = sorted(noun_dict, key=lambda x: noun_dict[x], reverse=True)

    # print the fifty most common words and their counts
    print()
    print("Most Common Nouns:")
    top_50 = []
    for x in range(min(50, len(sorted_nouns))):
        print(str(x+1) + '. ' + sorted_nouns[x] + ' - ' + str(noun_dict[sorted_nouns[x]]))

        # save the top fifty words to a list
        top_50.append(sorted_nouns[x])
    return top_50


def guessing_game(possible_words):
    '''
      Choose a random word from the given list, and allow the user to attempt to guess all of the letters in it. Continue this game until the user has a negative score or enters '!'
      Args:
        possible_words: list of strings that can be used in the guessing game
      Returns: None
      Example:
        >>> guessing_game(['apple'])
        >>> Let's play a word guessing game!
        >>> _ _ _ _ _
        >>> Guess a letter: a
        >>> Right! Score is 6
        >>> a _ _ _ _
        >>> Guess a letter: z
        >>> Sorry, guess again. Score is 5
        >>> Guess a letter: !
        >>> You have chosen to exit the game.
        >>> Final score: 5
    '''

    print()
    print("Let's play a word guessing game!")

    # give the user five points to start with
    points = 5

    while True:

        new_int = randint(0,len(possible_words)-1)

        # randomly choose one of the fifty words from the top 50 list
        word = possible_words[new_int]

        print("NEW")
        print(new_int)
        print(word)
        print(possible_words)

        # initially, none of the letters in the word have been guessed correctly
        correctly_guessed = list(False for _ in range(len(word)))

        # use a set to track which letters have already been guessed
        already_guessed = set()
        
        # the user can continue making guesses for the current word until:
        #  1) they have a negative score or 
        #  2) they successfully guess all of the letters
        while points >= 0 and False in correctly_guessed:
            
            letters_to_print = ''
            for x in range(len(correctly_guessed)):

                # output to console an "underscore space" for each letter of the word that has not been guessed yet
                if not correctly_guessed[x]:
                    letters_to_print += '_ '
                # otherwise, output the letter that the user has already solved
                else:
                    letters_to_print += word[x] + ' '

            print(letters_to_print)

            # allow the user to make their next guess
            guessed_letter = input("Guess a letter: ")

            # the game ends if the user guesses '!' as a letter
            if guessed_letter == '!':
                print("You have chosen to exit the game.")
                print("Final score: " + str(points))
                return

            # validate the user input is a single alphabetic character
            elif len(guessed_letter) != 1 or not guessed_letter.isalpha():
                points -= 1
                print("Sorry, guess again. Your input was not a valid letter. Score is " + str(points))

            # if the user has successfully guessed a new letter, give them a point
            elif guessed_letter not in already_guessed and guessed_letter in word:
                points += 1
                print("Right! Score is " + str(points))

                # fill in all of the characters that match the guessed letter
                for x in range(len(word)):
                    if word[x] == guessed_letter:
                        correctly_guessed[x] = True

                # do not allow the user to get points for re-guessing the same letter in the future
                already_guessed.add(guessed_letter)

            # if the letter is not in the word, subtract 1 from their score
            else:
                points -= 1
                print("Sorry, guess again. Score is " + str(points))
                
        # end the game when the total score is negative
        if points < 0:
            print("Sorry, you have less than zero points. Game over.")
            print("Final score: " + str(points))
            return
        
        # otherwise, continue the game with a new word after completing this current word
        else: 
            print("You solved it!")


if __name__ == '__main__':
    '''
      This program calculates the lexical diversity of a text, pre-processes the text, then uses the most common fifty nouns from the text in an interactive word guessing game.
      Args: 
        One system argument with a relative path to a text file
      Returns: None
    '''
    
    # if the user does not specify a sysarg, print an error message and end the program
    if len(sys.argv) < 2:
        print('Error: Please specify a relative path to your input file as a system arg')
    else:
        # try opening the file with the given filename
        try:
            text = open(sys.argv[1], "r").read()

        # exit the program if the input file does not exist
        except IOError:
            print('Error: The specified relative file path is not valid')
            exit(1)
            
        # process the given text
        calculate_lexical_diversity(text)
        tokens, nouns = preprocess_raw_text(text)
        top_50_nouns = create_noun_count_dictionary(nouns, tokens)

        # use the top 50 nouns from the processed text in a word guessing game
        guessing_game(top_50_nouns)