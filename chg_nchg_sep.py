# -*- coding: utf-8 -*-
# python chg_nchg_sep.py AllvsMW/AllvsMW_sf_corrected.txt AllvsMW/chg.txt AllvsMW/nchg.txt
import re, sys
if __name__=="__main__":
	filein = sys.argv[1]
	filechange = sys.argv[2]
	filenochange = sys.argv[3]
	fin = open(filein, 'r', encoding='utf-8')
	fchg = open(filechange, 'w', encoding='utf-8')
	fnchg = open(filenochange, 'w', encoding='utf-8')
	for line in fin:
		splt = line.split(':')
		if line.endswith(':n\n') or line.endswith(':n\r\n'):
			if not splt[1] == splt[2]:
				print(splt)
				print('item different, but marked with no change')
				exit(0)
			if not splt[0] in ['ACC','BHS','BUR','IEG','KRM','VEI','PD']:
				wrd = splt[1]
				fnchg.write(wrd+'\n')
		else:
			if splt[1] == splt[2]:
				print(splt)
				print('item same, but marked with change')
				exit(0)
			fchg.write(line)
	fin.close()
	fchg.close()
	fnchg.close()
	