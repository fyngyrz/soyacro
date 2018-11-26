#!/usr/bin/python

# Project Info:
# =============
#   Written by: fyngyrz - codes with magnetic needle
#   Incep date: November 24th, 2018
#  Last Update: November 26th, 2018 (code file only)
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
# ----------------------------------------------------------

# Data filename:
# ==============
# These are user-configurable; you can make these filenames
# anything you like, and put them anywhere you want, and you
# **should**, to provide a layer of obsurity:
# ----------------------------------------------------------
cginame = 'soyacro.py'	# DEFINITELY change this!
ifile = 'acrobase.txt'	# list of known acronyms - see file
mfile = 'aambase.txt'	# list of aa_macro macros - see file

# Likewise, you should rename THIS file, nominally "soyacro.py",
# so that it cannot be found by simply looking in your folders
# by bots, etc.
# --------------------------------------------------------------

# The format for each line in the data file is:
# =============================================
# all-caps-keyword,[optional keyword replacement],expansion
#     or...
# blank line
#     or...
# #[optional comment text]
# ------------------------------------------------------------------

# Code - alter at your own risk:
# ==============================

from aa_webpage import *
import cgi
from aa_macro import *

undict = {}
errors = ''

# Read in the user's post content:
# --------------------------------
form = cgi.FieldStorage()

try:
	usertext = form['thetext'].value
	usernote = ''
except:
	usertext = ''
	usernote = 'No text entered'

# Read in the style definitions:
# ------------------------------
try:
	fh = open(mfile)
	aambase = fh.read()
	fh.close
except:
	aambase = ''

# Process the canned styles:
# --------------------------
if aambase != '':
	mod = macro(noshell=True,noembrace=True,noinclude=True)
	mod.do(aambase)
	mod.do('[listg source=local,loclist][asort loclist]')
	thestyles = mod.do('[style cnt <span style="color:#00ffff;">[b]</span>][style pur <span style="color:#ff00ff;">[b]</span>][style tmp {pur [ls]}<span style="color:white;">[b]</span> {cnt [i content]}{pur [rs]}][dlist style=tmp,inter=[co] ,loclist]')
	thestylecount = mod.do('[llen loclist]')
else:
	mod = None
	thestyles = ''
	thestylecount = ''

# Read in the abbreviation / acronym file:
# ----------------------------------------
try:
	fh = open(ifile)
	acrobase = fh.read()
	fh.close()
	acrobase = acrobase.replace('"','&quot;')
except:
	acrobase = ''

# Create a dictionary from the acronym / abbreviation file contents:
# ------------------------------------------------------------------
acros = {}
linecounter = 1
l1 = acrobase.split('\n')
for el in l1:
	if len(el) != 0:
		if el[0:1] != '#':
			try:
				key,alternate,expansion = el.split(',',2)
				term = key
				if alternate != '':
					term = alternate
				acros[key] = '<abbr title="'+expansion+'">'+term+'</abbr>'
			except:
				errors += 'line '+str(linecounter)+': '
				errors += '"<span style="color:red;">'+el+'</span>"<br>'
	linecounter += 1

# This removes all square braces prior to aa_macro processing.
# That means that only styles can be used; and that, in turn,
# prevents users of the page from using aa_macro's more powerful
# square-bracket commands directly and putting the host at risk.
# --------------------------------------------------------------
metaleft = '7G6H7f9sJJq'
metaright= '8fgh36vhd0x'
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
		if c == '{':
			left += 1
		elif c == '}':
			right += 1
	if left != right:	# indication of unbalanced braces
		aambase = ''	# this cancels any {macro} processing
		errors += '<span style="color: red;">Unbalanced sqiggly braces</span><br>'

# This method determines if what appears to be an acronym (because
# acronyms can have/be numbers) is entirely numeric. If it is, it
# won't warn that it can't expand an unrecongized number group the
# way it does for an all-caps sequence it doesn't recognize.
# ----------------------------------------------------------------
def isnumeric(text):
	for c in text:
		if c < '0' or c > '9': return False
	return True

# Convert ALL-CAPS sequences into <abbr>ALL-CAPS</abbr> sequences:
# ----------------------------------------------------------------
def makeacros(text):
	incaps = False
	accum = ''
	o = ''
	for c in text: # iterate all characters
		if (c >= 'A' and c <= 'Z') or (c >= '0' and c <= '9'):
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
				accum = ''
			else: # 1 or 0
				o += accum
				accum = ''
				o += c
	if accum != '': # any pending on end of post?
		if len(accum) > 1:
			taccum = acros.get(accum,accum)
			if taccum == accum:
				if isnumeric(taccum) == False:
					undict[taccum] = 1 # we don't know this one
			accum = taccum
			o += accum
			accum = ''
		else: # 1 or 0
			o += accum
			accum = ''
	return o

# HTML conversion of some active HTML entities so formatted for repost
# --------------------------------------------------------------------
reps = {'<':'&lt;',
'>':'&gt;',
'&':'&amp;'}

def makeraw(text):
	o = ''
	for c in text:
		c = reps.get(c,c)
		o += c
	return o

# Our HTML Page setup
# -------------------
mtag = '<meta name="robots" content="noindex,nofollow">\n'
colors = 'style="color: #FFFF00; background-color: #000088;"'
mystyles = """
abbr {
border-bottom: red dashed;
}
"""

mybody = """
This is an acronym clarifier. When you're going to make a post
on soylentnews.org, which supports use of the <acro> tag, run the
post through this first, then copy & paste the output into the
Soylent comment box. For example, here's what happens to "ISP."

Save yourself some angst, and use lower case for all your HTML tags. :)
"""

myform = """
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
myform = myform.replace('TEXTBLOCK',tmp)	# goes into the entry form (again)
mybody = makeraw(mybody)					# the text at the top of the page
mybody = '<p>'+makeacros(mybody)+'</p>'		# gets the acronyms stuffed in
mybody += myform							# form added to main page body
mybody += '<hr>'
tmp = makeacros(usertext)					# Now the post gets its acronyms
testforbalance(tmp)							# verify {macro} brace balance
if aambase != '':			# here's the aa_macro processing, if braces balance
	tmp = nosquares(tmp)	# escape any square brackets
	tmp = mod.do(tmp)		# process the {macros}
	tmp = repsquares(tmp)	# replace the square brackets
	tmp = makeraw(tmp)		# encode for the textarea

# Add prepped post to a stand-alone textarea:
# -------------------------------------------
mybody += '<div style="text-align:center;"><div><TEXTAREA NAME="thetext" ROWS="5" COLS="80">'+tmp+'</TEXTAREA></div><br></div>'

# Report any errors:
# ------------------
if errors != '':
	mybody += '<hr><div><b><span style="color:orange;">Errors found in</span> <span style="color:white;">'+ifile+'</span></b><br>'
	mybody += errors
	mybody += '</div>'

# Report any non-fully-numeric caps sequences that are not recognized:
# --------------------------------------------------------------------
unknowns = undict.keys()
if unknowns != []:
	unknowns.sort()
	o = ''
	for el in unknowns:
		o += '<span style="color:red;">'+el+'</span>, '
	o = o[:-2]
	mybody += '<hr><p><b><span style="color:orange;">Unknown all-CAPS sequences:</span></b><br>'+o+'</p>'

# If there are styles (and there should be), list them:
# -----------------------------------------------------
if thestyles != '':
	mybody += '<hr><div><span style="color:#00ff00;">Styles ('+thestylecount+'):</span><br><span style="color:green;">'+thestyles+'</span></div>'

# Report all known acronyms:
# --------------------------
ka = acros.keys()
if ka != None:
	ka.sort()
	o = ''
	for k in ka:
		o += k+', '
	kao = o
	if len(kao) > 0: kao = kao[:-2]
	mybody += '<hr><div><span style="color:#00ff00;">Known ABBRs ('+str(len(ka))+'):</span><br><span style="color:green;">'+kao+'</span></div>'

mybody += '<hr>'

# Finally, produce the web page:
# ------------------------------
print thePage(	title   = 'Abbr processor',
				styles  = mystyles,
				body    = mybody,
				valid   = 1,
				forhead = mtag,
				forbody = colors)
