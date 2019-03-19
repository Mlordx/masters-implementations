#!/usr/bin/env python

import sys
import time
import os.path
import geocomp
from geocomp import config
from geocomp.gui import dummy

def get_func (strTemp):

	listTemp = strTemp.split('/')
	if listTemp[0] == 'geocomp':
		listTemp.pop (0)

	last = listTemp.pop ()
	ext = last.rfind ('.py', -4)
	#ext = rfind (last, '.py', -4)
	if ext != -1: 
		last = last[:ext]

	mod = geocomp
	for name in listTemp:
		mod = getattr (mod, name)

	tempTuple = (list(filter (lambda x, last=last: x[0] == last, mod.children)))[0]

	if tempTuple[1] == None: return None

	mod = getattr (mod, last)
	func = getattr (mod, tempTuple[1])

	return func

def run_alg (func, localInput):
	init = time.clock ()
	cont, extra = geocomp.run_algorithm (func, localInput)
	end = time.clock ()

	delta = end - init

	print(repr(cont), '  ','%.2f'%delta,'s', '  ', extra)
	sys.stdout.flush ()

def many_algs (strings):
	filename = strings.pop (0)
	print(filename, ':')
	lInput = geocomp.open_file (filename)

	for func_name in strings:
		print(os.path.basename (func_name),':', end=' ')
		func = get_func (func_name)

		run_alg (func, lInput)

def many_files (strings):
	func_name = strings.pop (0)
	print(func_name,':')
	func = get_func (func_name)

	for filename in strings:
		print(os.path.basename (filename),':', end=' ')
		lInput = geocomp.open_file (filename)

		run_alg (func, lInput)


if __name__ == '__main__':
	if len (sys.argv) < 2:
		print(sys.argv[0], '<algorithm> <file1> [file2]...')
		print(sys.argv[0], '-a <file1> <algorithm1> [algorithm2]...')
		sys.exit (1)

	geocomp.init_display (dummy, None)

	if sys.argv[1] == '-a':
		sys.argv.pop (0)
		sys.argv.pop (0)
		many_algs (sys.argv)
	else: 
		sys.argv.pop (0)
		many_files (sys.argv)


