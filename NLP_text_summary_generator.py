import requests
import nltk
import os
import urllib
from bs4 import BeautifulSoup
import re
import urllib.request
import bs4 as bs
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import heapq

stopwords = nltk.corpus.stopwords.words('english')

url_list = ['https://www.nytimes.com/2020/07/24/sports/football/nfl-players-regular-season-start.html',
            'https://www.nytimes.com/article/which-stores-require-masks.html',
           'https://www.nytimes.com/2020/07/25/world/asia/us-china-trump-xi.html',
           'https://en.wikipedia.org/wiki/Artificial_intelligence',
           'https://jasminemharrison.com/blog/how-to-define-your-personal-style',
           'https://www.nytimes.com/2020/07/26/us/protests-portland-seattle-trump.html?action=click&module=Top%20Stories&pgtype=Homepage']

keywords = ['season','teams','computer','thrift','style','protests']

article_objects = []

class Articles:

    def __init__(self, name, raw_text_string, cleaned_text_string, formatted_cleaned_text_string, tokenized_word_list, tokenized_sentence_list, word_freq_dict, sentence_score_dict, found_keywords, summary):
        self.name = name
        self.raw_text_string = raw_text_string
        self.cleaned_text_string = cleaned_text_string
        self.formatted_cleaned_text_string = formatted_cleaned_text_string
        self.tokenized_word_list = tokenized_word_list
        self.tokenized_sentence_list = tokenized_sentence_list
        self.word_freq_dict = word_freq_dict
        self.sentence_score_dict = sentence_score_dict
        self.found_keywords = found_keywords
        self.summary = summary

    def web_scrape(self):
        scraped_data = urllib.request.urlopen(self.name)
        article = scraped_data.read()
        parsed_article = bs.BeautifulSoup(article,'lxml')
        paragraphs = parsed_article.find_all('p')
        text_string = ""
        for i in paragraphs:
            text_string += i.text
        self.raw_text_string = text_string

    def clean_text_string(self):
        # Removing Square Brackets and Extra Spaces
        cleaned_text_string = re.sub(r'\[[0-9]*\]', ' ', self.raw_text_string)
        cleaned_text_string = re.sub(r'\s+', ' ', self.raw_text_string)
        self.cleaned_text_string = cleaned_text_string

    def format_cleaned_text_string(self):
        # Removing special characters and digits
        formatted_text_string = re.sub('[^a-zA-Z]', ' ', self.raw_text_string)
        formatted_text_string = re.sub(r'\s+', ' ', self.raw_text_string)
        self.formatted_cleaned_text_string = formatted_text_string

    def tokenize_words(self):
        tokenized_word_list = word_tokenize(self.formatted_cleaned_text_string)
        self.tokenized_word_list = tokenized_word_list

    def tokenize_sentences(self):
        tokenized_sentence_list = sent_tokenize(self.cleaned_text_string)
        self.tokenized_sentence_list = tokenized_sentence_list

    def word_freq(self):
        for word in self.tokenized_word_list:
            if word not in stopwords:
                if word not in self.word_freq_dict.keys():
                    self.word_freq_dict[word] = 1
                else:
                    self.word_freq_dict[word] += 1
        maximum_frequency = max(self.word_freq_dict.values())
        for word in self.word_freq_dict.keys():
            self.word_freq_dict[word] = (self.word_freq_dict[word]/maximum_frequency)

    def sentence_score(self): #come back to this, may need to add a second parameter?
        for sent in self.tokenized_sentence_list:
            for word in nltk.word_tokenize(sent.lower()):
                if word in self.word_freq_dict.keys():
                    if len(sent.split(' ')) < 30:
                        if sent not in self.sentence_score_dict.keys():
                            self.sentence_score_dict[sent] = self.word_freq_dict[word]
                        else:
                            self.sentence_score_dict[sent] += self.word_freq_dict[word]

    def generate_summary(self):
        summary = heapq.nlargest(7, self.sentence_score_dict, key=self.sentence_score_dict.get)
        self.summary = ' '.join(summary)

    def heapsort_tokenized_word_list(self):
        self.tokenized_word_list = [i.lower() for i in self.tokenized_word_list]
        heapq.heapify(self.tokenized_word_list)
        self.tokenized_word_list = [heapq.heappop(self.tokenized_word_list) for i in range(len(self.tokenized_word_list))]
     
    #non recursive binary search
    def search(self, tokenized_word_list, keyword):
        low = 0
        high = len(tokenized_word_list) - 1
        while low <= high:
            middle = int((low + high)/ 2)
            mid = tokenized_word_list[middle]
            #keyword found
            if mid == keyword:
                return True
            elif mid > keyword:
                high = middle - 1
            elif mid < keyword:
                low = middle + 1
                    
    def populate_found_keywords(self):
        for i in keywords:
            word_in_list = self.search(self.tokenized_word_list, i)
            if word_in_list == True:
                self.found_keywords.append(i)
            else:
                continue

'''
    def populate_found_keywords(self):
        for i in keywords:
            try:
                keyword = self.search(self.tokenized_word_list, i, 0, len(self.tokenized_word_list)-1)
                if keyword != -1:
                    self.found_keywords.append(i)
            except RecursionError:
                continue
'''

'''
    def search(self, tokenized_word_list, keyword, low, high):
        mid = int((low + high)/2)
        #keyword found
        if tokenized_word_list[mid] == keyword:
            return keyword
        #value at mid index higher than target
        elif tokenized_word_list[mid] > keyword:
            self.search(self.tokenized_word_list, keyword, low, mid-1)
        #value at mid index lower than target
        elif tokenized_word_list[mid] < keyword:
            self.search(self.tokenized_word_list, keyword, mid+1, high)
        #low and high have crossed: keyword not present
        elif low>high:
            return -1
'''

#create an object for each article in the url_list and add it to article_objects list
for i in url_list:
    i = Articles(i, "", "", "", None, None, {}, {}, [], "")
    article_objects.append(i)
    
for i in article_objects:
    i.web_scrape()
    i.clean_text_string()
    i.format_cleaned_text_string()
    i.tokenize_words()
    i.heapsort_tokenized_word_list()
    i.populate_found_keywords()

    if len(i.found_keywords)>0:
        i.tokenize_sentences()
        i.word_freq()
        i.sentence_score()
        i.generate_summary()
        print(i.name)
        print(str(i.found_keywords)[1:-1])
        print('\n')
        print(i.summary)
        print('\n')
