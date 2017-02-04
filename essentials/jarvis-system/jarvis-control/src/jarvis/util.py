#!/usr/bin/python

import os
import yaml
import urllib2
from urlparse import urlparse

GITHUB_RAW_CONTENT_DOMAIN = 'https://raw.githubusercontent.com'

def get_github_raw_content_url(target, repo_url, branch_name, path):
	username, repo_name = get_github_repo_data(repo_url)
	return ''.join([GITHUB_RAW_CONTENT_DOMAIN, '/', username, '/',
		repo_name, '/',branch_name, '/', path, '/', target])

def retrieve_file(url, file_path):
	try:
		response = urllib2.urlopen(url)
		with open(file_path, 'w') as file:
			file.write(response.read())
		return True
	except urllib2.HTTPError as e:
		return False

def retrieve_files(*file_infos):
	success = {}
	for file_info in file_infos:
		make_dirs(file_info[1])
		if not retrieve_file(file_info[0], file_info[1]):
			success[file_info[1]] = False
			if file_info[2]:
				print file_info[3]
				raise RuntimeError
		else:
			success[file_info[1]] = False
	return success

def make_dirs(filename):
	if not os.path.exists(os.path.dirname(filename)):
		try:
			os.makedirs(os.path.dirname(filename))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise

def get_github_repo_data(repo_url):
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