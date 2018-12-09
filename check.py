#!/usr/bin/python

import sys

# Quick way to see if an acronym is in the acrobase.txt file
# ----------------------------------------------------------
# ./check.py MHZ
# ./check.py NAFTA CEO CPU
# ./check.py NOTINHERE 73

errors = u''

argc = len(sys.argv)
if argc < 2:
	print 'Usage: check.py ACRO[,ACRO2]...[ACROn]'
	exit()

fn = 'acrobase.txt'

try:
	with open(fn) as fh:
		acrobase = fh.read()
except:
	print 'Could not read' + fn
	exit()

# Create a dictionary from the acronym / abbreviation file contents:
# ------------------------------------------------------------------
acros = {}
linecounter = 1
l1 = acrobase.split(u'\n')
for el in l1:
	if len(el) != 0:
		if el[0:1] != u'#':
			try:
				veri = True
				key,alternate,expansion = el.split(u',',2)
				if expansion.find('<') != -1: veri = False
				if expansion.find('>') != -1: veri = False
				if veri == True:
					term = key
					if alternate != u'':
						term = alternate
					if acros.get(key,'') != '':
						errors += u'<span style="color:red;">Duplicate ACRO key: '+ unicode(key) + u'</span><br>'
					acros[key] = u'<abbr title="'+expansion+'">'+term+u'</abbr>'
				else:
					errors += u'<span style="color:red;">&lt; or &gt; found in ACRO: '+ unicode(key) + u'</span><br>'
			except:
				errors += u'line '+str(linecounter)+u': '
				errors += u'"<span style="color:red;">'+unicode(el)+u'</span>"<br>'
	linecounter += 1

loclist = sys.argv[1:]
llen = argc - 1

while len(loclist) > 0:
	for n in range(0,llen):
		tst = loclist[n]
		okay = True
		for c in tst:
			if c.isdigit() is False:
				if c.isupper() is False:
					okay = False
					break
		if okay == True:
			res = acros.get(tst,'')
			if res == '':
				print '"' + tst + '" not in acronyms'
			else:
				print tst + ' : ' + res
		else:
			print '"'+tst+'" is not a valid expansion key'
	iput = raw_input(':')
	loclist = iput.split(' ')
	if len(loclist) == 1:
		if loclist[0] == '':
			loclist = []
	llen = len(loclist)

