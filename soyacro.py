#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
start = time.time()

# Project Info:
# =============
#   Written by: fyngyrz - codes with magnetic needle
#   Incep date: November 24th, 2018
#  Last Update: January 19th, 2019 (this code file only)
#  Environment: Webserver cgi, HTML 4.01 strict, Python 2.7
# Source Files: soyacro.py, check.py, testacros.py
#   Data files: acrobase.txt
#  Tab Spacing: Set to 4 for sane readability of Python source
#     Security: Suitable for benign users only (IOW, me.)
#      Purpose: Creates informative <abbr> tag wraps around
#               all-caps terms in the source text. Written
#               to support use of <abbr> on soylentnews.org
#               Also supports canned aa_macro styles via mfile
#      License: None. Use as you will. PD, free, etc.
# Dependencies: aa_webpage.py by fyngyrz
#               aa_macro.py by fyngyrz
#               acroclass.py by fyngyrz
#               standard Python cgi import library
#               standard Python sys import library
#               standard Python os import library
# ----------------------------------------------------------

# =========================================================================
# =========================== CONFIGURATION ===============================
# You can override this with a local file. Just copy the lines below into
# a file called saconfig.txt and set them as you like. Then, as you update
# the project files from the github repo, your config file will override
# the settings here, allowing you to maintain consistent behavior as you
# prefer. Otherwise, every time you update from the repo, the settings
# here will need to be changed if you don't like the defaults.
# =========================================================================

# App Filenames:
# --------------
cginame		= 'soyacro.py'		# this CGI filename
configfile	= 'saconfig.txt'	# configuration override filename
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
showpreview	= True				# show preview of formatted post
showsigs	= True				# all signatures displayed or not
randsigs	= False				# append a random signature when generating
sigecho		= True				# echo the random signature to the page
entlines	= 20				# number of text lines in entry box
reslines	= 20				# number of text lines in result box

# Other
# -----
bgcolor		= 'DDFFDD'		# background color for read-only textboxes

# =========================================================================
# ========================= END CONFIGURATION =============================
# =========================================================================

# Code - Good luck if you change anything. :)
# ===========================================
# - - - - - - - - - - - - - - - - - - - - - -
# ===========================================

from aa_webpage import *
import acroclass
import cgi,sys,os,re

errors = u''

# Create true / False from text parameter:
# ----------------------------------------
def maketf(p,text):
	result = False
	text = text.lower().strip()
	if text == 't' or text == 'true' or text == '1' or text == 'yes':
		result = True
	return result

# create an integer from text, or use default
def makeint(p,text,default):
	try:
		n = int(text)
	except:
		n = default
	return n

# See if there's a config file that overrides the settings in this file:
# ----------------------------------------------------------------------
try:
	with open(configfile) as fh:
		cfbase = fh.read()
except: # it's okay if we can't read this
	pass
else: # but if we did read it, then we process it for settings
	clist = cfbase.split('\n')	# break it into lines
	line = 1
	for el in clist:
		el = el.strip() # remove leading and trailing space(s)
		if el != '' and el[0] != '#':
			thisline = el
			el = el.split('#') # strip off comments if present
			el = el[0]
			try:
				parm,data = el.split('=')
				data = data.replace("'",'')	# terms can be single quoted, but we ignore those
				data = data.replace('"','') # likewise double quotes
			except:
				errors += u'Error on line %d of %s: %s<br>' % (line,configfile,el)
			else: # read the line okay
				parm = parm.strip()
				data = data.strip()
				if parm == 'cginame': cginame = data
				elif parm == 'ifile': ifile = data
				elif parm == 'mfile': mfile = data
				elif parm == 'detectterms':	detectterms = maketf(parm,data)
				elif parm == 'numberterms':	numberterms = maketf(parm,data)
				elif parm == 'detectcomps':	detectcomps = maketf(parm,data)
				elif parm == 'usemacros':	usemacros = maketf(parm,data)
				elif parm == 'showstyles':	showstyles = maketf(parm,data)
				elif parm == 'showacros':	showacros = maketf(parm,data)
				elif parm == 'showpreview':	showpreview = maketf(parm,data)
				elif parm == 'showsigs':	showsigs = maketf(parm,data)
				elif parm == 'randsigs':	randsigs = maketf(parm,data)
				elif parm == 'sigecho':		sigecho = maketf(parm,data)
				elif parm == 'entlines':	entlines = makeint(parm,data,entlines)
				elif parm == 'reslines':	reslines = makeint(parm,data,reslines)
				elif parm == 'bgcolor':		bgcolor = unicode(data)
				else: errors += u'config file; unknown parameter error: %s<br>' % (unicode(thisline))
		line += 1

tiglist = ''
coninput = u''
bgcolor = u'#'+unicode(bgcolor)

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
checkshowpreview=u''
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
		tiglist = tiglist.replace('\t',' ')
		while(tiglist.find(',,') != -1):
			tiglist = tiglist.replace(',,',',')
		while(tiglist.find(' ,') != -1):
			tiglist = tiglist.replace(' ,',',')
		while(tiglist.find(', ') != -1):
			tiglist = tiglist.replace(', ',',')
		while(tiglist.find('  ') != -1):
			tiglist = tiglist.replace('  ',' ')
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
		flag = form['showpreview'].value
		showpreview = True
	except:
		showpreview = False

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
if showsigs == True:	checkshowsignatures = chk
if randsigs == True:	checkautosignature = chk
if usemacros == True:	checkusemacros = chk
if showacros == True:	checkshowexpansions = chk
if showstyles == True:	checkshowstyles = chk
if showpreview == True:	checkshowpreview = chk
if sigecho == True:		checksigecho = chk
if detectcomps == True:	checkdetectcomps = chk
if detectterms == True:	checkdetectterms = chk
if numberterms == True:	checkdetectnumbers = chk;

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

ltiglist = tiglist.split(' ')
ac = acroclass.core(acrofile=ifile,
					iglist=ltiglist,
					detectterms = detectterms,
					numberterms = numberterms,
					detectcomps = detectcomps)

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
ul {
margin-top: -1em;
margin-bottom: 0px;
}
ol {
margin-top: -1em;
margin-bottom: 0px;
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
<INPUT TYPE="checkbox" NAME="showpreview"CHECKSHOWPREVIEW>Show&nbsp;Preview<br>
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
myform = myform.replace(u'CHECKSHOWPREVIEW',checkshowpreview)
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
	conoutput = ac.makeascii(coninput)
	conoutput = conoutput.replace(u'&',u'&amp;')
myform = myform.replace(u'CONOUTPUT',conoutput)

# The name of this Python file can change. This takes care of the
# invocation being correct in the form above:
# ---------------------------------------------------------------
myform = myform.replace(u'CGINAME',unicode(cginame))

# ready to go, process everything into page body
# ----------------------------------------------
testforhtml(usertext)							# test for unbalanced HTML tag braces
tmp = makeraw(usertext)							# the text you entered
myform = myform.replace(u'TEXTBLOCK',tmp)		# goes into the entry form (again)
mybody = makeraw(mybody)						# the text at the top of the page
mybody = u'<p>'+ac.u2u(mybody)+u'</p>'			# gets the acronyms stuffed in
mybody += myform								# form added to main page body
tmp = ac.u2u(usertext)							# Now the post gets its acronyms
testforsquigs(tmp)								# verify {macro} brace balance
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
	tmp = ac.makeascii(tmp)	# aa_macro requires ASCII string
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
tmp = ac.subents(tmp)				# convert char entities into actual unicode

# Add prepped post to a stand-alone textarea:
# -------------------------------------------
resform = u'<div style="text-align:left;"><div><TEXTAREA style="background-color:BGCOLOR;" NAME="thetext" ROWS="RESLINES" COLS="80" readonly>'+tmp+u'</TEXTAREA></div></div>'
resform = resform.replace(u'RESLINES',unicode(str(reslines)))
mybody += resform

if showpreview == True:
	resform = u'Preview:<br><div style="white-space:pre-line; padding-left:3px; color:#000000; width:36em; background-color:#ffffff; border-color:#000000;">TEXTHERE</div>'
	tmp = tmp.replace(u'&lt;',u'<')
	tmp = tmp.replace(u'&gt;',u'>')
	tmp = tmp.replace(u'&amp;',u'&')
	tmp = tmp.replace(u'</li>\n',u'</li>')
	tmp = tmp.replace(u'<blockquote>',u'<blockquote style="margin-bottom:-1em; margin-top:1em; padding-left:3px; border-left:solid; border-left-width:3px; border-left-color:#000000;">')
	resform = resform.replace(u'TEXTHERE',tmp)
	mybody += resform

# Set read-only areas background color
# ------------------------------------
mybody = mybody.replace(u'BGCOLOR',bgcolor)

# Insert random signature pick
# ----------------------------
if rsig != '':
	trsig = rsig.replace('<br>',' ')
	mybody = mybody.replace(u'PUTRSIGHERE',unicode(trsig))
else:
	mybody = mybody.replace(u'PUTRSIGHERE',u'')

# Report any errors:
# ------------------
if errors != u'' or ac.errors != u'':
	mybody += u'<hr><div><b><span style="color:orange;">Errors found:</span></b><br>'
	mybody += errors
	lerrors = ac.errors.replace('\n','<br>')
	mybody += lerrors
	mybody += u'</div>'

# Report any non-fully-numeric caps sequences that are not recognized:
# --------------------------------------------------------------------
unknowns = ac.undict.keys()
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
	ka = ac.acros.keys()
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
end = time.time()
if cmdline == False:
	timestr = u'<div><br>Execution time: '+unicode(str(round(end-start,2)))+u' seconds</div>'
else:
	timestr = u''

tp = thePage(	title   = u'Abbr processor',
				styles  = mystyles,
				body    = mybody+timestr,
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
