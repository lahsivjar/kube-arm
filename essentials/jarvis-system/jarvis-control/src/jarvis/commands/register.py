#!/usr/bin/python

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
		print 'Registering module'
		registry_info = util.convert_yaml_to_object(registry_file_path)
		request_url = '%s://%s:%s/%s' % (
			config.get_config('orchestrator.protocol'),
			config.get_config('orchestrator.host'),
			config.get_config('orchestrator.port'),
			config.get_config('orchestrator.register_path')
		)
		req = urllib2.Request(request_url, json.dumps(registry_info), {'Content-Type': 'application/json'})
		response = urllib2.urlopen(req)
		response_data = json.load(response)
		if response_data:
			print 'Module registered'
		else:
			print 'Module registration failed'