import json

from serviceregistry import ServiceRegistry
from worker import Worker
from flask import Flask
from flask import request

mapping = Flask(__name__)

@mapping.route('/v1/search', methods=['GET'])
def query():
  query = request.args.get('query')
  return json.dumps(Worker().do(query))

@mapping.route('/v1/service/register', methods=['POST'])
def register():
  # Get the service description
  service_desc = request.json
  # Register service
  return json.dumps(ServiceRegistry().register(service_desc))

@mapping.route('/v1/service/deregister', methods=['POST'])
def deregister():
  # Get service id to deregister
  service_id = request.form['service_id']
  # Deregister the service
  return json.dumps(ServiceRegistry().deregister(service_id))

@mapping.route('/v1/service/getall', methods=['GET'])
def get_all_services():
  return json.dumps(ServiceRegistry().get_service_list())
