#!/usr/bin/python

config = {
	'orchestrator' : {
		'protocol' : 'http',
		'host' : '119.74.248.86',
		'port' : '8080',
		'register_path' : 'jarvis/orchestrator/v1/service/register',
		'query_path' : 'jarvis/orchestrator/v1/search?query=%s'
	},

	'tmp_working_dir' : '/tmp',

	'deploy' : {
		'default' : {
			'repo' : 'https://github.com/lahsivjar/jarvis-kube-modules.git',
			'branch' : 'master',
			'module_path' : '',
			'should_register' : False,

			'deployment_yaml_path' : 'deployment/deployment.yaml',
			'service_yaml_path' : 'deployment/service.yaml',
			'ingress_yaml_path' : 'deployment/ingress.yaml'
		}
	},

	'register' : {
		'default' : {
			'registry_yaml_path' : 'deployment/registry.yaml'
		}
	}
}

DEFAULT_BRANCH = 'master'
DEFAULT_MODULE_PATH = ''
DEFAULT_SHOULD_REGISTER = False

def get_config(config_name):
	config_keys = config_name.split('.')
	config_value = config
	try:
		for config_key in config_keys:
			config_value = config_value[config_key]
		return config_value
	except KeyError as e:
		raise KeyError(config_name)
