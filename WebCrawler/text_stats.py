#August 2021 - Used with KSU.py
import json
import string
import re
import matplotlib.pyplot as plt
from collections import Counter
from decimal import *
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# header
print('Text Stats from KSU Web Crawler')
print('-------------------------------\n')

# open json file extracted from website
file = open('KSUCrawlerData.json', 'r')
data = json.load(file)

# variables
emails = []
allWords = []
emailCounter = 0
tokenCounter = 0
rank = 0
stops = stopwords.words('english')
punctuation = string.punctuation

# Urls that have one email address and token counter
for i in range(len(data)):
    tokenCounter = tokenCounter + len(data[i]['body'].split())
    if len(data[i]['emails']) != 0:
        emailCounter = emailCounter + 1
        for email in data[i]['emails']:
            emails.append(str(email))

# print average document length after tokenization
docLen = format(tokenCounter/len(data), '.3f') # calculate average length of document based on tokenization
print("doc_len: " + str(docLen))

# print 10 most common emails
print("emails:")
c = Counter(emails)
MostCommonEmails = c.most_common(10)
for email in MostCommonEmails: print('\t' + str(email))

# print percentage of websites with at least one email
percent = format(emailCounter/len(data), '.3f')
print("perc: " + str(percent))

# determine 30 most common words before and after stop words are added with length calculated
for i in range(len(data)):
    allWords.append(str(data[i]['body']).lower())
numberOfWords = len(str(allWords).split())

# print 30 most common words before stop words are added
print("With Stopwords:")
print('\trank\t\tterm\t\tfreq.\t\tperc.')
print('\t----------\t----------\t----------\t----------')
cBefore = Counter(str(allWords).split())
MostCommonBeforeStopWords = cBefore.most_common(30)
for word in MostCommonBeforeStopWords: 
    rank = rank + 1
    if len(word[0]) > 7:
        print('\t' + str(rank) + '\t\t' + str(word[0]) + '\t' + str(word[1]) + '\t\t' + str(format(word[1]/numberOfWords, '.3f')))
    else:
        print('\t' + str(rank) + '\t\t' + str(word[0]) + '\t\t' + str(word[1]) + '\t\t' + str(format(word[1]/numberOfWords, '.3f')))

# determine most common words without stop words
MostCommonAfterStopWords = {}
cAfter = Counter(str(allWords).split())
for word in cAfter.copy():
    if word in stops or word in punctuation or '\n' in word or ',' in word or '.' in word or '\\' in word or word.isnumeric():
        cAfter.pop(word)
MostCommonAfterStopWords = cAfter.most_common(30)

# print 30 most common words after stop words are removed
rank = 0
print("Without Stopwords:")
print('\trank\t\tterm\t\tfreq.\t\tperc.')
print('\t----------\t----------\t----------\t----------')
for word in MostCommonAfterStopWords: 
    rank = rank + 1
    if len(word[0]) > 7:
        print('\t' + str(rank) + '\t\t' + str(word[0]) + '\t' + str(word[1]) + '\t\t' + str(format(word[1]/numberOfWords, '.3f')))
    else:
        print('\t' + str(rank) + '\t\t' + str(word[0]) + '\t\t' + str(word[1]) + '\t\t' + str(format(word[1]/numberOfWords, '.3f')))

# word distribution plot before stop words are removed
plt.plot(sorted(cBefore.values(), reverse=True))
plt.xticks([0, 200, 400, 600, 800, 1000])
plt.yticks([0, 2000, 4000, 6000, 8000, 10000, 12000, 14000, 16000])
plt.xlim([-100, 1000])
plt.ylim([-500, 16000])
plt.title('Word Distribution Before Removing Stopwords')
plt.xlabel('rank')
plt.ylabel('frequency')
plt.show()

# word distribution plot after stop words are removed
plt.plot(sorted(cAfter.values(), reverse=True))
plt.xticks([0, 200, 400, 600, 800, 1000])
plt.yticks([0, 600, 1200, 1800, 2400, 3000])
plt.xlim([-100, 1000])
plt.ylim([-100, 3000])
plt.title('Word Distribution After Removing Stopwords')
plt.xlabel('rank')
plt.ylabel('frequency')
plt.show()

# log-log word distribution plot before stop words are removed
plt.xscale('log')
plt.yscale('log')
plt.title('Word Distribution Before Removing Stopwords - Log-Log')
plt.xlabel('rank')
plt.ylabel('log occurrences')
plt.plot(sorted(cBefore.values(), reverse=True))
plt.show()

# log-log word distribution plot after stop words are removed
plt.xscale('log')
plt.yscale('log')
plt.title('Word Distribution After Removing Stopwords - Log-Log')
plt.xlabel('rank')
plt.ylabel('log occurrences')
plt.plot(sorted(cAfter.values(), reverse=True))
plt.show()

# close json file
file.close()