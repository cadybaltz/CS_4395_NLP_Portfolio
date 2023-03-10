"""
CS 4395.001 Human Language Technologies
Portfolio: Finding or Building a Corpus
Cady Baltz (cmb180010)
3/6/2023
"""

from urllib.parse import urlparse
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import requests
import os
import re
import mysql.connector
from collections import deque

RAW_TEXT_DIR = 'raw_page_texts'
CLEANED_TEXT_DIR = 'cleaned_page_texts'

def get_url_page_text(url):
    try:
        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, features="html.parser")
        return soup.text
    except:
        print("Error getting page text for the URL: " + str(url))
        return None

def web_crawler(starter_url):
    related_links = []
    related_hostnames = set()
    links_in_same_domain = []
    link_queue = deque([starter_url])

    blocked_hosts = ['creativecommons.org', 'wikimedia.org', 'foundation.wikimedia.org', 'donation.wikimedia.org', 'support.apple.com', 'mlhw.go.jp', 'tabelog.com', 'ana.co.jp']

    iter = 0

    while len(related_links) < 15 and iter < 1000:
        current_url = link_queue.popleft()
        current_hostname = urlparse(current_url).hostname

        if current_url is not None and current_url.startswith('http'):
            try:
                # r = requests.get(current_url, timeout=1)
                # data = r.text
                # soup = BeautifulSoup(data, features="html.parser")
                # page_text = soup.text
                raw_page_text = get_paragraph_text(current_url)

                if raw_page_text is not None:
                    words = raw_page_text.split()
                    num_words_on_page = len(words)

                    if num_words_on_page > 500 and len(words[0]) == len(words[0].encode()):
                        if current_hostname not in related_hostnames and current_hostname not in blocked_hosts:
                            related_links.append(current_url)
                            print('Adding new link: ' + current_url)
                            print("BACK: " + str(len(related_links)))
                            create_raw_text_file(raw_page_text, len(related_links))
                            link_queue.append(current_url)

                            r = requests.get(current_url, timeout=1)
                            data = r.text
                            soup = BeautifulSoup(data, features="html.parser")
                            all_links = set(soup.find_all('a'))
                            for link in all_links:
                                link_href = link.get('href')
                                if link_href is not None and link_href.startswith('http'):
                                    link_queue.append(link_href)
                            related_hostnames.add(urlparse(current_url).hostname)

                        elif current_url not in links_in_same_domain and current_url not in related_links:
                            links_in_same_domain.append(current_url)

                        related_hostnames.add(current_hostname)
            except:
                print("Could not reach the link: " + current_url)
            print(related_links)
        iter += 1

    if len(related_links) < 15:
        x = 0
        while len(related_links) < 15 and x < len(links_in_same_domain):
            related_links.append(links_in_same_domain[x])
            print('Adding new link: ' + current_url)
            print("HERE: " + str(len(related_links)))
            create_raw_text_file(raw_page_text, len(related_links))
            link_queue.append(current_url)
            x += 1

    return related_links

def get_paragraph_text(url):
    try:
        r = requests.get(url, timeout=1)
        data = r.text
        soup = BeautifulSoup(data, features="html.parser")
        paragraph_text = ''
        for paragraph in soup.find_all("p"):
            paragraph_text += paragraph.get_text()
            paragraph_text += ' '
        return paragraph_text
    except:
        print("Could not reach the link: " + url)
        return None

def create_raw_text_file(raw_text, link_number):
    link_file = open(RAW_TEXT_DIR + "/link-" + str(link_number + 1) + ".txt", "w", encoding="utf8")
    link_file.write(raw_text)

# def scrape_text(url_list):
#     dir_name = 'raw_page_texts'
#
#     os.makedirs(dir_name, exist_ok=True)
#
#     for x in range(len(url_list)):
#         r = requests.get(url_list[x], timeout=1)
#         data = r.text
#         soup = BeautifulSoup(data, features="html.parser")
#         paragraph_text = ''
#         for paragraph in soup.find_all("p"):
#             paragraph_text += paragraph.get_text()
#             paragraph_text += ' '
#
#         link_file = open("raw_page_texts/link-" + str(x + 1) + ".txt", "w", encoding="utf8")
#         link_file.write(paragraph_text)
#
#     return dir_name


def clean_text(old_dir):
    new_dir = 'cleaned_page_texts'
    os.makedirs(new_dir, exist_ok=True)

    for filename in os.listdir(old_dir):
        f = os.path.join(old_dir, filename)

        if os.path.isfile(f):
            file = open(f, "r", encoding="utf8")

            # read in the text and remove new lines/tabs
            text = file.read()
            text = re.sub('\n', '', text)
            text = re.sub('\t', '', text)

            sentences = sent_tokenize(text)

            cleaned_file = open(new_dir + '/' + os.path.basename(f), "w", encoding="utf8")

            for sentence in sentences:
                cleaned_file.write(sentence + '\n')

    return new_dir


def get_top_25_terms(text_dir):
    term_counts = {}

    for filename in os.listdir(text_dir):
        f = os.path.join(text_dir, filename)

        if os.path.isfile(f):
            file = open(f, "r", encoding="utf8")

            sentences = file.readlines()
            for sentence in sentences:
                processed_text = sentence.lower()

                tokens = word_tokenize(processed_text)
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
    sorted_terms = sorted(term_counts.items(), key=lambda item: item[1], reverse=True)

    top_25 = []
    x = 0
    while x < 25 and x < len(sorted_terms):
        top_25.append(sorted_terms[x][0])
        x += 1
    return top_25


def create_knowledge_base_dict():
    return {}


def create_sql_db():
    db = mysql.connector.connect(
        host="localhost",
        user="NLP",
        password=""
    )

    cursor = db.cursor()

    cursor.execute("CREATE DATABASE chatbot_kb")


if __name__ == '__main__':
    related_links = web_crawler('https://en.m.wikivoyage.org/wiki/Japan')

    print("Relevant URLs found: ")
    for x in range(len(related_links)):
        print(str(x+1) + '. ' + related_links[x])

    # raw_text_dir = scrape_text(related_links)
    # raw_text_dir = 'raw_page_texts'

    clean_dir = clean_text(RAW_TEXT_DIR)

    clean_dir = 'cleaned_page_texts'

    terms = get_top_25_terms(clean_dir)
    print(terms)

    top_10_terms = ['travel', 'japanese', 'foreign', 'photography', 'places', 'adventure', 'business', 'nationals',
                    'experience', 'popular']
