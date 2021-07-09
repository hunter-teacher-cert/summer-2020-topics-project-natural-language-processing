#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import nltk
import nltk.corpus
import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
from wordcloud import WordCloud
import matplotlib.pyplot as plt


# In[ ]:


alice = nltk.corpus.gutenberg.words('carroll-alice.txt')


# In[ ]:


aliceString = ""
for word in alice:
    aliceString += word
    aliceString += " "


# In[ ]:


def cleanTextR1(text):
    '''Make text lowercase, remove punctuation and remove words containing numbers.'''
    text = text.lower()
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text

round1 = cleanTextR1(aliceString)


# In[ ]:


stopWords = set(stopwords.words('english')) 


# In[ ]:


round1Tokens = word_tokenize(round1)


# In[ ]:


filteredAlice = [w for w in round1Tokens if not w in stopWords]

filteredAlice = []

for w in round1Tokens:
    if w not in stopWords:
        filteredAlice.append(w)


# In[ ]:


wordDictionary = {}

for i in range(len(filteredAlice)):
  if filteredAlice[i] in wordDictionary:
    wordDictionary[filteredAlice[i]] += 1
  else:
    wordDictionary[filteredAlice[i]] = 1


# In[ ]:


wc = WordCloud(background_color="white", colormap="Dark2",
               max_font_size=150, random_state=42).generate_from_frequencies(wordDictionary)


# In[ ]:


import matplotlib.pyplot as plt

plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.show()

