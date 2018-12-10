# soyacro.py - making better posts on soylentnews.org

We're deluged by acronyms and abbreviations, quite often in the form of
all-caps terms. Even though I'm technically oriented and have been around
social networks for quite some time, I see such terms I don't know \(or
remember\) constantly. If it's happening to me, it's happening to others.
While I can't fix my own failure to recognize, I can fix those I use in
my posts so that others can learn about them easily, without otherwise
clogging up the post text with explanations.

So what this project does is provides built-in definitions of terms
written in all-capital letters and/or numeric digits used in posts \(as
long as they're in the expansion file, `acrobase.txt`.\) You can edit the
`acrobase.txt` file and add terms, and you should, as you find yourself
using them. You might keep an eye on the one in the project, as I seem to
be adding to it regularly. Better yet, submit your additions here as a
pull request, and we all win. Here's the format for a line to do that, where
[] indicates optional:

> term,[replacement],expansion[;expansion]

You can produce output that is comprised more than just all-caps and/or
numbers by using the second field, the optional replacement. The only
restrictions are that there can be no actual commas in the replacement
\(you can use &amp;#44; if you need a comma, just not an actual
comma character\), and that there be no non-ASCII characters. So, for
instance, this line in the `acrobase.txt` file...

> `TLDR,TL;DR:,Too Long, Didn't Read`

...sets things up so that when you enter TLDR in your post source, the
output post will contain the string `TL;DR:` instead, which corresponds
with the actual common usage.

There is also a built-in macro processor that lets you build shortcuts
for anything, signatures, etc., so you can make richer posts more easily.

### But what if I _need_ non-ASCII characters in a replacement field?

Then you can use HTML entities. For instance, El ni&#241;o can be
represented by `El ni&#241;o`. Simple as that. You can write the same
thing in the replacement field:

> `ENSO,,El Ni&#241;o/Southern Oscillation`

### Contributions:

I would particularly appreciate any pull requests that enhance the
acronym file. Anything that is reasonable will be merged. Code PRs
will be carefully checked and if suitable, I will happily accept
those as well.

## Requirements / Installation:

This is a CGI web application, so it needs to run on a webserver such as
Apache. Put all the files into a directory where **Python** cgi applications
\(denoted by files that end in `.py`\) are allowed to run, then
simply access the application with:

> `http://yourserver.tld/cgi-path/soyacro.py`

## Setup

You can use the `ifile` and `mfile` variables at the top of the
`soyacro.py` code to change the name of the acronym and style files. If
you're running only on your own LAN, not much to worry about there. But
if the web page is on a server with WAN access, I recommend renaming both
so as to prevent snoooping, etc. I also suggest you rename the main cgi
and set the `cginame` variable to match.

At the top of the `soyacro.py` file, there are settings you can change to
control the number of lines in the entry and result text boxes, and to
switch on or off various displays of other information relevant to what
you're doing. You can also set up automatic random signatures. See the
section on signatures below for more details.

### More on Security:

This application is something specifically intended for use by the person
who has access to the definition files, which will almost certainly be
the owner of the server permissions. I highly recommend that you do _not_
hand out the URL to this web application, as I wrote it for the use of a
benign user.

On a WAN or untrusted LAN? I've provided a means for
security-by-obscurity, in that you can rename any of the data files \(and
you should do so\) to anything you like, preferably something very
unlikely, so as to prevent anyone from stumbling upon the cgi.

In such a case, you should also rename the main processor. To do this,
you need to change the `cginame` variable at the top of the file to match
the new filename.

You should also set your permissions carefully. There's no cause for the
app to write to the folder it or the data files are in, so the folder
should be read-only except by very high priviledge users. The app itself
and the two data files should also be read-only to anyone but high
priviledge users.

Personally, I run this on a webserver inside my LAN, which has no
external means of access and to which no one else has any access, so I'm
not particularly worried about anyone else using it. The above remarks
are more meant for those who only have a public webserver to place this
on, or who have untrusted users on their LAN \(why?\)

## Use:

When you write your post on this page, if you use a known term it'll be
wrapped with HTML `<abbr>` tags and will include an expansion visible
when one hovers a mouse pointer in a web browser.

The result is generated into the lower text box when you press `submit`.

Copy the result and paste it into the soylentnews.org comment box \(or
any other commenting system that allows the `<abbr>` tag.\)

## Files

File | Purpose
---- | -------
`soyacro.py` | the webserver cgi
`aa_webpage.py` | convenience for generating HTML 4.01 pages
`aa_macro.py` | macro processor [docs here](http://ourtimelines.com/aamacrodoc/general.html)
`aambase.txt` | macro definitions [docs here](http://ourtimelines.com/aamacrodoc/general.html)
`acrobase.txt` | term definitions \(see below\)
`testacros.py` | Tests `acrobase.txt` file to assure proper operation with `soyacro.py`
`testfile.uco` | Test comparison file for running `soyacro.py` from the command line
`check.py` | Quick checker to see if a term is in `acrobase.txt`

## `acrobase.txt`:

The format is defined at the top of the file. Basically there are three
comma-separated fields. **Important:** _Don't use HTML in these fields._

The first field is the caps-and/or-number sequence that is the term,
such as `TIL`, `3D`, or `MHZ`.

The second field is a replacement field that is only used if the all-caps
sequence isn't exactly how the term should be presented. So for `MHZ`,
this field contains `MHz`, which is the correct way to write the term.
For acronymns that are all-caps, this field remains empty.

The third field is the expansion that is presented when the mouse is
hovered over the term \(or its replacement\) in the post.

This file must contain only ASCII characters; no unicode. You can use
HTML entities in the replacement and expansion fields instead, though, so
there's no limit on the accuracy of the results, only on the all-caps
sequences used to trigger them, and those don't show up in the posts
except where there is no replacement field content.

### Examples:

> `3D,,Three Dimensional`  
> `411,,A number, and a shorthand for: Information`  
> `MHZ,MHz,Megahertz - Millions of cycles per second`  
> `NASA,,National Aeronautics and Space Administration (US)`  

### Working with `acrobase.txt`

#### Adding new expansions

Edit the `acrobase.txt` file with a text editor. Stick to the format
described at the top of the file. ASCII only, no unicode. Square
braces mean optional:

> TERM,[replacement],Expansion(s)

#### Checking `acrobase.txt` for correctness

Run `testacros.py` - it will tell you if there are any problems,
and where they are in the file.

#### Checking to see if an expansion is already present

Run `check.py` with the term(s) you want to check for...

> `./check.py MHZ THZ`

...If the term or terms are found in the file, you'll see confirmation of
that. If not, you'll be informed as to what is missing.

Once `check.py` is running, it will keep running until you press `return`
without providing a term to search for.

## `aambase.txt`:

This contains macros you can use in your posts. The macro language,
[aa_macro](http://ourtimelines.com/aamacrodoc/general.html), is very
capable, and if you'd like to go further,
[the documentation](http://ourtimelines.com/aamacrodoc/general.html)
awaits. You can use HTML in the macros, but you must use only ASCII; no
unicode. The macro system, in the context of this application, will
process unicode symbols, but the macros themselves cannot be written in
unicode. If you desperately need a unicode character in a macro used
here, then write it as an HTML numeric entity, such as `&#128169;`
(that's the "poop" emoji.) Here's an example of that...

> `[style poophead [b] is a &#128169;-head.]`

...which you would use this way: {poophead fyngyrz}

As to HTML in general, here's a macro that produces a link to my iToolBox
project as a simple example:

_Macro:_

> `[style itoolbox <a target="_blank" href="http://ourtimelines.com/itdoc/intro.html">iToolBox</a>]`

_Usage:_

> `{itoolbox}`

_Result:_

> `<a target="_blank" href="http://ourtimelines.com/itdoc/intro.html">iToolBox</a>`

### Examples:

> `[style b <b>[b]</b>]`  
> `[style i <i>[b]</i>]`  
> `[style strike <strike>[b]</strike>]`  
> `[style bq <blockquote>[b]</blockquote>]`  

### More about styles

Specifically in the context of this application, `[style]` \(page-local
styles\) and `[gstyle]` \(global styles\) perform exactly the same
function, because the global context for the macro processor is the same
as the local one: there's only one "page" being processed by the
webapp.

However, since the global styles and the local styles are kept in
separate lists, the application uses the local list to display available
styles, which effectively hides the global styles from the list at the
bottom of the page. The end result is that you can create styles that
don't clog up the page with things you're not planning to use directly.

I demonstrate this with the signature generator \(`{sig}`\) style. You'd
use that, but not any of the lower-level styles that it calls upon, so
those are implemented with `[gstyle]` instead of `[style]`, consequently
you don't see them listed on the web page.

### Using the Macros:

_This macro in the `aambase.txt` file:_

> [style i <i>[b]</i>]

_Used in a post as follows:_

> `Italizing for emphasis, I {i really} mean it!`

_Produces:_

> `Italizing for emphasis, I <i>really</i> mean it!`

### The Signature Generator

I've included three macros for your signing pleasure. soylentnews.org
allows you to have one short, fixed string for your signature. This can
be limiting. You can clear out your signature setting on soylentnews.org,
and use the signature generator macro instead.

There's a list named `sigs` towards the end of  the `aambase.txt` file.
This contains a list of various signatures, separated by the `|` (pipe)
character. I've populated it with placholders like `Signature 1`, where
the intent is that you replace those placeholders with clever signature
lines of your own. You can have as many (or as few) as you want. Just
follow the formatting shown: a newline, a `|` \(pipe character\), and
a signature. Signatures can be more than one line; just don't use the
pipe on the 2nd and following lines for that particular signature. The
pipe marks the _beginning_ of the next signature.

Simply placing `{sig}` at the end of your message will generate a
**random** signature from that list every time you hit `[Submit]` on
the webpage.

You can even make this automatic; just set the `randsigs` variable near
the top of the `soyacro.py` file to `True`. The default is `False`,
because the sigs list is initially populated with demo placeholders which
have no value in an actual post.

You can also select specific signatures with `{nsig N}`, where `N` is the
number of the signature you want, from 1-N. Considering that you may add
to the list, you can't count on the number remaining the same, so there's
a web page display option that allows you to see your current list of
signatures, numbered to match the usage in the `{nsig N}` macro. This
defaults to on.

There is also an `{lsigs}` macro, which will list, and number, every
signature for you right in the generated output. So use that once, look
for the one you want, and then use the number in front of it.

Suppose the signature you want is number 10 in the `{lsigs}` result. Just
write `{nsig 10}` and that's the signature that will be used. Easy. Fun!
_Improved!_

### Squiggly braces are special, because of macro processing

If macro processing is on, you need to be mindful about using `{` and `}`
as these are used to invoke macros. If you want to use them as characters
in a post, just use `{ls}` for the left squiggly brace, and `{rs}` for the
right squiggly brace. **If there are unbalanced squiggly braces in the text,
macro processing is cancelled.**

### Angle braces are special too, because of HTML

Angle braces need to be balanced because of how HTML tags are processed
\(not just by the app, but also by the HTML browser.\) If you need to use
an angle brace in text, use the usual HTML escapes, which are
`&lt;` for the less-than brace, and `&gt;` for the greater-than brace.

If angle braces are unbalanced, the app will warn you.

## The Python files

`soyacro.py` is the cgi you access on your webserver. You might put it in
a cgi-bin folder, along with the other two **Python** files, and then get to
it with `http://mysite.com/cgi-bin/soyacro.py`

Please do observe the ruminations at the top of this readme about security.

## Limitations and Design Choices

This is a **Python** project. It incorporates another **Python** project,
[aa_macro](http://ourtimelines.com/aamacrodoc/general.html), and until
or unless I move that project to **Python3** \(not very likely, but someone
else might undertake that\), **Python** will remain the target here.

Having said all that, by all means feel free to fork and go your own way
with either / both projects. The Github repo for the macro processor is
[here](https://github.com/fyngyrz/aa_macro).

## License

You can use this any way you want. It's 100% free and unencumbered by any
rights claims whatsoever, released into the public domain. It is original
code written by me, and any claims otherwise should be heartily laughed
at and otherwise ignored. Stop feeding the lawyers. Also, if your country
doesn't allow for public domain release by authors, you should get to
work fixing that right away. It's your country, you broke it, you get to
fix it.

The top of the **Python** files present information about development and so
forth if you'd like to peruse that. Otherwise, don't worry about it, and
have fun.
