#!/usr/bin/python
# -*- coding: utf-8 -*-

# Project Info:
# =============
#   Written by: fyngyrz - codes with magnetic needle
#   Incep date: November 24th, 2018
#  Last Update: November 27th, 2018 (code file only)
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

# If you use UTF-8 (emojis, non-English characters), you should
# set this to True. Macro processing is disabled in that case.
# -------------------------------------------------------------
utf8 = False

# If you use this in the utf8 = False mode, then any characters
# above 127 will be replaced with the following string.
# Other sane choices might be '' for just skipping the characters,
# '.' for a period, '--NO UNICODE--' to really annoy yourself,
# etc. You can use anything, just be aware that a lot of "anything"
# will probably make a mess out of your posts. :)
# -----------------------------------------------------------------
ucrep = '<strike>x</strike>'

# Data filenames:
# ===============
# These are user-configurable; you can make these filenames
# anything you like, and put them anywhere you want, and you
# **should**, to provide a layer of obscurity:
# ----------------------------------------------------------
cginame = 'soyacro.py'		# DEFINITELY change this!
ifile = 'acrobase.txt'	# list of known acronyms - see file
mfile = 'aambase.txt'	# list of aa_macro macros - see file

# Likewise, you should rename THIS file, nominally "soyacro.py",
# so that it cannot be found by simply looking in your folders
# by bots, etc. The filename must match the filename in the
# cginame variable just above.
# --------------------------------------------------------------

# The format for each line in the data file is:
# =============================================
# all-caps-keyword,[optional keyword replacement],expansion
#     or...
# blank line
#     or...
# #[optional comment text]
# ------------------------------------------------------------------

# Code - Good luck if you change anything. :)
# ===========================================
# - - - - - - - - - - - - - - - - - - - - - -
# ===========================================

from aa_webpage import *
import cgi,sys,os

undict = {}
errors = u''

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
	usertext = u'A little ASCII to stroke the acronym generator, some {i italics} to run the macro processor.'
	usernote = u'Running from command line'

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
if utf8 == False:
	from aa_macro import *
	if aambase != '':
		mod = macro(noshell=True,noembrace=True,noinclude=True)
		mod.do(aambase)
		mod.do(u'[listg source=local,loclist][asort loclist]')
		thestyles = mod.do(u'[style cnt <span style="color:#00ffff;">[b]</span>][style pur <span style="color:#ff00ff;">[b]</span>][style tmp {pur [ls]}<span style="color:white;">[b]</span>&nbsp;{cnt [i content]}{pur [rs]}][dlist style=tmp,inter=[co] ,loclist]')
		thestylecount = mod.do(u'[llen loclist]')
	else:
		mod = None
		thestyles = u''
		thestylecount = u''
else: # utf8 processing, so no macros
	mod = None
	thestyles = u''
	thestylecount = u''
	aambase = u''

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
				key,alternate,expansion = el.split(u',',2)
				term = key
				if alternate != u'':
					term = alternate
				acros[key] = u'<abbr title="'+expansion+'">'+term+u'</abbr>'
			except:
				errors += u'line '+str(linecounter)+u': '
				errors += u'"<span style="color:red;">'+el+u'</span>"<br>'
	linecounter += 1

# This removes all square braces prior to aa_macro processing.
# That means that only styles can be used; and that, in turn,
# prevents users of the page from using aa_macro's more powerful
# square-bracket commands directly and putting the host at risk.
# --------------------------------------------------------------
metaleft = u'7G6H7f9sJJq'
metaright= u'8fgh36vhd0x'
def nosquares(text):
	global metaleft,metaright
	text = text.replace('[',metaleft)
	text = text.replace(']',metaright)
	return text

# Restores braces, post aa_macro processing
# -----------------------------------------
def repsquares(text):
	global metaleft,metaright
	text = text.replace(metaleft,'[')
	text = text.replace(metaright,']')
	return text

# Converts a unicode string to an ASCII string, replacing any
# characters > 127 with '.'
# -----------------------------------------------------------
def makeascii(text):
	global ucrep
	o = ''
	for i in range(0,len(text)):
		try:
			c = text[i].encode("ascii")
			o += c
		except:
			o += ucrep
	return o

# aa_macro uses squiggly braces for macro invocation. Because it
# can nest macros, the braces must be balanced, or things will
# get out of hand in a hurry. This method makes sure that the
# braces in the post, if any, are balanced; if they are not,
# it cancels aa_macro processing and warns about the problem.
# --------------------------------------------------------------
def testforbalance(text):
	global errors,aambase
	left = 0
	right = 0
	for c in text:		# examine all braces
		if c == u'{':
			left += 1
		elif c == u'}':
			right += 1
	if left != right:	# indication of unbalanced braces
		aambase = u''	# this cancels any {macro} processing
		errors += u'<span style="color: red;">Unbalanced sqiggly braces</span><br>'

# This method determines if what appears to be an acronym (because
# acronyms can have/be numbers) is entirely numeric. If it is, it
# won't warn that it can't expand an unrecongized number group the
# way it does for an all-caps sequence it doesn't recognize.
# ----------------------------------------------------------------
def isnumeric(text):
	for c in text:
		if c < u'0' or c > u'9': return False
	return True

# Convert ALL-CAPS sequences into <abbr>ALL-CAPS</abbr> sequences:
# ----------------------------------------------------------------
def makeacros(text):
	incaps = False
	accum = u''
	o = u''
	for c in text: # iterate all characters
		if (c >= u'A' and c <= u'Z') or (c >= u'0' and c <= u'9'):
			accum += c
		else: # not a cap now
			if len(accum) > 1:
				taccum = acros.get(accum,accum)
				if taccum == accum:
					if isnumeric(taccum) == False:
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
This is an acronym clarifier. When you're going to make a post
on soylentnews.org, which supports use of the <abbr> tag, run the
post through this first, then copy & paste the output into the
Soylent comment box. For example, here's what happens to "ISP."

Save yourself some angst, and use lower case for all your HTML tags. :)
"""

myform = u"""
<FORM ACTION="CGINAME" METHOD="POST">
<div style="text-align: center;">
<TEXTAREA NAME="thetext" ROWS="40" COLS="80">TEXTBLOCK</TEXTAREA><br>
<INPUT TYPE="SUBMIT" VALUE="Submit">
<br><br>
</div>
</FORM>
"""

# The name of this Python file can change. This takes care of the
# invocation being correct in the form above:
# ---------------------------------------------------------------
myform = myform.replace('CGINAME',cginame)

# ready to go, process everything into page body
# ----------------------------------------------
tmp = makeraw(usertext)						# the text you entered
myform = myform.replace(u'TEXTBLOCK',tmp)	# goes into the entry form (again)
mybody = makeraw(mybody)					# the text at the top of the page
mybody = u'<p>'+makeacros(mybody)+u'</p>'	# gets the acronyms stuffed in
mybody += myform							# form added to main page body
mybody += u'<hr>'							# new output section
tmp = makeacros(usertext)					# Now the post gets its acronyms
testforbalance(tmp)		# verify {macro} brace balance
if aambase != '':			# here's the aa_macro processing, if braces balance
	tmp = nosquares(tmp)	# escape any square brackets
	tmp = makeascii(tmp)	# aa_macro requires ASCII string
	tmp = mod.do(tmp)		# process the {macros}
	tmp = repsquares(tmp)	# replace the square brackets
	tmp = makeraw(tmp)		# encode for the textarea

# Add prepped post to a stand-alone textarea:
# -------------------------------------------
mybody += u'<div style="text-align:center;"><div><TEXTAREA NAME="thetext" ROWS="5" COLS="80">'+tmp+u'</TEXTAREA></div><br></div>'

# Report any errors:
# ------------------
if errors != '':
	mybody += u'<hr><div><b><span style="color:orange;">Errors found in</span> <span style="color:white;">'+ifile+u'</span></b><br>'
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
if aambase != '':
	if thestyles != u'':
		mybody += u'<hr><div><span style="color:#00ff00;">Styles ('+thestylecount+u'):</span><br><span style="color:green;">'+thestyles+u'</span></div>'

# Report all known acronyms:
# --------------------------
ka = acros.keys()
if ka != None:
	ka.sort()
	o = u''
	for k in ka:
		o += k+u', '
	kao = o
	if len(kao) > 0: kao = kao[:-2]
	mybody += u'<hr><div><span style="color:#00ff00;">Known ABBRs ('+str(len(ka))+u'):</span><br><span style="color:green;">'+kao+u'</span></div>'

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
			print '\ntest failed!'
		else:
			print 'test passed.'
	else:
		sys.stdout.write(s)
