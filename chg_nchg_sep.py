# -*- coding: utf-8 -*-
# python chg_nchg_sep.py AllvsMW/AllvsMW_sf_corrected.txt AllvsMW/chg.txt AllvsMW/nchg.txt
import codecs, re, sys
if __name__=="__main__":
	filein = sys.argv[1]
	filechange = sys.argv[2]
	filenochange = sys.argv[3]
	fin = codecs.open(filein,'r','utf-8')
	fchg = codecs.open(filechange,'w','utf-8')
	fnchg = codecs.open(filenochange,'w','utf-8')
	for line in fin:
		if line.endswith(':n\n') or line.endswith(':n\r\n'):
			splt = line.split(':')
			wrd = splt[1]
			fnchg.write(wrd+'\n')
		else:
			fchg.write(line)
	fin.close()
	fchg.close()
	fnchg.close()
	