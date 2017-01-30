#!/usr/bin/python

import sys
import importlib
import argparse
from commands import *

def handle_command(args):
	command = None
	# look for command module in commands directory
	try:
		# causes exception in development due to module path issues
		command = importlib.import_module('jarvis.commands.' + args[0])
	except ImportError as e:
		print e
		try:
			# does not work in distributable
			command = importlib.import_module('.' + args[0], 'commands')
		except ImportError as e:
			print e
			# the module for the command does not exist
			print '\'' + args[0] + '\' command not found' 
	
	if command is not None:
		command_module_name = command.__name__
		command_module_name_arr = command_module_name.split('.')
		command_name = command_module_name_arr[len(command_module_name_arr) - 1]
		parser = argparse.ArgumentParser('jarvis %s' % command_name)
		if hasattr(command, 'available_arguments'):
			for argument in command.available_arguments():
				if argument.has_key('flags'):
					positional_argument = argument['flags']
					del(argument['flags'])
					parser.add_argument(*positional_argument, **argument)
				else:
					parser.add_argument(**argument)
		args = parser.parse_args(args[1:])
		command.run(args)
	return 0;
	
def main():
	handle_command(sys.argv[1:])
	
if __name__ == '__main__':
	main()