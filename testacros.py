#!/usr/bin/python

afile = 'acrobase.txt'

errors = ''

try:
	with open(afile) as fh:
		text = fh.read()
except:
	print 'failed to read ' + afile
	exit()

di = {}
data = text.split('\n')
ln = 1
for line in data:
	if line != '' and line[0] != '#':
		try:
			key,replacement,expansion = line.split(',',2)
		except:
			errors += 'line %d failed to split into three components\n' % (ln)
		else:
			if expansion.find('<') != -1: errors += 'expansion of key '+key+' contains "<"\n'
			if expansion.find('>') != -1: errors += 'expansion of key '+key+' contains "<"\n'
			if replacement.find('<') != -1: errors += 'expansion of key '+key+' contains "<"\n'
			if replacement.find('>') != -1: errors += 'expansion of key '+key+' contains "<"\n'
			if expansion == '': errors += 'expansion of key '+key+' is empty\n'
			if key == '':
				errors += 'key is empty at line %d\n' % (ln)
			else:
				di[key] = expansion
	ln += 1

keys = di.keys()
keys.sort()
if errors != '':
	print errors
else:
	print afile + ' passed all tests'
print '%d acronyms found' % (len(keys))