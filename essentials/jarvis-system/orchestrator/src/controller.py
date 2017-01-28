import json

from serviceregistry import ServiceRegistry
from worker import Worker
from flask import Flask
from flask import request

mapping = Flask(__name__)

@mapping.route('/v1', methods=['GET'])
def query():
  query = request.args.get('query')
  return json.dumps(Worker().do(query))

@mapping.route('/v1/register', methods=['POST'])
def register():
  # Get the service description
  service_desc = request.json
  # Register service
  return json.dumps(ServiceRegistry().register(service_desc))
