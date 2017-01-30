#!/usr/bin/python

import subprocess
import argparse
import urllib
import uuid
import yaml
import os
from urlparse import urlparse

GITHUB_DEFAULT_REPO = 'https://github.com/lahsivjar/jarvis-kube-modules.git'
GITHUB_RAW_CONTENT_URL = 'https://raw.githubusercontent.com'
GITHUB_DEFAULT_BRANCH = 'master'

DEFAULT_DEPLOYMENT_PATH = 'deployment/deployment.yaml'
DEFAULT_SERVICE_PATH = 'deployment/service.yaml'
DEFAULT_INGRESS_PATH = 'deployment/ingress.yaml'

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
	
	deployment_path = get_raw_content_url(DEFAULT_DEPLOYMENT_PATH, username, repo_name, branch_name, module_path)
	service_path = get_raw_content_url(DEFAULT_SERVICE_PATH, username, repo_name, branch_name, module_path)
	ingress_path = get_raw_content_url(DEFAULT_INGRESS_PATH, username, repo_name, branch_name, module_path)

	tmp_dir = uuid.uuid4().hex
	
	try:
		print 'Downloading deployment files'
		deployment_file = DEFAULT_TEMP_DIR + '/' + tmp_dir + '/deployment.yaml'
		make_dirs(deployment_file)
		urllib.urlretrieve(deployment_path, deployment_file)
		#TODO handle the case where deployment file does not exist or network fails
	
		service_file = DEFAULT_TEMP_DIR + '/' + tmp_dir + 'service.yaml'
		make_dirs(service_file)
		urllib.urlretrieve(service_path, service_file)
		#TODO handle if service file does not exist or network fails

		ingress_file = DEFAULT_TEMP_DIR + '/' + tmp_dir + 'ingress.yaml'
	        make_dirs(ingress_file)
        	urllib.urlretrieve(ingress_path, ingress_file)
	        #TODO handle if ingress file does not exist or network fails
		print 'Deployment files downloaded'

		with open(deployment_file, 'r') as stream:
			try:
				deployment_info = yaml.load(stream)
				tag = deployment_info['spec']['template']['spec']['containers'][0]['image']
			except yaml.YAMLError as e:
				print e	

		print 'Building docker image from source %s with tag %s' % (build_source, tag)
		subprocess.check_output(('docker build -t %s %s' % (tag, build_source)).split())
		print 'Docker image created'

		print 'Creating deployment'
		subprocess.check_output(('kubectl create -f %s' % deployment_file).split())
		print 'Deployment created'

		print 'Creating service'
		subprocess.check_output(('kubectl create -f %s' % service_file).split())
		print 'Service created'

		print 'Creating ingress'
		subprocess.check_output(('kubectl create -f %s' % ingress_file).split())
		print 'Ingress created'
	except subprocess.CalledProcessError as e:
		print 'ERROR: ' , e.output
