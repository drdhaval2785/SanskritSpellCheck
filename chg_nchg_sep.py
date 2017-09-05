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
		splt = line.split(':')
		if line.endswith(':n\n') or line.endswith(':n\r\n'):
			if not splt[1] == splt[2]:
				print splt
				print 'item different, but marked with no change'
				exit(0)
			if not splt[0] in ['ACC','BHS','BUR','IEG','KRM','PD']:
				wrd = splt[1]
				fnchg.write(wrd+'\n')
		else:
			if splt[1] == splt[2]:
				print splt
				print 'item same, but marked with change'
				exit(0)
			fchg.write(line)
	fin.close()
	fchg.close()
	fnchg.close()
	