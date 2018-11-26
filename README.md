# soyacro.py - making better posts on soylentnews.org

We're deluged by acronyms and abbreviations. Even though I'm technically
oriented and have been around social networks for quite some time, I see
acronyms and abbreviations I don't know \(or remember\) constantly. If
it's happening to me, it's happening to others. While I can't fix my own
failure to recognize, I can fix the acronyms I use in my posts so that
others can learn about them easily, without otherwise clogging up the
post text with explanations.

So what this project does is provides built-in definitions of acronyms
used in posts \(as long as they're in the acronym file, `acrobase.txt`.\)
You can edit the `acrobase.txt` file and add acronyms, and you should, as
you find yourself using them.

In addition, there's a built-in macro processor that lets you build
shortcuts for anything, signatures, etc., so you can make richer posts
more easily.

## Requirements / Installation:

This is a CGI web application, so it needs to run on a webserver such as
Apache. Put all the files into a directory where python cgi applications
\(denoted by files that end in `.py`\) are allowed to run, then
simple access the application with:

`http://yourserver.tld/cgi-path/soyacro.py`

## Security:

This application is something specifically intended for use by the person
who has access to the definition files, which will almost certainly be
the owner of the server permissions. I highly recommend that you do _not_
hand out the URL to this web application, as I wrote it for the use of a
benign user. I've provided a means for security-by-obscurity, in that you
can rename any of the files \(and you should do so\) to anything you
like, preferably something very unlikely, so as to prevent anyone from
stumbling upon the cgi.

## Use:

When you write your post on this page, if you use an acronym (defined as
an caps-and/or-numbers sequence), it'll be wrapped with HTML `<abbr>`
tags and will include an expansion visible when one hovers a mouse
pointer in a web browser.

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
`acrobase.txt` | acronym definitions \(see below\)

## `acrobase.txt`:

The format is defined at the top of the file. Basically there are three
comma-separated fields. *Don't use HTML in these fields.*

The first field is the caps-and/or-number sequence that is the acronym,
such as `TIL`, `3D`, or `MHZ`.

The second field is a replacement field that is only used if the all-caps
sequence isn't exactly how the term should be presented. So for `MHZ`,
this field contains `MHz`, which is the correct way to write it. For
acronymns that are all-caps, this field remains empty.

The third field is the content that is presented when the mouse is
hovered over the acronym in the post.

### Examples:

```
3D,,Three Dimensional
411,,A number, and a shorthand for: Information
MHZ,MHz,Megahertz - Millions of cycles per second
NASA,,National Aeronautics and Space Administration (US)
```

## `aambase.txt`:

This contains macros you can use in your posts. The macro language,
[aa_macro](http://ourtimelines.com/aamacrodoc/general.html) is _very_
capable, and if you'd like to go further, the documentation awaits. You
can use HTML in the macros. For instance, here's a macro that produces a
link to my iToolBox project:

_Macro:_

```
[style itoolbox <a target="_blank" href="http://ourtimelines.com/itdoc/intro.html">iToolBox</a>]
```

_Usage:_

```
{itoolbox}
```

_Result:_

```
<a target="_blank" href="http://ourtimelines.com/itdoc/intro.html">iToolBox</a>
```

### Examples:

```
[style b [b [b]]]
[style i [i [b]]]
[style strike <strike>[b]</strike>]
[style bq <blockquote>[b]</blockquote>]
```

### Using the Macros:

```
Italizing for emphasis, I {i really} mean it!
```

_Produces:_

```
Italizing for emphasis, I <i>really</i> mean it!
```

## The Python files

`soyacro.py` is the cgi you access on your webserver. You might put in a
cgi-bin folder, along with the other two Python files, and then get to it
with `http://mysite.com/cgi-bin/soyacro.py`, although I strongly
recommend you rename it to something else, and change the `cginame`
variable in `soyacro.py` to that name in order to provide a layer of
"security by obscurity."

Likewise, you can, and probably should, change the filenames of the
`aambase.txt` and `acrobase.txt`, and again there are variables at the
top of `soyacro.py` into which you should place the new names so it knows
how to find the files.

## License

You can use this any way you want. It's 100% free and unencumbered by any
rights claims whatsoever, released into the public domain. It is original
code written by me, and any claims otherwise should be heartily laughed
at. Stop feeding the lawyers. Also, if your country doesn't allow for
public domain release by authors, you should get to work fixing that
right away.

The top of the Python files contains information about development and so
forth if you'd like to peruse that. Otherwise, don't worry about it, and
have fun.
