#!/usr/bin/python

import json
import urllib2

from .. import util
from .. import config

def available_arguments():
	return [
		{
			'metavar' : 'registry_file_url',
			'dest' : 'registry_file_url',
			'help' : 'Registry file of the module'
		}
	]

def run(args, work_dir):

	registry_file_url = args.registry_file_url
	registry_file_path = ''.join([work_dir, '/registry.yaml'])
	if not util.retrieve_file(registry_file_url, registry_file_path):
		print 'Resource not found'
		return 1

	register(registry_file_path)

def register(registry_file_path):
	if registry_file_path is not None:
		registry_info = util.convert_yaml_to_object(registry_file_path)
		print 'Registering module %s' % registry_info['service_name']

		request_url = '%s://%s:%s/%s' % (
			config.get_config('orchestrator.protocol'),
			config.get_config('orchestrator.host'),
			config.get_config('orchestrator.port'),
			config.get_config('orchestrator.register_path')
		)
		req = urllib2.Request(request_url, json.dumps(registry_info), {'Content-Type': 'application/json'})
		try:
			response = urllib2.urlopen(req)
			response_data = json.load(response)
			if response_data:
				print 'Module registered'
			else:
				print 'Module registration failed'
		except urllib2.HTTPError as e:
			if e.code == 404:
				print 'Orchestrator not found'
			else:
				raise e
