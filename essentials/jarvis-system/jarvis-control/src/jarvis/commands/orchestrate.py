#!/usr/bin/python

import json
import urllib2

ORCHESTRATOR_PROTOCOL = 'http'
#ORCHESTRATOR_HOST = '119.74.248.86'
ORCHESTRATOR_HOST = '192.168.1.11'
ORCHESTRATOR_PORT = '8080'
ORCHESTRATOR_PATH = '/jarvis/orchestrator/v1?query=%s'

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
	print 'Let me try to %s for you...' % task
	request_url = (ORCHESTRATOR_PROTOCOL + '://' + ORCHESTRATOR_HOST +':' + ORCHESTRATOR_PORT + ORCHESTRATOR_PATH) % urllib2.quote(task)
	response = urllib2.urlopen(request_url)
	response_data = json.load(response)
	print response_data