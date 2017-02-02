#!/usr/bin/python

import os
import json
import uuid
import yaml
import shutil
import urllib
import urllib2
import argparse
import subprocess
from urlparse import urlparse

# TODO get config from central location
ORCHESTRATOR_PROTOCOL = 'http'
ORCHESTRATOR_HOST = '119.74.248.86'
# ORCHESTRATOR_HOST = '192.168.1.11'
ORCHESTRATOR_PORT = '8080'
ORCHESTRATOR_REGISTER_PATH = 'jarvis/orchestrator/v1/register'

GITHUB_DEFAULT_REPO = 'https://github.com/lahsivjar/jarvis-kube-modules.git'
GITHUB_RAW_CONTENT_URL = 'https://raw.githubusercontent.com'
GITHUB_DEFAULT_BRANCH = 'master'

DEFAULT_DEPLOYMENT_PATH = 'deployment/deployment.yaml'
DEFAULT_SERVICE_PATH = 'deployment/service.yaml'
DEFAULT_INGRESS_PATH = 'deployment/ingress.yaml'
DEFAULT_REGISTRY_PATH = 'deployment/registry.yaml'

MSG_DEPLOYMENT_FILE_NOT_FOUND = 'Deployment file: %s not found'

DEFAULT_TEMP_DIR = '/tmp'

def available_arguments():
	return [
		{
			'metavar': 'module-path',
			'dest': 'module_path',
			'help': 'The path of the module in the git repo',
			'nargs': '?'
		},
		{
			'flags': ('-r', '--repo-url'),
			'help': 'The git repo to clone the module from'
		},
		{
			'flags': ('-b', '--branch'),
			'help': 'The branch to pull from. Default is master.'
		},
		{
			'flags': ('-l', '--local'),
			'help': 'Deploy a local module'
		}
	]

def get_raw_content_url(target, username, repo_name, branch_name, path):
	return GITHUB_RAW_CONTENT_URL + '/' + username + '/' + repo_name + '/' + branch_name + '/' + path + '/' + target
	
def retrieve_file(url, file_path):
	try:
		response = urllib2.urlopen(url)
		with open(file_path, 'w') as file:
			file.write(response.read())
		return True
	except urllib2.HTTPError as e:
		return False
		

def make_dirs(filename):
	if not os.path.exists(os.path.dirname(filename)):
		try:
			os.makedirs(os.path.dirname(filename))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise

def get_repo_data(repo_url):
	url = urlparse(repo_url)
	username = url.path.split('/')[1]
	repo_name = url.path.split('/')[2][:-4]
	return (username, repo_name)
	
def convert_yaml_to_object(yaml_path):
	with open(yaml_path, 'r') as stream:
		try:
			return yaml.load(stream)
		except yaml.YAMLError as e:
			print e
			raise

def run(args):
	if args.repo_url is None and args.module_path is None:
		print 'No deploy target found'
		return
	
	repo_url = args.repo_url if args.repo_url is not None else GITHUB_DEFAULT_REPO
	branch_name = args.branch if args.branch is not None else GITHUB_DEFAULT_BRANCH
	module_path = args.module_path if args.module_path is not None else ''

	build_source = repo_url + '#' + branch_name
	build_source += (':' + module_path if module_path is not '' else '')

	username, repo_name = get_repo_data(repo_url)
	
	deployment_url = get_raw_content_url(DEFAULT_DEPLOYMENT_PATH, username, repo_name, branch_name, module_path)
	service_url = get_raw_content_url(DEFAULT_SERVICE_PATH, username, repo_name, branch_name, module_path)
	ingress_url = get_raw_content_url(DEFAULT_INGRESS_PATH, username, repo_name, branch_name, module_path)
	registry_url = get_raw_content_url(DEFAULT_REGISTRY_PATH, username, repo_name, branch_name, module_path)

	tmp_dir = ''.join([DEFAULT_TEMP_DIR, '/',  uuid.uuid4().hex])
	
	try:
		print 'Downloading deployment files'
		deployment_file_path = ''.join([tmp_dir, '/deployment.yaml'])
		make_dirs(deployment_file_path)
		if not retrieve_file(deployment_url, deployment_file_path):
			deployment_file_path = None
			print MSG_DEPLOYMENT_FILE_NOT_FOUND % DEFAULT_DEPLOYMENT_PATH
			return 1
			
		service_file_path = ''.join([tmp_dir, '/service.yaml'])
		make_dirs(service_file_path)
		if not retrieve_file(service_url, service_file_path):
			service_file_path = None
			print MSG_DEPLOYMENT_FILE_NOT_FOUND % DEFAULT_SERVICE_PATH
			return 1
		
		ingress_file_path = ''.join([tmp_dir, '/ingress.yaml'])
		make_dirs(ingress_file_path)
		if not retrieve_file(ingress_url, ingress_file_path):
			ingress_file_path = None
			# print MSG_DEPLOYMENT_FILE_NOT_FOUND % DEFAULT_INGRESS_PATH
			# print 'Module will not be externally reachable'
		
		registry_file_path = ''.join([tmp_dir, '/registry.yaml'])
		make_dirs(registry_file_path)
		if not retrieve_file(registry_url, registry_file_path):
			registry_file_path = None
			# print MSG_DEPLOYMENT_FILE_NOT_FOUND % DEFAULT_REGISTRY_PATH
			# print 'Module will not be registered on the orchestrator'
		
		print 'Deployment files downloaded'

		deployment_info = convert_yaml_to_object(deployment_file_path)
		tag = deployment_info['spec']['template']['spec']['containers'][0]['image']

		deploy(build_source, tag, deployment_file_path, service_file_path, ingress_file_path, registry_file_path)

	except subprocess.CalledProcessError as e:
		print 'ERROR: ' , e
	finally:
		cleanup(tmp_dir)

def deploy(build_source, tag, deployment_file_path, service_file_path, ingress_file_path, registry_file_path):
	print 'Building docker image from source %s with tag %s' % (build_source, tag)
	subprocess.check_output(('docker build -t %s %s' % (tag, build_source)).split())
	print 'Docker image created'

	#TODO verify yamls
	if deployment_file_path is not None:
		print 'Creating deployment'
		subprocess.check_output(('kubectl create -f %s' % deployment_file_path).split())
		print 'Deployment created'

	if service_file_path is not None:
		print 'Creating service'
		subprocess.check_output(('kubectl create -f %s' % service_file_path).split())
		print 'Service created'

	if ingress_file_path is not None:
		print 'Creating ingress'
		subprocess.check_output(('kubectl create -f %s' % ingress_file_path).split())
		print 'Ingress created'
		
	if registry_file_path is not None:
		print 'Registering module'
		registry_info = convert_yaml_to_object(registry_file_path)
		request_url = '%s://%s:%s/%s' % (ORCHESTRATOR_PROTOCOL, ORCHESTRATOR_HOST, ORCHESTRATOR_PORT, ORCHESTRATOR_REGISTER_PATH)
		req = urllib2.Request(request_url, json.dumps(registry_info), {'Content-Type': 'application/json'})
		response = urllib2.urlopen(req)
		response_data = json.load(response)
		if response_data:
			print 'Module registered'
		else:
			print 'Module registration failed'
			
def cleanup(tmp_dir):
	shutil.rmtree(tmp_dir)
