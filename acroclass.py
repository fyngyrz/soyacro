import re

class core(object):
	# Project Info:
	# =============
	#   Written by: fyngyrz - codes with magnetic needle
	#   Incep date: November 24th, 2018
	#  Last Update: January 12th, 2019 (this code file only)
	#  Environment: Python 2.7
	# Source Files: acroclass.py
	#  Tab Spacing: Set to 4 for sane readability of Python source
	#     Security: Suitable for benign users only (IOW, me.)
	#      Purpose: Creates informative <abbr> tag wraps around
	#               all-caps terms in the source text. Written
	#               to support use of <abbr> on soylentnews.org
	#      License: None. Use as you will. PD, free, etc.
	# Dependencies: standard Python re import library
	# ----------------------------------------------------------

	def version_set(self):
		return('0.0.1 Beta')

	def __init__(self,	detectterms=True,			# disable class.makeacros() = False
						numberterms=False,			# disable detecting terms incorporating numbers
						detectcomps=True,			# detect electronic components
						iglist=[],					# terms to ignore
						acrofile='acrobase.txt'):	# file to load term expansions from
		self.version = self.version_set()
		self.detectterms = detectterms
		self.numberterms = numberterms
		self.detectcomps = detectcomps
		self.acrofile = acrofile
		self.igdict = {}
		self.undict = {}
		self.acros = {}
		self.rmlist = []
		self.relist = []
		self.errors = u''
		self.setacros(acrofile)
		self.geniglist(iglist)

	def geniglist(self,iglist):
		for el in iglist:
			el = str(el).upper()
			self.igdict[el] = True
			try:
				del self.acros[el]
			except:
				pass

	def setacros(self,acrofile):
		try:
			with open(acrofile) as fh:
				self.acrobase = fh.read()
		except Exception,e:
			self.acrobase = u''
			self.errors += u'failed to read file'+str(e)+u'\n'
		else:
			self.acrobase = self.acrobase.replace(u'"',u'&quot;') # can't have quotes in abbr tags
			self.makedict()

	def chkint(self,text):
		try:
			n = int(text)
		except:
			return False
		return True

	def makedict(self):
		# Create a dictionary from the acronym / abbreviation file contents:
		# ------------------------------------------------------------------
		self.acros = {}
		linecounter = 1
		l1 = self.acrobase.split(u'\n')
		for el in l1:
			if len(el) != 0:
				if el[0:1] != u'#':
					try:
						veri = True
						key,alternate,expansion = el.split(u',',2)
						if expansion.find('<') != -1: veri = False
						if expansion.find('>') != -1: veri = False
						if veri == True:
							if key == '*': # if this is a component designator
								if self.detectcomps == True:
									self.rmlist.append(expansion)
									self.relist.append(alternate)
								else:
									pass
							elif self.numberterms == False and self.chkint(key) == True:
								pass
							else: # normal term definition
								term = key
								if alternate != u'':
									term = alternate
								if self.acros.get(key,'') != '':
									self.errors += u'Duplicate ACRO key: '+ unicode(key) + u'\n'
								alist = expansion.split('|')
								if len(alist) == 1:
									self.acros[key] = u'<abbr title="'+expansion+'">'+term+u'</abbr>'
								else:
									alist.sort()
									s = u''
									n = 1
									for el in alist:
										if n != 1: s = s + u' '
										s = s + u'(' + unicode(str(n)) + u'): '+unicode(str(el))
										n += 1
									self.acros[key] = u'<abbr title="'+s+'">'+term+u'</abbr>'
						else:
							self.errors += u'&lt; or &gt; found in ACRO: '+ unicode(key) + u'\n'
					except Exception,e:
						self.errors += u'line '+str(linecounter)+u': '
						self.errors += u'"'+unicode(el)+u'"\n'+unicode(str(e))
			linecounter += 1

	def compmatch(self,term):
		if self.detectcomps == False: return term
		if self.igdict.get(term,False) == True: return term
		if self.isnumeric(term) == False: # if not fully numeric
			rmatch = False
			ren = 0
			for el in self.relist:
				ln = len(el)
				el = el + '\d*'
				if re.match(el,term):
					try:
						n = int(term[ln:])
					except: # not a number, bail
						pass
					else:
						comp = self.rmlist[ren]
						ell = comp.split('|')
						if len(ell) == 1:
							string = '<abbr title="'+comp + ' ' + str(n) + '">'+term+'</abbr>'
						else: # multiple elements
							x = 1
							string = '<abbr title="'
							ell.sort()
							for element in ell:
								if x != 1: string += ' '
								string += '(%d): %s %d' % (x,element,n)
								x += 1
							string += '">'+term+'</abbr>'
						return string
				ren += 1
		return term

	def isnumeric(self,text):
		for c in text:
			if c < u'0' or c > u'9': return False
		return True

	def makeacros(self,text):
		if self.detectterms == False: return text
		incaps = False
		accum = u''
		o = u''
		ctag = u''
		wait = False
		wait2 = False
		for c in text: # iterate all characters
			if c == u'<':
				wait = True	# if within an HTML tag, don't bother
				ctag = u''	# reset abbr detector
			elif c == u'>': wait = False
			ctag += c.lower()
			if ctag[:5] == u'<abbr':
				wait2 = True	# ignore between <abbr></abbr>
				ctag = u''
			elif ctag[:6] == u'</abbr':
				wait2 = False
				ctag = u''
			if wait == False and wait2 == False and ((c >= u'A' and c <= u'Z') or (c >= u'0' and c <= u'9')):
				accum += c
			else: # not a cap now
				if len(accum) > 1:
					taccum = self.acros.get(accum,accum)
					if taccum == accum: # not found
						if self.isnumeric(accum) == False: # if not fully numeric
							taccum = self.compmatch(accum)
							if taccum == accum: # still not found
								if self.igdict.get(taccum,'') == '':
									self.undict[taccum] = 1 # we don't know this one
					accum = taccum
					accum += c
					o += accum
					accum = u''
				else: # 1 or 0
					o += accum
					accum = u''
					o += c
		if accum != u'': # any pending on end of post?
			if len(accum) > 1:
				taccum = self.acros.get(accum,accum)
				if taccum == accum:
					if self.isnumeric(taccum) == False:
						taccum = self.compmatch(accum)
						if taccum == accum: # still not found
							if self.igdict.get(taccum,'') == '':
								self.undict[taccum] = 1 # we don't know this one
				accum = taccum
				o += accum
			else: # 1 or 0
				o += accum
		return o
