#!/usr/bin/perl

# You can test the speed here by firing this off this way:
#     yourCmdPrompt:time ./pltest.pl
# --------------------------------------------------------

# This is a test file for "acroclass.pm" -- it runs the class through
# various combinations of circumstances. "acroclass.pm" provides a way,
# through using "acrobase.txt" and an optional "acrolocl.txt" file, to
# expand all-caps and/or numbers terms like RPM to "revolutions per minute"
# using the HTML <abbr> tag pair. There are various options you can set.
# These are demonstrated in the code below.

use strict;
use warnings;

use acroclass;
use utf8;

my $ret;
my $err;
my $nfl;

# In the following test string:
# -----------------------------
# FOO, BLEEP and C1 are ignored terms
# 123 is a pure numeric term
# BAR will result in a "not found"
# GHZ is a translated term: ends up as "GHz"
# R1 is a single definition component
# VR23 is a multiple definition component
# DF21 is an undefined, component-style term, which will be "not found"
# BS is a multiple definition term
# --------------------------------
my $utext = "What the 73 CAM FOO BAR BLEEP is going on with <blockquote>the XTAL1 GHZ</blockquote> into R1 and C1 at VR23 in DF13? What is this BS? Do you use OSX?\n";
# --------------------------------

# Basic setup:
# ------------
my $cvt = new acroclass;	# instantiate class

my $version = $cvt->getversion();
print "Version $version\n";

# You can set a prefix and/or postfix to go in the <abbr> tag that makes it
# clear that the <abbr> is coming from a particular source, such as
# soylentnews.org. Bytram has expressed a concern with the reader knowing
# the difference between an <abbr> in the original source, and an <abbr>
# that is added by this system. This allows constant identifying verbiage
# to be stuffed into every one of the generated <abbr> tags title element
# so as to address that specific concern. The default is no prefix or
# postfix. You can set the detectquotes flag (this turns edit marks on and
# off ONLY within the scope of <blockquote> and </blockquote>) All of these
# must be set before loadstandard() and loadlocal() are called. You add a
# prefix and/or postfix this way:
# ---------------------------------------------------------------------
$cvt->setntag('Ed:[');		# prefix markup
$cvt->setmtag(']');			# postfix markup
$cvt->setdetectquotes(1);	# markup only in quotes: [0]/1 = [no]/yes
# ---------------------------------------------------------------------
# To recap: (1) If you want editor's marks everywhere, just set them.
#           (2) If you just want them in blockquotes, set them AND
#               call setdetectquotes(1)

# You can call setstandardfile('filename') here to load other than acrobase.txt
$cvt->loadstandard();		# get acros from standard list or from other file
# You can call $cvt->setworry(1); here if you want errors if acrolocl.txt is not found
# You can call $cvt->setlocalfile('filename') here to load other than acrolocl.txt


# In the line below, the [] indicate the default state.
# The call as shown here is 100% redundant because of the default.
# But you can change it to pass one to see what happens.
# -------------------------------------------------------------------
$cvt->setworry(0);			# throw error if acrolocl.txt not found: [0]/1 = [no]/yes
$cvt->loadlocal();			# get local acro list (fails quietly if worry not 1)

# You can optionally pass a list of terms to ignore. If a term
# is in the ignore list, it won't be flagged as not found, and
# it won't be looked up:
# ------------------------------------------------------------
my @ignore = ('FOO','BLEEP','C1'); # an array of terms to ignore
# the following is optional; if not done, or array is empty, nothing ignored
$cvt->setiglist(\@ignore);

# In the two lines below, the [] indicate the default state.
# The calls as shown here are 100% redundant because of the defaults.
# but you can change them to pass zero to see what happens.
# -------------------------------------------------------------------
$cvt->setdetectterms(1);	# detect all terms: 0/[1]=no/[yes]
$cvt->setdetectcomps(1);	# detect electronic components: 0/[1]=no/[yes]

# You can tell the class to ignore pure numeric terms; But numbers
# are a special case even when detectable in that if a numeric
# term is not found, it will NOT be included in the "not found"
# list, as numbers are almost always not imbued with special
# meanings, so it isn't a great idea to freak out every time
# one can't be expanded. The following is redundant, it defaults
# to detecting them:
# --------------------------------------------------------------
$cvt->setdetectnums(1);		# detect numeric terms 0/[1]=no[yes]

# $ret = processed text
# $err = a text block possibly containing processing errors
# $nfl = CAPs sequences that were not found
# ---------------------------------------------------------
($ret,$err,$nfl) = $cvt->u2u($utext); # here's the meat of it

print "$ret\n";

# If there are errors, you can do something with them.
# It's just a string of various complaints. Although
# hopefully empty. :)
# ---------------------------------------------------
if ($err ne '')
{
	print "errors:\n$err"
}

# Lastly, if terms were ID'd but not in the terms file and
# not specified in the ignore list, they'll show up here:
# --------------------------------------------------------
foreach (@$nfl)
{
	print "not found::: $_\n";
}

exit();
