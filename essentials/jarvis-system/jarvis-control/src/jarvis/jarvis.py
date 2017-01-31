#!/usr/bin/python

import re
import sys
import argparse
import importlib
from commands import *

DEBUG = False

def command_list():
	return [('deploy', 'Deploy a jarvis kube module'),
			('version', 'Display jarvis version')]

def handle_command(args):
	command = get_command_module(args[0])
	if command is not None:
		parser = argparse.ArgumentParser('jarvis %s' % args[0])
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
	else:
		print '%s: command not found' % args[0]
	return 0;
	
def handle_orchestrator_task(args):
	print args
	
def get_command_module(command_name):
	# look for command module in commands directory
	try:
		# causes exception in development due to module path issues
		return importlib.import_module('jarvis.commands.%s' % command_name)
	except ImportError as e:
		if DEBUG: print e
		try:
			# does not work in distributable
			return importlib.import_module('.%s' % command_name, 'commands')
		except ImportError as e:
			if DEBUG: print e
			# the module for the command does not exist
			return None
			
def print_help(parser):
	parser.print_help()
	print
	print_command_list()
			
def print_command_list():
	commands = command_list()
	print 'Jarvis control commands:'
	print '------------------------'
	print "\n".join(['  %-18s %-80s' % (command[0], command[1]) for command in commands])
	
def create_jarvis_parser():
	parser = argparse.ArgumentParser('jarvis', add_help=False)
	parser.add_argument(
		'command', 
		help='Jarvis control command or task for the orchestrator with \
		orchestrate option(-o) enabled',
		nargs = '*')
	parser.add_argument(
		'-h', '--help',
		dest='help',
		help='Show this help message',
		action='store_true')
	parser.add_argument(
		'-o', '--orchestrate',
		dest='handler',
		help='Provide task for the orchestrator (Default: Provide jarvis \
		control command)',
		required=False,
		default=handle_command,
		const=handle_orchestrator_task,
		action='store_const')
	return parser

def main():
	parser = create_jarvis_parser()
	args = parser.parse_args(sys.argv[1:])
	if args.help and len(args.command) == 0:
		print_help(parser)
	elif not args.help and len(args.command) == 0: 
		print 'What can I do for you?'
	else: args.handler(sys.argv[1:])
	return 0
		
if __name__ == '__main__':
	main()