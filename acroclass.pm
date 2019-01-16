package acroclass;

use strict;
use warnings;

# Note: set tabs = 4 spaces in editor, or insanity results
# ========================================================

sub new
{
	my $self = {errors=>'',
				acros=>{},
				igdic=>{},
				undic=>{},
				codic=>{},
				nflst=>[],
				standardfile=>'acrobase.txt',
				localfile=>'acrolocl.txt',
				worry=>0,
				detectcomps=>1,
				detectterms=>1,
				detectnums=>1
				};

	bless $self;
	return $self;

	sub rpterr
	{
		my $self = shift;
		my $err = shift;
		$self->{errors} = $self->{errors} . $err . "\n";
	}

	sub loadstandard
	{
		my $self = shift;
		my $fn;
		my $rv;

		# go grab the term expansions
		# ---------------------------
		$fn = $self->{standardfile};
		if (loadacros($self,$fn))	# try to get standard file, always worry
		{
			rpterr($self,"Could not open \"$fn\"");
		}
	}

	sub loadlocal
	{
		my $self = shift;
		my $fn;
		my $rv;
		$fn = $self->{localfile};
		$rv = loadacros($self,$fn);			# try to get optional local file
		if ($self->{worry})
		{
			if ($rv)
			{
				rpterr($self,"Could not open \"$fn\"");
			}
		}
	}

	sub loadacros
	{
		my $self = shift;
		my $fn = shift;
		my $row;	# rows of text in the acro file
		my $term;	# term to be expanded
		my $mdef;	# possible multiple definition of term
		my $fh;		# filehandle
		my $rc; 	# row count
		my @ray;	# splitter for current line

		if (open($fh,$fn))
		{
			$rc = 0;
			while($row = <$fh>)
			{
				$rc += 1;
				chomp $row;
				if ($row ne '')						# ignore blank lines
				{
					if (substr($row,0,1) ne '#')	# ignore comments
					{
						@ray = split(/,/, $row, 3);
						if (scalar(@ray) == 3)
						{
							if ($ray[0] eq '*')	# look for components
							{	# expansion into designator dictionary:
								$self->{codic}{$ray[1]} = $ray[2];
							}
							else # not a component, normal term
							{
								$term = $ray[0];
								if ($ray[1] ne '')	# substitutions
								{
									$term = $ray[1];
								}
								$mdef = multidef($ray[2]);
								$term = "<abbr title=\"$mdef\">$term</abbr>";
								$self->{acros}{$ray[0]} = $term;
							}
						}
						else # split was not three
						{
							rpterr($self,"line $rc failed to split into 3 components in $fn");
						}
					}
				}
			}
			close($fh);
			return(0); # all good
		}
		return(1); # oops
	}

	sub setworry
	{
		my $self = shift;			# class hash
		my $worry = shift;			# should we worry about localfile?
		$self->{worry} = $worry;	# set it for later
	}

	sub setstandardfile
	{
		my $self = shift;				# class hash
		my $fn = shift;					# passed filename
		$self->{standardfile} = $fn;	# setter
	}

	sub setlocalfile
	{
		my $self = shift;			# class hash
		my $fn = shift;				# passed filename
		$self->{localfile} = $fn;	# setter
	}

	sub multidef
	{
		my $text = shift;
		my @ray;
		my $len;
		my $count;
		my $item;
		my $o = '';
		@ray = split(/\|/, $text);
		$len = scalar(@ray);
		if ($len == 1)	{ return($text);	} # nothing to do
		$count = 0;
		while(@ray)
		{
			if ($count != 0)	{	$o = $o . " ";	} # intersticials
			$count += 1;
			$item = pop(@ray);
			$o = $o . "($count): $item";
		}
		return($o);
	}

	sub multicomp
	{
		my $text = shift;
		my $num = shift;
		my $des = shift;
		my @ray;
		my $len;
		my $count;
		my $item;
		my $o = '';
		@ray = split(/\|/, $text);
		$len = scalar(@ray);
		if ($len == 1)	{ return("<abbr title=\"$text $num\">$des</abbr>");	} # nothing to do
		$count = 0;
		$o = "<abbr title=\"";
		while(@ray)
		{
			if ($count != 0)	{	$o = $o . " ";	} # intersticials
			$count += 1;
			$item = pop(@ray);
			$o = $o . "($count): $item $num";
		}
		$o = $o . "\">$des</abbr>";
		return($o);
	}

	sub setdetectcomps
	{
		my $self = shift;
		my $flag = shift;
		$self->{detectcomps} = $flag;
	}

	sub setdetectterms
	{
		my $self = shift;
		my $flag = shift;
		$self->{detectterms} = $flag;
	}

	sub setdetectnums
	{
		my $self = shift;
		my $flag = shift;
		$self->{detectnums} = $flag;
	}

	sub setiglist
	{
		my $self = shift;	# self
		my @list = @{$_[0]};
		foreach(@list)
		{
			$self->{igdic}{$_} = 1;
		}
	}

	sub chkhtmlbalance
	{
		my $text = shift;	# passed text
		my $bal = 0;
		my $char;
		foreach $char (split //, $text)
		{
			if ($char eq "<")		{	$bal += 1;	}
			elsif ($char eq ">")	{	$bal -= 1;	}
		}
		return($bal);
	}

	sub isdigits
	{
		my $text = shift;
		my $c;
		foreach $c (split //, $text)
		{
			if ($c ge '9' or $c le '0')
			{
				return(0);
			}
		}
		return(1);
	}

	sub compmatch
	{
		my $self = shift;
		my $text = shift;
		my $num;
		my $term;
		if ($self->{detectcomps} == 0) {	return($text);	}	# comps off?
		if (!exists($self->{igdic}{$text}))	# we might need to ignore this
		{
			# Okay, we're up: let's see if this looks like a component
			# The regex produces two groups, the letters ($1) and numbers ($2)
			# ----------------------------------------------------------------
			if ($text =~ /([A-Z]+)(\d+)/ ) # if (regex matches)
			{
				if (exists($self->{codic}{$1}))			# if letters in comps dict
				{
					$term = $self->{codic}{$1};			# get term from comps dict
					$text = multicomp($term,$2,$text);	# build comp or multicomp
				}
			}
		}
		return("$text");
	}

	sub isnum
	{
		my $text = shift;
		my $char;
		foreach $char (split //, $text)
		{
			if ($char lt "0")		{	return(0);	}
			elsif ($char gt "9")	{	return(0);	}
		}
		return(1);
	}

	sub u2u
	{
		my $self = shift;	# self
		my $text = shift;	# passed text
		my $o = "";			# accumulated output
		my $incaps = 0;		# not in caps at start
		my $wait = 0;		# not holding off expansion at start
		my $wait2 = 0;		# not holding off expansion at start
		my $ctag = '';		# 
		my $accum = '';		# accumulator
		my $taccum = '';	# temp accumulator
		my $char;
		my $key;
		my $go;				# flag to control number hits
		my @keys=();

		if ($self->{detectterms} == 0) {	return($text);	} # function disabled
		if (chkhtmlbalance($text) != 0)
		{
			rpterr($self,'&lt;&gt; unbalanced');
			return($text,$self->{errors},$self->{nflist});
		}

		foreach $char (split //, $text)
		{
			if ($char eq "<")
			{
				$wait = 1;	# noop within HTML tags
				$ctag = '';	# reset abbr detector
			}
			elsif ($char eq ">")
			{
				$wait = 0; # out of html tag, presumably
			}
			$ctag = $ctag . lc($char);
			if ($ctag eq '<abbr')
			{
				$wait2 = 0;
				$ctag = "";
			}
			elsif ($ctag eq '</abbr')
			{
				$wait2 = 0;
				$ctag = '';
			}
			if ($wait==0 && $wait2==0 &&			# not in HTML tag or <abbr> scope
				(($char ge 'A' && $char le 'Z') ||	# char is cap alpha or...
				 ($char ge '0' && $char le '9')))	# ...char is numeric
			{
				$accum = $accum . $char;
			}
			else	# not a cap or number or else out of scope
			{
				if (length($accum) > 1)
				{
					$go = 1;
					if (!$self->{detectnums}) # if excluding numbers
					{
						if (isnum($accum))	# watch for pure numbers
						{
							$go = 0;
						}
					}
					if (exists($self->{acros}{$accum})) # is this defined?
					{
						if ($go)
						{
							$taccum = $self->{acros}{$accum}; # then grab it
						}
						else # it's a number and we're ignoring it
						{
							$taccum = $accum;
						}
					}
					else # we don't know about this one
					{
						if (isdigits($accum) == 0) # if not fully numeric
						{
							$taccum = compmatch($self,$accum); # is this a component?
							if ($taccum eq $accum) # if still not found
							{
								if ($go and !exists($self->{igdic}{$accum})) # in ignore dict?
								{
									$self->{undic}{$accum} = 1; # whoops... don't know this one
								}
							}
						}
					}
					$accum = $taccum;
					$o = $o . $taccum;
					$o = $o . $char;
					$accum = '';
					$taccum = '';
				}
				else	# length 1 or zero, ignore so far
				{
					$o = $o . $accum;
					$o = $o . $char;
					$accum = '';
				}
			}
		}
		@keys = keys $self->{undic};
		while(@keys) # throw errors about items not found
		{
			$char = pop(@keys); # reusing $char here for unfound terms
			push @{$self->{nflst}},$char;
		}
		return($o,$self->{errors},$self->{nflst});
	}
}

1;
