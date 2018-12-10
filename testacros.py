#!/usr/bin/python

# Project Info:
# =============
#   Written by: fyngyrz - codes with magnetic needle
#   Incep date: November 24th, 2018
#  Last Update: November 29th, 2018 (this code file only)
#  Environment: Webserver cgi, HTML 4.01 strict, Python 2.7
# Source Files: soyacro.py, acrobase.txt (these may be renamed)
#  Tab Spacing: Set to 4 for sane readability of Python source
#     Security: Suitable for benign users only (IOW, me.)
#      Purpose: Creates informative <abbr> tag wraps around
#               all-caps terms in the source text. Written
#               to support use of <abbr> on soylentnews.org
#               Also supports canned aa_macro styles via mfile
#      License: None. Use as you will. PD, free, etc.
# Dependencies: aa_webpage.py by fyngyrz
#               aa_macro.py by fyngyrz
#               standard Python cgi import library
#               standard Python sys import library
#               standard Python os import library
# ----------------------------------------------------------

afile = 'acrobase.txt'

errors = ''

try:
	with open(afile) as fh:
		text = fh.read()
except:
	print 'failed to read ' + afile
	exit()

def tstchars(text):
	for c in text:
		if (c >= 'A' and c <= 'Z'):
			pass
		else:
			if (c >= '0' and c <= '9'):
				pass
			else:
				return False
	return True

di = {}
data = text.split('\n')
ln = 1
rct = 0
exl = 0
defcount = 0
multidefs = 0
for line in data:
	if line != '' and line[0] != '#':
		try:
			key,replacement,expansion = line.split(',',2)
		except:
			errors += 'line %d failed to split into three components\n' % (ln)
		else:
			if replacement != '': rct += 1
			if expansion.find('<') != -1: errors += 'expansion of key '+key+' contains "<"\n'
			if expansion.find('>') != -1: errors += 'expansion of key '+key+' contains ">"\n'
			if replacement.find('<') != -1: errors += 'expansion of key '+key+' contains "<"\n'
			if replacement.find('>') != -1: errors += 'expansion of key '+key+' contains "<"\n'
			if expansion == '': errors += 'expansion of key '+key+' is empty\n'
			if key.find('<') != -1: errors += 'key '+key+' contains "<"\n'
			if key.find('>') != -1: errors += 'key '+key+' contains ">"\n'
			if tstchars(key) == False: errors += 'key '+key+' contains illegal characters\n'
			if key == '':
				errors += 'key is empty at line %d\n' % (ln)
			else:
				if di.get(key,'') != '':
					errors += 'duplicate key %s at line %d\n' % (key,ln)
				di[key] = expansion
			sublist = expansion.split(';')
			dc = len(sublist)
			defcount += dc
			if dc > 1:
				multidefs += 1
			exl += len(expansion)
	ln += 1

if errors != '':
	print errors
else:
	s = afile + ' passed all tests'
	sl = len(s)
	print s
	print '-' * sl
al = len(di)
print '%d terms found' % (len(di))
print '%d definitions' % (defcount)
print '%d terms have multiple definitions' % (multidefs)
print '%d terms have replacements' % (rct)
print 'expansion file size is %d bytes' % (len(text))
print 'average expansion length is %d characters' % (round(float(exl) / float(al)))
