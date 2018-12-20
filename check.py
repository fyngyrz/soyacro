#!/usr/bin/python

import sys,re

# Quick way to see if an acronym is in the acrobase.txt file
# ----------------------------------------------------------
# ./check.py MHZ
# ./check.py NAFTA CEO CPU
# ./check.py NOTINHERE 73

# Project Info:
# =============
#   Written by: fyngyrz - codes with magnetic needle
#   Incep date: November 24th, 2018
#  Last Update: December 14th, 2018 (this code file only)
#  Environment: Webserver cgi, HTML 4.01 strict, Python 2.7
# Source Files: soyacro.py, acrobase.txt (these may be renamed)
#               check.py, testacros.py
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

errors = u''
relist = []
rmlist = []
detectcomps = True

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

# This method determines if what appears to be an acronym (because
# acronyms can have/be numbers) is entirely numeric. If it is, it
# won't warn that it can't expand an unrecongized number group the
# way it does for an all-caps sequence it doesn't recognize.
# ----------------------------------------------------------------
def isnumeric(text):
	for c in text:
		if c < u'0' or c > u'9': return False
	return True

def compmatch(term):
	global relist,rmlist,detectcomps
	if detectcomps == False: return term
	if isnumeric(term) == False: # if not fully numeric
		rmatch = False
		ren = 0
		for el in relist:
			ln = len(el)
			el = el + '\d*'
			if re.match(el,term):
				try:
					n = int(term[ln:])
				except: # not a number, bail
					return term
				comp = rmlist[ren]
				ell = comp.split('|')
				if len(ell) == 1:
					string = term + ' : ' +comp + ' ' + str(n)
				else: # multiple elements
					x = 1
					string = ''
					for element in ell:
						if x != 1: string += '\n'
						string += term + ' (%d): %s %d' % (x,element,n)
						x += 1
				return string
			ren += 1
	return term


# Create a dictionary from the acronym / abbreviation file contents:
# ------------------------------------------------------------------
acros = {}
altkeys = {}
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
					if key == '*':
						relist.append(alternate)
						rmlist.append(expansion)
					else:
						if alternate != u'':
							altkeys[key] = alternate
						if acros.get(key,'') != '':
							errors += u'<span style="color:red;">Duplicate ACRO key: '+ unicode(key) + u'</span><br>'
						acros[key] = expansion
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
				res = compmatch(tst)
				if res == tst:
					print '"' + tst + '" not in acronyms'
				else:
					print res
			else:
				ll = res.split('|')
				if len(ll) == 1:
					alt = altkeys.get(tst,'')
					if alt != '': tst = alt
					print tst + ' : ' + res
				else:
					n = 1
					for el in ll:
						print tst + ' (' + str(n) + '): ' + str(el)
						n += 1
		else:
			print '"'+tst+'" is not a valid expansion key'
	iput = raw_input('> ')
	loclist = iput.split(' ')
	if len(loclist) == 1:
		if loclist[0] == '':
			loclist = []
		elif loclist[0] == 'q':
			loclist = []
	llen = len(loclist)

