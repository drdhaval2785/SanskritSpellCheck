#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
from lxml import etree # lxml.de
import re
import codecs
import datetime

# See https://github.com/sanskrit-lexicon/CORRECTIONS/issues/137#issuecomment-155525313 for the need of this code.
def sortlen(inputfile,outputfile):
	fin = codecs.open(inputfile,'r','utf-8')
	fout = codecs.open(outputfile,'w','utf-8')
	lines = fin.readlines(fin)
	outlist = []
	for line in lines:
		line = line.strip()
		firstwordlen = line.split(':')[0]
		outlist.append((line,firstwordlen))
	outlist.sort(key=lambda x: (len(x[1]),x[0]), reverse=True)
	for (a,b) in outlist:
		fout.write(a+"\n")
	fin.close()
	fout.close()
print "Sorting the composite1 to composite3 by length of words"
print "in descending order and stroring in composite1a to composite3a."
sortlen('output3/composite1.txt','output3/composite1a.txt')
sortlen('output3/composite2.txt','output3/composite2a.txt')
sortlen('output3/composite3.txt','output3/composite3a.txt')

	