#!/usr/bin/python
# -*- coding: utf-8 -*-

# Project Info:
# =============
#   Written by: fyngyrz - codes with magnetic needle
#   Incep date: November 24th, 2018
#  Last Update: January 10th, 2019 (this code file only)
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

# =========================================================================
# =========================== CONFIGURATION ===============================
# =========================================================================

# App Filenames:
# --------------
cginame		= 'soyacro.py'		# this CGI filename
ifile		= 'acrobase.txt'	# acronyms filename
mfile		= 'aambase.txt'		# macros filename

# Initial Web Page Options:
# -------------------------
detectterms	= True				# detect general terms
numberterms	= False				# detect completely numeric terms
detectcomps	= True				# detect electronic component designations
usemacros	= True				# macro styles enabled or not
showstyles	= True				# macro styles displayed or not
showacros	= False				# all acronyms displayed or not
showsigs	= True				# all signatures displayed or not
randsigs	= False				# append a random signature when generating
sigecho		= True				# echo the random signature to the page
entlines	= 20				# number of text lines in entry box
reslines	= 20				# number of text lines in result box

# Other
# -----
bgcolor		= u'#DDFFDD'		# background color for read-only textboxes

# =========================================================================
# ========================= END CONFIGURATION =============================
# =========================================================================

# Code - Good luck if you change anything. :)
# ===========================================
# - - - - - - - - - - - - - - - - - - - - - -
# ===========================================

from aa_webpage import *
import cgi,sys,os
import re

# returns true if text is an integer
# ----------------------------------
def chkint(text):
	try:
		n = int(text)
	except:
		return False
	return True

undict = {}
errors = u''
tiglist = ''
coninput = u''

# These provide for matching component designations
# -------------------------------------------------
relist = [] # regular expressions
rmlist = [] # component terms

if 'GATEWAY_INTERFACE' in os.environ:
	cmdline = False
else:
	cmdline = True

# Read in the user's post content:
# --------------------------------
if cmdline == False:
	form = cgi.FieldStorage()
	try:
		usertext = unicode(form['thetext'].value,'UTF-8')
		usernote = u''
	except Exception,e:
		usertext = u''
		usernote = u'No text entered'
else: # we're running from command line
	usertext = u'skip this: <abbr title="testing">DONTTREADONME</abbr> uchar pizza: &#127829; and a little ASCII to stroke the acronym generator, some {i italics} to run the macro processor.'
	usernote = u'Running from command line'

# Set the flags
# -------------
checkautosignature=u''
checkshowsignatures=u''
checkusemacros=u''
checkshowexpansions=u''
checkshowstyles=u''
checksigecho=u''
checkdetectcomps=u''
checkdetectterms=u''
checkdetectnumbers=u''

# Detect if this is a resubmit or an initial entry:
# -------------------------------------------------
try:
	flag = form['resubmit'].value
	resubmit = True
except:
	resubmit = False
hidden = u''

# If the form isn't being resubmitted, we skip using
# the checkboxes to set the initial conditions, and
# instead will default to the variable settings
# above.
# --------------------------------------------------
if resubmit == True:
	try:
		val = int(form['entlines'].value)
		if val < 10: val = 10
		elif val > 50: val = 50
		entlines = val
	except:
		pass

	try:
		val = unicode(form['coninput'].value,'UTF-8')
		coninput = val
		if val == 'CONINPUT':
			coninput = u''
	except:
		coninput = u''

	try:
		val = form['iglist'].value
		tiglist = val
		if val == 'IGLIST':
			tiglist = ''
		tiglist = tiglist.replace(',',' ') # allow use of commas
		tiglist = tiglist.upper()
	except:
		tiglist = ''

	try:
		val = int(form['reslines'].value)
		if val < 10: val = 10
		elif val > 50: val = 50
		reslines = val
	except:
		pass

	try:
		flag = form['signature'].value
		randsigs = True
	except:
		randsigs = False

	try:
		flag = form['sigecho'].value
		sigecho = True
	except:
		sigecho = False

	try:
		flag = form['detectcomps'].value
		detectcomps = True
	except:
		detectcomps = False

	try:
		flag = form['detectterms'].value
		detectterms = True
	except:
		detectterms = False

	try:
		flag = form['detectnumbers'].value
		numberterms = True
	except:
		numberterms = False

	try:
		flag = form['showsignatures'].value
		showsigs = True
	except:
		showsigs = False

	try:
		flag = form['usemacros'].value
		usemacros = True
	except:
		usemacros = False

	try:
		flag = form['showexpansions'].value
		showacros = True
	except:
		showacros = False

	try:
		flag = form['showstyles'].value
		showstyles = True
	except:
		showstyles = False

# Now set the checkmarks in the form:
# -----------------------------------
chk = u'CHECKED'
if showsigs == True: checkshowsignatures = chk
if randsigs == True: checkautosignature = chk
if usemacros == True: checkusemacros = chk
if showacros == True: checkshowexpansions = chk
if showstyles == True: checkshowstyles = chk
if sigecho == True: checksigecho = chk
if detectcomps == True: checkdetectcomps = chk
if detectterms == True: checkdetectterms = chk
if numberterms == True: checkdetectnumbers = chk;

# Override autosigs if '{nsig ' is present
if usertext.find('{nsig ') != -1:
	randsigs = False

# Read in the style definitions:
# ------------------------------
try:
	with open(mfile) as fh:
		aambase = fh.read()
except Exception,e:
	aambase = u''
	errors += u'failed to read file'+str(e)+u'<br>'

# Process the canned styles:
# --------------------------
if usemacros == True:
	from aa_macro import *
	if aambase != '':
		mod = macro(noshell=True,noembrace=True,noinclude=True)
		mod.do(aambase)
		mod.do('[listg source=local,loclist][asort loclist]')
		thestyles = mod.do('[dlist style=dls,inter=[co] ,loclist]')
		thestylecount = mod.do('[llen loclist]')
	else:
		mod = None
		thestyles = u''
		thestylecount = u''
else:
	aambase = ''
	mod = None
	thestyles = u''
	thestylecount = u''

# Read in the abbreviation / acronym file:
# ----------------------------------------
try:
	with open(ifile) as fh:
		acrobase = fh.read()
except Exception,e:
	acrobase = u''
	errors += u'failed to read file'+str(e)+u'<br>'
else:
	acrobase = acrobase.replace(u'"',u'&quot;') # can't have quotes in abbr tags

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
					if key == '*': # if this is a component designator
						if detectcomps == True:
							rmlist.append(expansion)
							relist.append(alternate)
						else:
							pass
					elif numberterms == False and chkint(key) == True:
						pass
					else: # normal term definition
						term = key
						if alternate != u'':
							term = alternate
						if acros.get(key,'') != '':
							errors += u'<span style="color:red;">Duplicate ACRO key: '+ unicode(key) + u'</span><br>'
						alist = expansion.split('|')
						if len(alist) == 1:
							acros[key] = u'<abbr title="'+expansion+'">'+term+u'</abbr>'
						else:
							alist.sort()
							s = u''
							n = 1
							for el in alist:
								if n != 1: s = s + u' '
								s = s + u'(' + unicode(str(n)) + u'): '+unicode(str(el))
								n += 1
							acros[key] = u'<abbr title="'+s+'">'+term+u'</abbr>'
				else:
					errors += u'<span style="color:red;">&lt; or &gt; found in ACRO: '+ unicode(key) + u'</span><br>'
			except Exception,e:
				errors += u'line '+str(linecounter)+u': '
				errors += u'"<span style="color:red;">'+unicode(el)+u'</span>"<br>'+unicode(str(e))
	linecounter += 1

# remove any items in the ignore list:
# ------------------------------------
nonolist = {}
iglist = tiglist.split(' ')
for el in iglist:
	el = el.strip()
	if el != '':
		try:
			nonolist[el] = True
			del acros[el]
		except:
			pass

# This removes all square braces prior to aa_macro processing.
# That means that only styles can be used; and that, in turn,
# prevents users of the page from using aa_macro's more powerful
# square-bracket commands directly and putting the host at risk.
# --------------------------------------------------------------
metaleft = u'7G6H7f9sJJqhdfudf67'
metaright= u'8fgh36vhd0x7887fgsz'
def nosquares(text):
	global metaleft,metaright
	text = text.replace('[',metaleft)
	text = text.replace(']',metaright)
	return text

# Restores square brackets, post aa_macro processing
# --------------------------------------------------
def repsquares(text):
	global metaleft,metaright
	text = text.replace(metaleft,'[')
	text = text.replace(metaright,']')
	return text

# This converts character entities into actual unicode
# ----------------------------------------------------
def subents(text):
	state = 0 # nothing detected
	accum = u''
	o = u''
	for c in text:
		if state == 0:		# nothing as yet?
			if c == u'&':	# ampersand?
				state = 1	# ampersand!
			else:
				o += c
		elif state == 1:	# ampersand found?
			if c == u'#':	# hash?
				state = 2	# hash!
				accum = u''	# clear accumulator
			else:			# not a hash, so not an entity encoding
				state = 0	# abort
				o += u'&'+c	# flush char, done
		elif state == 2:	# expecting digits or terminating semicolon
			if c.isdigit():	# digit?
				accum += c	# add it to accumulator if so
			elif c == u';':	# terminating
				s = u'\\U%08x' % (int(accum))
				ss= s.decode('unicode-escape')
				o += ss
				state = 0
			else: # bad encoding?
				o += u'&#'
				o += accum
				state = 0
	return o

# Converts a unicode string to an ASCII string, replacing any
# characters > 127 with the appropriate character entity.
# That in turn makes the text compatible with the macro
# processor, as character entities are 100$ ASCII.
# -----------------------------------------------------------
def makeascii(text):
	o = ''
	for i in range(0,len(text)):
		try:
			c = text[i].encode("ascii")
			o += c
		except:
			o += '&#{:d};'.format(ord(text[i]))
	return o

# general balance tester
# ----------------------
def lrtest(a,b,text):
	left = 0
	right = 0
	for c in text:
		if c == a:
			left += 1
		elif c == b:
			right += 1
	if left != right:
		return False
	return True

# aa_macro uses squiggly braces for macro invocation. Because it
# can nest macros, the braces must be balanced, or things will
# get out of hand in a hurry. This method makes sure that the
# braces in the post, if any, are balanced; if they are not,
# it cancels aa_macro processing and warns about the problem.
# --------------------------------------------------------------
def testforsquigs(text):
	global errors,aambase
	if lrtest(u'{',u'}',text) == False:
		aambase = u''	# this cancels any {macro} processing
		errors += u'<span style="color: red;">Unbalanced {...} braces</span><br>'

# If there are unbalanced angle braces, they should be character entities
# -----------------------------------------------------------------------
def testforhtml(text):
	global errors
	if lrtest(u'<',u'>',text) == False:
		errors += u'<span style="color: red;">Unbalanced &lt;...&gt; braces: need &amp;lt; or &amp;gt; ? Or is an HTML tag unclosed?</span><br>'

# This method determines if what appears to be an acronym (because
# acronyms can have/be numbers) is entirely numeric. If it is, it
# won't warn that it can't expand an unrecogized number group the
# way it does for an all-caps sequence it doesn't recognize.
# ----------------------------------------------------------------
def isnumeric(text):
	for c in text:
		if c < u'0' or c > u'9': return False
	return True

def compmatch(term):
	global relist,rmlist,detectcomps,errors
	if detectcomps == False: return term
	if nonolist.get(term,False) == True: return term
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
					pass
				else:
					comp = rmlist[ren]
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

# Convert ALL-CAPS sequences into <abbr>ALL-CAPS</abbr> sequences:
# ----------------------------------------------------------------
def makeacros(text):
	global detectterms
	if detectterms == False: return text
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
				taccum = acros.get(accum,accum)
				if taccum == accum: # not found
					if isnumeric(accum) == False: # if not fully numeric
						taccum = compmatch(accum)
						if taccum == accum: # still not found
							undict[taccum] = 1 # we don't know this one
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
			taccum = acros.get(accum,accum)
			if taccum == accum:
				if isnumeric(taccum) == False:
					taccum = compmatch(accum)
					if taccum == accum: # still not found
						undict[taccum] = 1 # we don't know this one
			accum = taccum
			o += accum
		else: # 1 or 0
			o += accum
	return o

# HTML conversion of some active HTML entities so formatted for repost
# --------------------------------------------------------------------
reps = {u'<':u'&lt;',
u'>':u'&gt;',
u'&':u'&amp;'}

def makeraw(text):
	o = u''
	for c in unicode(text):
		c = reps.get(c,c)
		o += c
	return o

# Our HTML Page setup
# -------------------
mtag = u'<meta name="robots" content="noindex,nofollow">\n'
colors = u'style="color: #FFFF00; background-color: #000088;"'
mystyles = u"""
abbr {
border-bottom: red dashed;
}
"""

mybody = u"""
This is an all-caps-and/or-digits term clarifier and macro system. When
you're going to make a post on soylentnews.org, which supports use of
the <abbr> tag, run the post through this first, then copy & paste the
output into the Soylent comment box. For example, here's what happens to
"ISP." Be sure to enter any term you want replaced as
all-caps-and/or-digits.
"""

myform = u"""
PUTRSIGHERE<FORM ACTION="CGINAME" METHOD="POST">
<div style="text-align: center;">
<div>
<div style="float:left;">
<TEXTAREA NAME="thetext" ROWS="ENTLINES" COLS="80">TEXTBLOCK</TEXTAREA><br>
Ignore List: <INPUT TYPE="TEXT" NAME="iglist" SIZE="64" VALUE="IGLIST">
<br><div style="text-align:center;">Unicode conversion: <INPUT TYPE="TEXT" NAME="coninput" SIZE="10" VALUE="CONINPUT">&rarr;<INPUT style="background-color:BGCOLOR;" TYPE="TEXT" NAME="conoutput" SIZE="40" VALUE="CONOUTPUT" readonly><br></div></div>
</div>
<div style="float:left;"><div style="float:right; text-align:left;"><INPUT TYPE="hidden" NAME="resubmit" VALUE="foo">
<INPUT TYPE="checkbox" NAME="detectterms"CHECKDETECTTERMS>Detect&nbsp;Terms<br>
<INPUT TYPE="checkbox" NAME="detectnumbers"CHECKDETECTNUMBERS>Detect&nbsp;Number&nbsp;Terms<br>
<INPUT TYPE="checkbox" NAME="detectcomps"CHECKDETECTCOMPS>Detect&nbsp;Electronic&nbsp;Components<br>
<INPUT TYPE="checkbox" NAME="usemacros"CHECKUSEMACROS>Use&nbsp;Macros<br>
<INPUT TYPE="checkbox" NAME="showstyles"CHECKSHOWSTYLES>Show&nbsp;Macros<br>
<INPUT TYPE="checkbox" NAME="signature"CHECKAUTOSIGNATURE>Auto&nbsp;Signature<br>
<INPUT TYPE="checkbox" NAME="sigecho"CHECKSIGECHO>Echo&nbsp;Auto&nbsp;Signature<br>
<INPUT TYPE="checkbox" NAME="showsignatures"CHECKSHOWSIGNATURES>Show&nbsp;Signatures<br>
<INPUT TYPE="checkbox" NAME="showexpansions"CHECKSHOWEXPANSIONS>Show&nbsp;Expansions<br>
<INPUT TYPE="TEXT" NAME="entlines" SIZE="3" VALUE="ENTLINES">&nbsp;Entry Lines<br>
<INPUT TYPE="TEXT" NAME="reslines" SIZE="3" VALUE="RESLINES">&nbsp;Result Lines<br>
<br>
<INPUT TYPE="SUBMIT" VALUE="Submit">
</div>
<br><br>
</div>
</div>
</FORM>
"""

myform = myform.replace(u'ENTLINES',unicode(str(entlines)))
myform = myform.replace(u'CHECKSHOWSIGNATURES',checkshowsignatures)
myform = myform.replace(u'CHECKAUTOSIGNATURE',checkautosignature)
myform = myform.replace(u'CHECKSIGECHO',checksigecho)
myform = myform.replace(u'CHECKUSEMACROS',checkusemacros)
myform = myform.replace(u'CHECKSHOWSTYLES',checkshowstyles)
myform = myform.replace(u'CHECKSHOWEXPANSIONS',checkshowexpansions)
myform = myform.replace(u'ENTLINES',str(entlines))
myform = myform.replace(u'RESLINES',str(reslines))
myform = myform.replace(u'IGLIST',tiglist)
myform = myform.replace(u'CHECKDETECTCOMPS',checkdetectcomps)
myform = myform.replace(u'CHECKDETECTTERMS',checkdetectterms)
myform = myform.replace(u'CHECKDETECTNUMBERS',checkdetectnumbers)
myform = myform.replace(u'CONINPUT',coninput)
conoutput = ''
if coninput != '':
	conoutput = makeascii(coninput)
	conoutput = conoutput.replace(u'&',u'&amp;')
myform = myform.replace(u'CONOUTPUT',conoutput)


# The name of this Python file can change. This takes care of the
# invocation being correct in the form above:
# ---------------------------------------------------------------
myform = myform.replace(u'CGINAME',unicode(cginame))

# ready to go, process everything into page body
# ----------------------------------------------
testforhtml(usertext)						# test for unbalanced HTML tag braces
tmp = makeraw(usertext)						# the text you entered
myform = myform.replace(u'TEXTBLOCK',tmp)	# goes into the entry form (again)
mybody = makeraw(mybody)					# the text at the top of the page
mybody = u'<p>'+makeacros(mybody)+u'</p>'	# gets the acronyms stuffed in
mybody += myform							# form added to main page body
#mybody += u'<hr>'							# new output section
tmp = makeacros(usertext)					# Now the post gets its acronyms
testforsquigs(tmp)			# verify {macro} brace balance
rsig = ''
rsignum = ''
if aambase != '':			# here's the aa_macro processing, if braces balance
	if randsigs == True:
		if tmp[-1:] != u'\n':
			tmp += u'\n'
		rsig = mod.do('\n{sig}')
		rsignum = mod.do('[add 1 [v rresult]]')
		tmp += unicode(rsig)
	tmp = nosquares(tmp)	# escape any square brackets
	tmp = makeascii(tmp)	# aa_macro requires ASCII string
	tmp = mod.do(tmp)		# process the {macros}
	tmp = repsquares(tmp)	# replace the square brackets
	tmp = makeraw(tmp)		# encode for the textarea
if sigecho == False: rsig = ''
else:
	rsig = rsig.replace('\n','<br>')
	grn = '<span style="color:#ff8844;">'
	rrn = '<span style="color:#ff00ff;">'
	zsn = ' '+grn+'(</span>'+rrn+rsignum+'</span>'+grn+')</span>'
	rsig = rsig.replace('--','--'+zsn)
	rsig = '<div style="text-align:left;">'+rsig+'</div>'

tmp = tmp.replace(u'&amp;#',u'&#')	# watch out for intended char entities
tmp = subents(tmp)					# convert char entities into actual unicode

# Add prepped post to a stand-alone textarea:
# -------------------------------------------
resform = u'<div style="text-align:left;"><div><TEXTAREA style="background-color:BGCOLOR;" NAME="thetext" ROWS="RESLINES" COLS="80" readonly>'+tmp+u'</TEXTAREA></div><br></div>'
resform = resform.replace(u'RESLINES',unicode(str(reslines)))
mybody += resform
mybody = mybody.replace(u'BGCOLOR',bgcolor)
if rsig != '':
	trsig = rsig.replace('<br>',' ')
	mybody = mybody.replace(u'PUTRSIGHERE',unicode(trsig))
else:
	mybody = mybody.replace(u'PUTRSIGHERE',u'')

# Report any errors:
# ------------------
if errors != '':
	mybody += u'<hr><div><b><span style="color:orange;">Errors found:</span></b><br>'
	mybody += errors
	mybody += u'</div>'

# Report any non-fully-numeric caps sequences that are not recognized:
# --------------------------------------------------------------------
unknowns = undict.keys()
if unknowns != []:
	unknowns.sort()
	o = u''
	for el in unknowns:
		o += u'<span style="color:red;">'+el+u'</span>, '
	o = o[:-2]
	mybody += u'<hr><p><b><span style="color:orange;">Unknown all-CAPS sequences:</span></b><br>'+o+u'</p>'

# If there are styles (and there should be), list them:
# -----------------------------------------------------
if showstyles == True:
	if aambase != '':
		if thestyles != '':
			thestylecount = unicode(thestylecount)
			thestyles = unicode(thestyles)
			mybody += u'<hr><div><span style="color:#00ff00;">Macros ('+thestylecount+u'):</span><br><span style="color:green;">'+thestyles+u'</span></div>'

if usemacros == True and showsigs == True:
	siglist = unicode(mod.do('{wlsigs}'))
	siglist = siglist.replace(u'\n',u'<br>\n')
	siglist = u'<hr><div><span style="color:#00ff00;">Signatures:</span><br>\n'+siglist+u'</div>'
	mybody += siglist

# Report all known acronyms:
# --------------------------
if showacros == True:
	ka = acros.keys()
	if ka != None:
		ka.sort()
		o = u''
		for k in ka:
			o += k+u', '
		kao = o
		if len(kao) > 0: kao = kao[:-2]
		mybody += u'<hr><div><span style="color:#00ff00;">Known ABBRs ('+str(len(ka))+u'):</span><br><span style="color:green;">'+kao+u'</span></div>'

# Last section, wall it off:
mybody += u'<hr>'

# Finally, produce the web page:
# ------------------------------
tp = thePage(	title   = u'Abbr processor',
				styles  = mystyles,
				body    = mybody,
				valid   = 1,
				forhead = mtag,
				forbody = colors)

s = (tp.assemble() + u'\n').encode('UTF-8')
tfile = 'testfile.uco'
if 0:
	with open(tfile,'w') as fh:
		fh.write(s)
else:
	if cmdline == True:
		with open(tfile) as fh:
			canned = fh.read()
		if canned != s:
			print s
			print '\ntest file does not match. New macros?'
		else:
			print 'test passed.'
	else:
		sys.stdout.write(s)
