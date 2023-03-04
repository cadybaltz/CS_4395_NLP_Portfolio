# CS_4395_NLP_Portfolio
This is my portfolio for the course CS 4395: Human Language Technologies (Spring 2023)

### Table of Contents

- [Assignment 0: Getting Started](#assignment-0-getting-started)
- [Assignment 1: Text Processing with Python](#assignment-1-text-processing-with-python)
- [Assignment 2: Word Guess Game](#assignment-2-word-guess-game)
- [Assignment 3: WordNet](#assignment-3-wordnet)
- [Assignment 4: Ngrams](#assignment-4-ngrams)
- [Assignment 5: Sentence Parsing](#assignment-5-sentence-parsing)

-----

### Assignment 0: Getting Started
Click [here](https://github.com/cadybaltz/CS_4395_NLP_Portfolio/blob/main/Assignment_0/Overview_of_NLP.pdf) to read my overview of NLP

-----

### Assignment 1: Text Processing with Python
[This program](https://github.com/cadybaltz/CS_4395_NLP_Portfolio/blob/main/Assignment_1/cmb180010-NLP-Assignment-1.py) parses an employee data file to produce more standardized values. It processes an employee's first name, last name, middle initial, phone number, and ID and makes sure each value follows a specified format (e.g., all phone numbers must be in the format 555-555-5555). To handle this text processing, I used standard Python text processing functions as well as regex. Then, this processed data is saved to a dictionary in a Pickle file. This Pickle file is then read to print out the data for each person.

#### To run:
To run this program, you must include one system argument with a relative path to the input data. In this repository, I have uploaded a sample data file within the 'data' subdirectory. This program must be run with **Python 3**.

`python3 cmb180010-NLP-Assignment-1.py data\data.csv`

#### Strengths/Weaknesses of Python for Text Processing
##### Strengths
- Python has a large number of built-in function for processing text, such as `split()`, which allowed me to easily split the input data based on commas.
- Python also has many libraries that provide additional functionality for processing text, such as `re`, which allowed me to use regex to process the employee's ID and phone number.

##### Weaknesses
- Python does not do type checking. I had to manually do any checks that were necessary for my data, such as ensuring the middle initial was a letter and not a number.
- Python does not distinguish between characters and strings. This would have been useful for fields like this middle initial.

#### What I learned in this assignment
- In this assignment, I reviewed the basics of Python text processing, including how to open and modify files, use built-in functions like `.capitalize()` and `input()`, and store data in a dictionary.
- Additionally, I learned how to work with additional Python libraries that I had less experience with, including `re` to match and modify text with regex, and `pickle` to store a dictionary in another file.

-----

### Assignment 2: Word Guess Game
[This program](https://github.com/cadybaltz/CS_4395_NLP_Portfolio/blob/main/Assignment_2/cmb180010-NLP-Assignment-2.py) uses Python and NLTK features to explore a text file, and then uses the fifty most common nouns from that text file in a word guessing game.

#### To run:
To run this program, you must include one system argument with a relative path to the input text file. In this repository, I have uploaded a sample data file called anat19.txt, which contains one chapter of an anatomy textbook.

`python3 .\cmb180010-NLP-Assignment-2.py .\anat19.txt`


-----

### Assignment 3: WordNet
Read my analysis of WordNet, SentiWordNet, and collocations [here](https://github.com/cadybaltz/CS_4395_NLP_Portfolio/blob/main/Assignment_3/cmb180010-NLP-Assignment-3.pdf).


-----

### Assignment 4: Ngrams

You can read my narrative overview of Ngrams [here](https://github.com/cadybaltz/CS_4395_NLP_Portfolio/blob/main/Assignment_4/cmb180010_ngrams_narrative.pdf).

[Program 1](https://github.com/cadybaltz/CS_4395_NLP_Portfolio/blob/main/Assignment_4/cmb180010_program_1.py) processes three text files in different languages ([English](https://github.com/cadybaltz/CS_4395_NLP_Portfolio/blob/main/Assignment_4/data/LangId.train.English), [French](https://github.com/cadybaltz/CS_4395_NLP_Portfolio/blob/main/Assignment_4/data/LangId.train.French), and [Italian](https://github.com/cadybaltz/CS_4395_NLP_Portfolio/blob/main/Assignment_4/data/LangId.train.Italian)), and outputs dictionaries of their unigram and bigram counts as Pickle files in a directory called `pickle_output`.

[Program 2](https://github.com/cadybaltz/CS_4395_NLP_Portfolio/blob/main/Assignment_4/cmb180010_program_2.py) then takes these dictionaries and uses them to predict the language of each line in a [test file](https://github.com/cadybaltz/CS_4395_NLP_Portfolio/blob/main/Assignment_4/data/LangId.test) using Laplace smoothing. These predictions are written to `predictions.txt`, and the accuracy and lines numbers of incorrect predictions are outputted.

#### To run:
Note that program 1 may take a few minutes to complete, and its output is required to execute program 2.

`python3 .\cmb180010_program_1.py`
`python3 .\cmb180010_program_2.py`

-----

### Assignment 5: Sentence Parsing

You can view my comparison of PSG, dependency, and SRL parsing [here](https://github.com/cadybaltz/CS_4395_NLP_Portfolio/blob/main/Assignment_5/cmb180010_sentence_parsing.pdf).