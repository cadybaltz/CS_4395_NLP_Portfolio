"""
CS 4395.001 Human Language Technologies
Portfolio: Finding or Building a Corpus
Cady Baltz (cmb180010)
3/13/2023
"""

import pickle
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import requests
import os
import re
import mysql.connector
from collections import deque

# Hardcode constant variables in this program

RAW_TEXT_DIR = 'raw_page_texts'
CLEANED_TEXT_DIR = 'cleaned_page_texts'

PICKLE_FILE_NAME = 'chatbot_kb.p'

SQL_DB_NAME = 'chatbot_kb'
SQL_HOST = 'localhost'
SQL_USER = 'root'
SQL_PASSWORD = 'root'
def web_crawler(starter_url):
    """
          Given a starter URL, uses Beautiful Soup to parse the website for other links
          After reviewing the content of these links, it returns 15 links that have content relevant to the initial URL
          Args:
              starter_url: String containing the URL of a website
          Returns:
              related_links: Array of 15 URL strings that contain at least 500 words of content
    """
    related_links = []
    related_hostnames = set()
    link_queue = deque([starter_url])

    # hardcode website domains that resulted in issues with scraping text to avoid them
    blocked_hosts = [
        'creativecommons.org',
        'wikimedia.org',
        'foundation.wikimedia.org',
        'donation.wikimedia.org',
        'support.apple.com',
        'mlhw.go.jp',
        'tabelog.com',
        'ana.co.jp'
    ]

    # search through a maximum of 1000 links before abandoning the search
    num_iter = 0

    # continue searching until you find 15 relevant links
    while len(related_links) < 15 and num_iter < 1000:

        # pop the next link to check off the queue
        current_url = link_queue.popleft()

        # get the link's hostname
        current_hostname = urlparse(current_url).hostname

        # try and access the current URL, but skip it if you cannot
        try:
            r = requests.get(current_url, timeout=1)
        except:
            continue

        # use Beautiful Soup to scrape text from the website
        data = r.text
        soup = BeautifulSoup(data, features="html.parser")
        raw_page_text = get_paragraph_text(soup)

        # split the text to count how many words this page has
        words = raw_page_text.split()
        num_words_on_page = len(words)

        # check if the link is "relevant"
        # I defined a relevant link as one that:
        #   1) has at least 500 words
        #   2) is written with ASCII characters
        #   3) a link from the same host is not already being used
        #   4) a link not from any of the manually-defined blocked hosts
        if num_words_on_page > 500 \
                and len(words[0]) == len(words[0].encode()) \
                and current_hostname not in related_hostnames \
                and current_hostname not in blocked_hosts:

            related_links.append(current_url)
            print('Adding new link: ' + current_url)

            # dump the raw text to a new file
            create_raw_text_file(raw_page_text, len(related_links))

        # add all links from the current link to the queue to continue searching as needed later
        all_links = set(soup.find_all('a'))
        for link in all_links:
            link_href = link.get('href')
            link_queue.append(link_href)

        # save the current hostname so you do not use it again
        related_hostnames.add(current_hostname)
        num_iter += 1

    return related_links


def get_paragraph_text(soup):
    """
          Returns all of the text in <p> tags in HTML in a single Python string
          Args:
              soup: a Beautiful Soup object
          Returns:
              paragraph_text: a string containing all of the raw paragraph text
    """

    paragraph_text = ''

    # iterate through all of the paragraphs in this Beautiful Soup object to put them in one string
    for paragraph in soup.find_all("p"):
        paragraph_text += paragraph.get_text()

        # add a space between paragraphs
        paragraph_text += ' '

    # return all of the paragraphs as a single raw string
    return paragraph_text


def create_raw_text_file(raw_text, link_number):
    """
          Creates a new text file consisting of raw paragraph text
          Args:
              raw_text: the string of text you want in the file
              link_number: the number that should be in the filename (format: link-1.txt)
          Returns: None
    """
    link_file = open(RAW_TEXT_DIR + "/link-" + str(link_number + 1) + ".txt", "w", encoding="utf8")
    link_file.write(raw_text)


def clean_text():
    """
          Iterates through all of the files in the raw text directory, cleans the files,
          and outputs new files to the cleaned text directory
          Args: None
          Returns: None
    """
    os.makedirs(CLEANED_TEXT_DIR, exist_ok=True)

    # iterate through all of the files containing raw text
    for filename in os.listdir(RAW_TEXT_DIR):
        f = os.path.join(RAW_TEXT_DIR, filename)

        if os.path.isfile(f):
            file = open(f, "r", encoding="utf8")

            # read in the text and remove new lines/tabs
            text = file.read()
            text = re.sub('\n', '', text)
            text = re.sub('\t', '', text)

            # use NLTK to tokenize the text by sentences
            sentences = sent_tokenize(text)

            # create a new file for the text in the cleaned text directory
            cleaned_file = open(CLEANED_TEXT_DIR + '/' + os.path.basename(f), "w", encoding="utf8")

            # output each tokenized sentence to the new file with a new line in between
            for sentence in sentences:
                cleaned_file.write(sentence + '\n')


def get_top_25_terms():
    """
          Returns a list of the 25 most frequent terms from the cleaned text files
          Args: None
          Returns:
              top_25: an array of strings representing the 25 most frequent terms
    """

    # create a dict to calculate the frequency of each token
    term_counts = {}

    # iterate through all of the files in the cleaned text directory
    for filename in os.listdir(CLEANED_TEXT_DIR):
        f = os.path.join(CLEANED_TEXT_DIR, filename)

        if os.path.isfile(f):
            file = open(f, "r", encoding="utf8")

            sentences = file.readlines()
            for sentence in sentences:
                # first, lowercase the current sentence
                processed_text = sentence.lower()

                # use NLTK to tokenize the text into individual words
                tokens = word_tokenize(processed_text)

                # use NLTK to get a list of English stopwords
                stop_words = set(stopwords.words('english'))

                # iterate through all of the tokens
                for token in tokens:

                    # reduce the tokens to only those that:
                    #   1) are alphabetic characters
                    #   2) are not in the NLTK english stopword list
                    #   3) have a length greater than 5
                    if token.isalpha() and token not in stop_words and len(token) > 5:
                        if token in term_counts:
                            term_counts[token] += 1
                        else:
                            term_counts[token] = 1

    # sort the term dictionary from highest to lowest counts
    sorted_terms = sorted(term_counts.items(), key=lambda item: item[1], reverse=True)

    # return the first 25 terms in the sorted result
    top_25 = []
    x = 0
    while x < 25 and x < len(sorted_terms):
        top_25.append(sorted_terms[x][0])
        x += 1
    return top_25

def create_knowledge_base_dict(top_10_terms):
    """
          Returns all of the text in <p> tags in HTML in a single Python string
          Args:
              top_10_terms: an array of 10 strings
          Returns:
              kb: a dictionary mapping of each the 10 terms to the tokenized sentences it is present in
    """

    # create a dictionary that will map each term to a list of relevant sentences
    kb = {}
    for term in top_10_terms:
        kb[term] = []

    # iterate through each file in the clean text directory
    for filename in os.listdir(CLEANED_TEXT_DIR):
        f = os.path.join(CLEANED_TEXT_DIR, filename)

        if os.path.isfile(f):
            file = open(f, "r", encoding="utf8")
            sentences = file.readlines()

            # iterate through each file sentence by sentence
            for sentence in sentences:

                # if one (or more) of the 10 terms is in the sentence, add the sentence to this term's dict entry
                for term in top_10_terms:
                    if term in sentence:
                        kb[term].append(sentence.strip())
    return kb


def execute_sql(db, query):
    """
          Given an existing SQL connection, run a query and check whether it was successful
          Args:
              db: an SQL database connection
          Returns:
              bool: boolean indicating whether the query was successful or if it failed
    """
    cursor = db.cursor()

    # try to execute the SQL command
    try:
        cursor.execute(query)

        # use commit to verify whether the command was successful
        db.commit()

        # return True/False to indicate whether the command was successful
        return True
    except:
        return False


def create_or_update_sql_db(kb_dict):
    """
          Creates a new MySQL database with two tables:
          term contains the 10 terms I am using to build my knowledge base
          sentence contains all of the knowledge that pertains to these terms

          Args:
              kb_dict: a dictionary mapping of each the 10 terms to the tokenized sentences it is present in
          Returns:
              bool: a boolean indicating whether the SQL database creation was successful
    """
    try:
        # first, connect to local SQL database (see variable values for username/password/host)
        sql = mysql.connector.connect(
            host=SQL_HOST,
            user=SQL_USER,
            password=SQL_PASSWORD
        )

        cursor = sql.cursor()

        # check if the database already exists
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()

        # if not, create a new database
        if ('chatbot_kb',) not in databases:
            print('Creating new SQL database ' + SQL_DB_NAME)
            cursor.execute('CREATE DATABASE ' + SQL_DB_NAME)

        # connect to the database
        db = mysql.connector.connect(
            host=SQL_HOST,
            user=SQL_USER,
            password=SQL_PASSWORD,
            database=SQL_DB_NAME
        )

        # access the tables stored in this database
        cursor = db.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
    except:
        print("SQL Error: Could not connect to SQL db " + SQL_DB_NAME)
        return False

    # if the tables already exist, drop them so we can update all of the values to the most recent information
    if ('sentence',) in tables:
        if not execute_sql(db, "DROP TABLE sentence"):
            print("SQL Error: Could not drop sentences table")
            return False
    if ('term',) in tables:
        if not execute_sql(db, "DROP TABLE term"):
            print("SQL Error: Could not drop term table")
            return False

    # SQL command to create the table storing the 10 terms I selected
    create_term_table = """
    CREATE TABLE term (
        term_id INT PRIMARY KEY,
        term VARCHAR(40) NOT NULL
    );
    """

    # SQL command to create the table that will store the sentences mapped to each term
    create_sentence_table = """
    CREATE TABLE sentence (
        sentence_id INT PRIMARY KEY,
        sentence VARCHAR(1000) NOT NULL,
        term INT
    );
    """

    # add a foreign key so the sentence table can map to each term in the 'term' table
    alter_sentence_table = """
    ALTER TABLE sentence
    ADD FOREIGN KEY(term)
    REFERENCES term(term_id)
    ON DELETE SET NULL;
    """

    # execute all of the SQL commands with error handling
    if not execute_sql(db, create_term_table):
        print("SQL Error: Could not create terms table")
    if not execute_sql(db, create_sentence_table):
        print("SQL Error: Could not create sentence table")
    if not execute_sql(db, alter_sentence_table):
        print("SQL Error: Could not alter sentence table")

    # the keys of the knowledge base will be entered into the 'term' table
    terms = list(kb_dict.keys())

    # create a SQL command to populate the term table with all 10 entries
    populate_terms = "INSERT INTO term VALUES\n"
    for x in range(len(terms)):

        # each entry includes a unique ID (assigned sequentially)
        new_entry = '('
        new_entry += str(x + 1) + ", '"

        # each entry includes the term itself
        new_entry += terms[x] + "')"

        if x < len(terms) - 1:
            new_entry += ','
        new_entry += '\n'
        populate_terms += new_entry

    if not execute_sql(db, populate_terms):
        print("SQL Error: Could not populate terms table")

    # create an SQL command to populate the sentences table
    populate_sentences_command = "INSERT INTO sentence VALUES\n"

    # each sentence will also have a unique sequential ID
    sentence_id = 1

    # iterate through all of the sentences based on what term they are mapped to
    for term_id in range(len(terms)):
        sentences = kb_dict[terms[term_id]]
        for sentence in sentences:

            # each sentence entry includes an ID
            new_entry = '('
            new_entry += str(sentence_id) + ", '"

            # each sentence entry includes the sentence itself
            new_entry += sentence + "', "

            # each entry includes a foreign key that maps to the corresponding term entry in the 'term' table
            new_entry += str(term_id + 1) + ")"
            if execute_sql(db, populate_sentences_command + new_entry):
                sentence_id += 1

    # indicate the database was created properly
    return True


if __name__ == '__main__':

    # start the program with my chosen URL
    related_links = web_crawler('https://en.m.wikivoyage.org/wiki/Japan')

    # print the 15 URLs that were returned
    print("Relevant URLs found: ")
    for x in range(len(related_links)):
       print(str(x+1) + '. ' + related_links[x])

    # generate 15 files of cleaned text from these URLs
    clean_text()

    top_25_terms = get_top_25_terms()
    print("Top 25 Most Frequent Terms")
    for x in range(len(top_25_terms)):
        print(str(x+1) + '. ' + top_25_terms[x])

    # after observing the top 25 terms printed previously, I chose 10 to include in my knowledge base
    selected_10_terms = [
        'japanese',
        'country',
        'english',
        'popular',
        'cities',
        'hotels',
        'restaurants',
        'travel',
        'international',
        'stores'
    ]
    print("Selected 10 Terms for Knowledge Base:")
    for x in range(len(selected_10_terms)):
        print(str(x + 1) + '. ' + selected_10_terms[x])

    # use these 10 terms to create a knowledge base
    kb_dict = create_knowledge_base_dict(selected_10_terms)

    # store the resulting dictionary in a pickle file
    pickle.dump(kb_dict, open(PICKLE_FILE_NAME, 'wb'))

    # also store the resulting dictionary in a MySQL database
    if create_or_update_sql_db(kb_dict):
        print("Successfully created SQL database " + SQL_DB_NAME)
    else:
        print("Failed to create SQL database " + SQL_DB_NAME + ". Please use the pickle file " + PICKLE_FILE_NAME + " instead.")
