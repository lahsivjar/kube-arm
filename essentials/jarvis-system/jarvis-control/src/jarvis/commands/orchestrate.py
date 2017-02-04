#!/usr/bin/python

import json
import urllib2

from .. import config

def available_arguments():
	return [
		{
			'metavar': 'task',
			'dest': 'task',
			'help': 'Task to do',
			'nargs': '*'
		}
	]

def run(args):
	task = ' '.join(args.task)
	request_url = '%s://%s:%s/%s' % (
		config.get_config('orchestrator.protocol'),
		config.get_config('orchestrator.host'),
		config.get_config('orchestrator.port'),
		(config.get_config('orchestrator.query_path') % urllib2.quote(task))
	)
	response = urllib2.urlopen(request_url)
	response_data = json.load(response)
	print response_data