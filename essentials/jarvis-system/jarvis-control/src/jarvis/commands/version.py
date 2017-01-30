#!/usr/bin/python

import pkg_resources

def run(args):
	print(pkg_resources.get_distribution('jarvis').version)