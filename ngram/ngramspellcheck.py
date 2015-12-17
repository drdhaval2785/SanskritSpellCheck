# -*- coding: utf-8 -*-
"""
To compare n-grams of a given text against the possible ngrams extracted and put in 'data' folder as 2grams.txt and 3grams.txt

Usage:
python ngramspellcheck.py inputfile filetostoreerrors n
e.g.
python ngramspellcheck.py data/test.txt data/error.txt 2

It is advisable to try for bigrams only (n=2) to minimize false positives.
It can be extended to trigrams and higher ngrams, but it would increase false positives too much.

would create 3-grams which are found in all of the following dictionaries.

Dictionaries
MW PW PWG PD MW72 VCP SHS YAT WIL SKD CAE AP ACC AP90 CCS SCH STC MD BUR BHS BEN
"""
import sys, re
import codecs
import string
import datetime
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

# Function to return timestamp
def timestamp():
	return datetime.datetime.now()

def triming(lst):
	output = []
	for member in lst:
		member = member.strip()
		output.append(member)
	return output


def getbasewords(basedict):
	global sanhw2
	headwithdicts = sanhw2
	basewords = []
	otherwords = []
	for (word,dicts,lnums) in headwithdicts:
		if basedict in dicts:
			basewords.append(word)
		else:
			otherwords.append((word,dicts,lnums))
	return [basewords,otherwords]

def ngrams(input, n):
	output = []
	if n >= len(input): # Removing whole word entries.
		pass
	else:
		for i in range(len(input)-n+1):
			output.append(input[i:i+n])
	return output

def getngrams(words,nth):
	ngr = []
	for word in words:
		ngr += ngrams(word,nth)
	ngr = list(set(ngr))
	return ngr
def commons(lstoflist,n):
	commons = []
	filestore = codecs.open('commonngram/'+str(n)+'grams.txt','w','utf-8')
	for member in lstoflist[-1]:
		if all(member in lst for lst in lstoflist):
			commons.append(member)
			filestore.write(member+"\n")
	print "Common ngrams are", len(commons)
	filestore.close()
	return commons
def stripper(text):
	striplist = codecs.open('data/stripgretil.txt','r','utf-8').read().split()
	striplist = triming(striplist)
	for stripp in striplist:
		text = re.sub(stripp,'',text)
	text = strip_tags(text)
	return text

def commonngram(n):	
	#majordicts = ["MW","PW","PWG","PD","MW72","VCP","SHS","YAT","WIL","SKD","CAE","AP","ACC","AP90","CCS","SCH","STC","MD","BUR","BHS","BEN"]
	majordicts = ["MW","PW"]
	ngrams = []
	for dict in majordicts:
		print dict
		[basewords,otherwords] = getbasewords(dict)
		ngram = getngrams(basewords,n)
		print len(ngram)
		ngrams.append(ngram)
	commonngrams = commons(ngrams,n)
def whiteterm(ends,word,diff,basengrams,n):
	for end in ends:
		[pre,post] = end.split(':')
		word1 = ''
		if word.endswith(pre):
			word1 = word.rstrip(pre)+post
		if diff<=set(pre) and set(ngrams(word,n)) < set(basengrams):
			return True
			break
		elif  not word1 == '' and set(ngrams(word1,n)) < set(basengrams):
			return True
			break
				
def testwithcommonngrams(test,error,n):
	basefile = codecs.open('data/'+str(n)+'grams.txt','r','utf-8')
	basengrams = basefile.read().split()
	basengrams = triming(basengrams)
	basefile.close()
	whitelistfile = codecs.open('data/whitelist.txt','r','utf-8')
	whitelist = whitelistfile.readlines()
	whitelist = triming(whitelist)
	whitelist = set(whitelist)
	whiteendsfile = codecs.open('data/whiteends.txt','r','utf-8')
	whiteends = whiteendsfile.readlines()
	whiteends = triming(whiteends)
	whiteends = list(set(whiteends))
	whiteendsfile.close()
	testfile = codecs.open(test,'r','utf-8')
	lines = testfile.read().split()
	lines = triming(lines)
	errorfile = codecs.open(error,'w','utf-8')
	counter = 0
	for line in lines:
		line = stripper(line)
		line = line.replace('-',' ')
		testwords = line.split(' ')
		for testword in testwords:
			testword = testword.replace(u'’',u'')
			testword = re.sub('[\'",.?0-9!/*_\(\)\[\]\{\}<>;:*’#$+%^@–=“”|]','',testword)
			testngrams = ngrams(testword,n)
			diff = set(testngrams)-set(basengrams)
			if not diff <= whitelist and not whiteterm(whiteends,testword,diff,basengrams,n):
				diff = list(diff)
				if len(diff) is not 0:
					print testword.encode('utf-8'), diff
					errorfile.write(testword+':'+','.join(diff)+'\n')
					counter += 1
	errorfile.close()
	print "Total potential errors by ngram method are", counter
	
if __name__=="__main__":
	fin = sys.argv[1]
	fout = sys.argv[2]
	n = sys.argv[3]
	#commonngram(int(n)) # to generate the common ngrams (data/2grams.txt and data/3grams.txt)
	testwithcommonngrams(fin,fout,int(n))
	