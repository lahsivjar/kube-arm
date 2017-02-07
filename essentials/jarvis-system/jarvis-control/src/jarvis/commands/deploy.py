#!/usr/bin/python

import json
import urllib2
import argparse
import register
import subprocess

from .. import util
from .. import config

def available_arguments():
	return [
		{
			'metavar': 'module-path',
			'dest': 'module_path',
			'help': 'The path of the module in the git repo',
			'nargs': '?'
		},
		{
			'flags': ('-u', '--repo-url'),
			'help': 'The git repo to clone the module from'
		},
		{
			'flags': ('-b', '--branch'),
			'help': 'The branch to pull from. Default is master.'
		},
		{
			'flags': ('-l', '--local'),
			'help': 'Deploy a local module'
		},
		{
			'flags': ('-r', '--register'),
			'help': 'Register the module after deploy',
			'default': config.get_config('deploy.default.should_register'),
			'const': True,
			'action': 'store_const',
			'required': False
		}
	]

def run(args, work_dir):
	if args.repo_url is None and args.module_path is None:
		print 'No deploy target found'
		return 1
	
	repo_url = args.repo_url if args.repo_url is not None else config.get_config('deploy.default.repo')
	branch_name = args.branch if args.branch is not None else config.get_config('deploy.default.branch')
	module_path = args.module_path if args.module_path is not None else config.get_config('deploy.default.module_path')
	should_register = args.register

	build_source = ''.join([repo_url, '#', branch_name])
	build_source = ''.join([build_source, (':' + module_path if module_path is not '' else '')])

	deployment_url = util.get_github_raw_content_url(config.get_config('deploy.default.deployment_yaml_path'), repo_url, branch_name, module_path)
	service_url = util.get_github_raw_content_url(config.get_config('deploy.default.service_yaml_path'), repo_url, branch_name, module_path)
	ingress_url = util.get_github_raw_content_url(config.get_config('deploy.default.ingress_yaml_path'), repo_url, branch_name, module_path)

	deployment_file_path = ''.join([work_dir, '/deployment.yaml'])
	service_file_path = ''.join([work_dir, '/service.yaml'])
	ingress_file_path = ''.join([work_dir, '/ingress.yaml'])
	
	if should_register:
		registry_url = util.get_github_raw_content_url(config.get_config('register.default.registry_yaml_path'), repo_url, branch_name, module_path)
		registry_file_path = ''.join([work_dir, '/registry.yaml'])
	
	try:
		print 'Downloading deployment files'

		MSG_DEPLOYMENT_FILE_NOT_FOUND = 'Deployment file: %s not found'
		download_files = ((deployment_url, deployment_file_path, True, MSG_DEPLOYMENT_FILE_NOT_FOUND % config.get_config('deploy.default.deployment_yaml_path')),
			(service_url, service_file_path, True, MSG_DEPLOYMENT_FILE_NOT_FOUND % config.get_config('deploy.default.service_yaml_path')),
			(ingress_url, ingress_file_path, False))

		if should_register:
			download_files += download_files + ((registry_url, registry_file_path, False),)
		
		try:
			success = util.retrieve_files(*download_files)
		except RuntimeError:
			return 1

		print 'Deployment files downloaded'

		deployment_info = util.convert_yaml_to_object(deployment_file_path)
		tag = deployment_info['spec']['template']['spec']['containers'][0]['image']

		deploy(build_source, tag,
			deployment_file_path,
			service_file_path,
			ingress_file_path if success[ingress_file_path] else None)

		if should_register:
			register.register(registry_file_path)

	except subprocess.CalledProcessError as e:
		print 'ERROR: ' , e

def deploy(build_source, tag, deployment_file_path, service_file_path, ingress_file_path):
	print 'Building docker image from source %s with tag %s' % (build_source, tag)
	subprocess.check_output(('docker build -t %s %s' % (tag, build_source)).split())
	print 'Docker image created'

	print 'Creating deployment'
	subprocess.check_output(('kubectl create -f %s' % deployment_file_path).split())
	print 'Deployment created'

	print 'Creating service'
	subprocess.check_output(('kubectl create -f %s' % service_file_path).split())
	print 'Service created'

	if ingress_file_path is not None:
		print 'Creating ingress'
		subprocess.check_output(('kubectl create -f %s' % ingress_file_path).split())
		print 'Ingress created'
