#!/usr/bin/python

# TODO:
# -----
# CGI widgets
# Tables

class thePage(object):
	"""Class to provide quality web page generation
      Author: fyngyrz  (Ben)
     Contact: fyngyrz@gmail.com (bugs, feature requests, kudos, bitter rejections)
     Project: aa_webpage.py
  Incep Date: May 15th, 2015     (for Project)
     LastRev: May 16th, 2015     (for Class)
  LastDocRev: May 16th, 2015     (for Class)
 Tab spacing: 4 (set your editor to this for sane formatting while reading)
    Examples: At bottom. Run in shell like so:    python aa_webpage.py
 Typical Use: from aa_webpage import *
     1st-Rel: 1.0.0
     Version: 1.0.0
     History:                    (for Class)
		1.0.0 - Initial Release
"""
#
# The default is to supply a link to the HTML validator until you
# (hopefully) set valid = 1, at which point the page will emplace
# a "validated" icon at the bottom. Don't do this until the validator
# tells you that your page is 100% and you are DONE changing the
# page design. If you don't think you can keep the page valid
# because of whatever is happening in the body, or  you simply
# don't want a link to the validator, just set validation = 0
# and it won't put a link OR the icon on the page. Although...
# during page development, it's very handy -- and responsible --
# to see to it that your result page validates.
#
	def __init__(self,
			title		= 'No Title',	# HTML (only) page title
			body		= None,			# Supply page body or use .setBody()
			mode		= 'html',		# defaults to HTML page
			styles		= None,			# Optional styles or use .setStyles()
			validation	= 1,			# Handy pagebottom validation link 0/1
			valid		= 0,			# 1 = CLAIM PAGE VALID  (only if sure!)
			vicon		= None,			# URL to other validate icon
			charset		= 'UTF-8',		# You can supply a different charset
			lang		= 'en',			# You can supply a different language
			forbody		= None,			# Ends up as: <BODY forbody>
			forhead		= None,			# Ends up as: <HEAD>forhead</HEAD>...
										# ...but see also .addHeadEl()
										# ==============================
			doctype		= '4.01s',		# defaults / falls back to 4.01s
										# and  by fall back I mean if you
										# put something here that the import
										# library doesn't know about the you
										# end up with 4.01s. XHTML is NOT
										# supported.
										# ------------------------------
										# Available options are:
										#     4.01s = 4.01 strict
										#     4.01  = 4.01 loose
										#     4.01f = 4.01 frameset
										#     3.2   = 3.2 final
										#     3.2t  = 3.2 Transitional
			cookiejar	= ''):			# Cookie em if you have em

		# Fixed setup  (ignore this):
		#  --------------------------
		self.messages = []
		self.headels = ''
		self.validator = '<p>\n<a href="http://validator.w3.org/check?uri=referer">Validate Page</a>\n</p>\n'
		self.vcheck = '<a href="http://validator.w3.org/check?uri=referer">'
		self.v401 = 'http://www.w3.org/Icons/valid-html401'
		self.v32  = 'http://www.w3.org/Icons/valid-html32'
		self.dtdstr = 'HTML PUBLIC "-//W3C//DTD HTML '
		self.cookiejar = cookiejar
		self.doctypes = {
	# 4.01 strict = 4.01s:
		'4.01s':['[DTDSTR]4.01//EN" "http://www.w3.org/TR/html4/strict.dtd"',
		'[HOTPARA]\n[VCHECK]<img src="'+self.v401+'" alt="Valid HTML 4.01 Strict" height="31" width="88"></a>\n</p>\n',
		'[401V]'],
	# 4.01 loose = 4.01:
		'4.01':['[DTDSTR]4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"',
		'[HOTPARA]\n[VCHECK]<img src="'+self.v401+'" alt="Valid HTML 4.01 Loose" height="31" width="88"></a>\n</p>\n',
		'[401V]'],
	# 4.01 frameset =  4.01f:
		'4.01f':['[DTDSTR]4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd"',
		'[HOTPARA]\n[VCHECK]<img src="'+self.v401+'" alt="Valid HTML 4.01 Frameset" height="31" width="88"></a>\n</p>\n',
		'[401V]'],
	# 3.2 final =  3.2:
		'3.2':['[DTDSTR]3.2 Final//EN"',
		'[HOTPARA]\n[VCHECK]<img src="'+self.v32+'" alt="Valid HTML 3.2 Final" height="31" width="88"></a>\n</p>\n',
		'[32V]'],
	# 3.2 Transitional =  3.2t:
		'3.2t':['[DTDSTR]3.2 Transitional//EN"',
		'[HOTPARA]\n[VCHECK]<img src="'+self.v32+'" alt="Valid HTML 3.2 Transitional" height="31" width="88"></a>\n</p>\n',
		'[32V]'],
}
		# Fluid setup:
		# ------------
		self.setDocType(doctype)
		self.setVIcon(vicon)
		self.setTitle(title)
		self.setStyles(styles)
		self.setBody(body)
		self.setLang(lang)
		self.setForBody(forbody)
		self.setValid(valid)
		self.addHeadEls(forhead)
		self.setCharSet(charset)
		self.setValidation(validation)
		self.setMode(mode)

	# msg MUST be string
	# msgClass can be string, empty string, or None
	# -----------------------------------------------
	def message(self,msg=None,msgClass=None):
		if msgClass != None:
			if type(msgClass) == str:
				if msgClass == '':
					msgClass = 'Message'
			else:
				self.messages += ['ERROR: non-string thingClass in .message()']
				msgClass = 'Unknown'
		else:
			msgClass = 'Message'
		if msg != None:
			if type(msg) == str:
				if msg != '':
						self.messages += [msgClass+': '+msg]
				else:
					self.messages += ['ERROR: Trying to insert empty string as '+msgClass]
			else:
				self.messages += ['ERROR: Trying to insert non-string as '+msgClass]
		else:
			self.messages += ['ERROR: Trying to insert None as '+msgClass]

	def warning(self,warning):
		message(warning,'WARNING: ')

	def error(self,error):
		self.message(error,'ERROR: ')


	def setValidation(self,validation=None):
		if type(validation) == int:
			if validation == 0 or validation == 1:
				self.validation = validation
			else:
				validation = 1
				error('.setValidation() parameter  out of range')
		else:
			validation = 1
			error('NON integer parameter in .setValidation()')

	def setCharSet(self,charset):
		if type(charset) == str:
			if charset != '':
				self.charset = charset
			else:
				self.charset = 'UTF-8'
				error('empty string passed to .setCharSet()')
		else:
			self.charset = 'UTF-8'
			error('non-string parameter in .setCharSet()')

	def setVIcon(self,vicon=None): # characters: link to validation icon
		if vicon != None:
			if type(vicon) == str:
				self.vicon = vicon
			else:
				self.vicon = self.doctypes[self.dtm][2]
				error('non-string parameter in .setVIcon()')
		else:
			self.vicon = self.doctypes[self.dtm][2]

	def setDocType(self,dtm): # character key: 4.01s | 4.01 | 4.01f | 3.2
		try:
			self.doctype = self.doctypes[dtm][0]
		except:
			self.dtm = '4.01s'
			self.doctype = self.doctypes[self.dtm][0]
		else:
			self.dtm = dtm

	def setLang(self,lang): # characters: en, en-gb, etc.
		if type(lang) == str:
			if lang != '':
				self.lang = lang

	def setTitle(self,title): # characters: page title
		if type(title) == str:
			self.title = title
		else:
			self.title = 'Page Title'
			error('non-string passed to .setTitle()')

	def setBody(self,body): #  characters: page content
		self.body = body
		if body != None:
			if type(body) == str:
				if body[-1:] != '\n':
					self.body += '\n'
			else:
				self.body = ''
				error('non-string passed to .setBody()')

	def setValid(self,valid=None): #  integer: 0 or 1
		if valid != None:
			if type(valid) == int:
				if valid == 0 or valid == 1:
					self.valid = valid
				else:
					self.valid = 0
					error('integer out of range for .setValid()')
			else:
				self.valid = 0
				error('non-integer passed to .setValid()')
		else:
			self.valid = 0
			error('No parameter passed to .setValid()')

	def setForBody(self,forbody): #  characters: body tag elements
		if forbody == None:
			self.forbody = ''
		else:
			if type(forbody) == str:
				self.forbody = ' '+forbody
			else:
				self.forbody = ''
				error('non-string passed to .setForBody()')

	def setStyles(self,styles=None): #  characters: local page styles
		self.styles = styles
		if styles != None:
			if type(styles) == str:
				if styles[-1:] != '\n':
					self.styles += '\n'
			else:
				styles = None
				error('non-string parameter passed to .setStyles()')

	def setMode(self,mode=None): # character keyword: 'text' or 'html'
		if mode != None:
			if type(mode) == str:
				if mode != 'html':
					mode = 'text'
			else:
				mode = 'html'
				error('non-string passed to .setMode()')
		else:
			mode = 'html'
		self.mode = mode
		if self.mode != 'html':
			self.header = 'Content-type: text/plain\n\n'
			self.leader = ''
			self.trailer = ''
		else:
			self.header = ''
			self.header += 'Content-type: text/html\n'
			if self.cookiejar != '':
				self.header += self.cookiejar+'\n'
			self.header += '\n'

			self.leader  = '<!DOCTYPE [DOCBLOCK]>\n'
			self.leader += '[HTMLTAG]'
			self.leader += '<HEAD>\n'
			self.leader += '<TITLE>[TITLEBLOCK]</TITLE>\n'
			self.leader += '<META http-equiv="Content-Type" content="text/html; charset='+self.charset+'">\n'
			self.leader += '[HEADELS]'
			self.leader += '[STYLEBLOCK]'
			self.leader += '</HEAD>\n'
			self.leader += '[BODYTAG]'

			self.trailer  = '[ENDBODYTAG]'
			self.trailer += '</HTML>'

	#
	# If you create the web page and don't immediately print the
	# resulting object, you can use .addHeadEls() to add as many
	# items to the <HEAD></HEAD> block as you like; one at a time,
	# or all at once. No formatting is appplied, so if  you want
	# the head region in the web page to be human readable, make
	# sure you provide new-lines and decent formatting for each
	# addition. The convention I use here is that newlines come
	# after a line, not before:
	#
	# wp = thePage(title,body)
	# wp.addHeadEls('<META blah blah>\n')
	# wp.addHeadEls('<LINK blah blah>\n')
	# wp.addHeadEls('<SCRIPT>blah</SCRIPT>\n')
	#  ...and so on
	#
	def addHeadEls(self,headels=None):
		if headels != None:
			if type(headels) == str:
				self.headels += headels
			else:
				error('Trying to insert non-string into HEAD')

	# HTML pages should end with a new line. If you use print
	# with the object, it will. You can use sys.stdout.write()
	# too, but the newline is then up to you. Because...
	# There is no trailing new line output within .__str__()
	# This is so that print can be used directly, as it appends
	# a line feed in typical use. But if you want to, for
	# instance, use sys.stdout.write(), you'd do it like this:
	#
	#	sys.stdout.write(str(tp)+'\n')
	#
	# -------------------------------------------------------------
	def __str__(self):
		s  = self.header
		if self.mode == 'html':
			styleblock = ''
			forbody = ''
			hotpara = '<p>'
			thevcheck = self.vcheck
			vicon = self.v32
			bodytag = '<BODY[FORBODY]>\n'
			endbodytag = '</BODY>\n'
			if self.dtm == '4.01f':
				bodytag = ''
				endbodytag = ''
			if self.dtm != '3.2':
				vicon = self.v401
				hotpara = '<p style="text-align: center;">'
				htmltag = '<HTML lang="[LANGBLOCK]">\n'
				forbody = self.forbody
				if self.styles != None:
					styleblock = '<STYLE type="text/css">\n'
					styleblock += self.styles
					if self.styles[-1:] != '\n':
						styleblock += '\n'
					styleblock += '</STYLE>\n'
			else:
				htmltag = '<HTML>\n'
			leader = self.leader
			leader = leader.replace('[BODYTAG]',bodytag)
			leader = leader.replace('[HTMLTAG]',htmltag)
			leader = leader.replace('[FORBODY]',forbody)
			leader = leader.replace('[DOCBLOCK]',self.doctype)
			leader = leader.replace('[TITLEBLOCK]',self.title)
			leader = leader.replace('[HEADELS]',self.headels)
			leader = leader.replace('[LANGBLOCK]',self.lang)
			leader = leader.replace('[STYLEBLOCK]',styleblock)
			leader = leader.replace('[DTDSTR]',self.dtdstr)
			leader = leader.replace('[401V]',self.v401)
			leader = leader.replace('[32V]',self.v32)
			s += leader
			if self.body != None:
				s += self.body
			else:
				s += 'Empty Body\n'
			if self.messages != []:
				s += '<p>\n'
				for el in self.messages:
					s += el+'<br>\n'
				s += '</p>\n'
			if self.valid == 1:
				validated = self.doctypes[self.dtm][1]
				validated = validated.replace('[VCHECK]',thevcheck)
				validated = validated.replace('[HOTPARA]',hotpara)
				if self.dtm == '3.2':
					validated = '<CENTER>\n'+validated+'</CENTER>\n'
				s += validated
			else:
				if self.validation == 1:
					s += self.validator
			trailer = self.trailer
			trailer = trailer.replace('[ENDBODYTAG]',endbodytag)
			s += trailer
		else:
			if self.body != None:
				s += self.body
			else:
				s += 'Empty Body\n'
		return(s)

# Note that these demos run on the CONSOLE, because they output
# multiple examples.
# =============================================================
# Argument order is title,body,mode,styles
# --------------------------------------------------------------
if __name__ == "__main__":
	# Here's a properly wrapped HTML page:
	# ------------------------------------
	print thePage('Example 1','<p>This is a test</p>\n')

	# Here's one with styles.
	# First we'll set up the styles,
	# then the body, then BAM. :)
	# --------------------------------
	mystyles = """div#note
{
	margin-right: 100px;
	margin-left: 80px;
	margin-bottom: 10px;
	clear: both;    
	padding-left: 10px;
	padding-right: 10px;
	padding-top: 5px;
	padding-bottom: 5px;
	border: 1px solid #000000;
	background: #ddddff;
	color: #000000;
}
"""
	mybody = """<P>
Foo
</p>
<div id="note">
<p>
This is a note
</p>
</div>
<p>
Bar
<\p>
\n"""

	# set up meta tags and body colors
	# --------------------------------
	mtag = '<meta name="robots" content="noindex,nofollow">\n'
	colors = 'style="color: #FFFF00; background-color: #000088;"'

	# You can supply arguments in any order if you name them:
	# -------------------------------------------------------
	print thePage(	title   = 'Example 2',
					styles  = mystyles,
					body    = mybody,
					valid   = 1,
					forhead = mtag,
					forbody = colors)

	# You might want to do setup and content later, like this:
	# --------------------------------------------------------
	wp = thePage()
	wp.setTitle('Example 3')
	wp.setBody('<p>body text<\b>')
	wp.setStyles(mystyles)
	print wp

	# And here's a NON-HTML web page consisting of normal text:
	# ---------------------------------------------------------
	print '\nExample 4'
	print thePage(body='This is a test\n',mode='text')
