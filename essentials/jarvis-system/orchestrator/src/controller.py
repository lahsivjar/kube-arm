import queryanalyzer
import serviceregistry
import json

from serviceregistry import ServiceRegistry
from flask import Flask
from flask import request

mapping = Flask(__name__)

@mapping.route('/v1', methods=['GET'])
def query():
  query = request.args.get('query')
  return queryanalyzer.do(query)

@mapping.route('/v1/register', methods=['POST'])
def register():
  # Get the service description
  service_desc = request.json
  print ServiceRegistry().get_regex_map()
  # Register service
  return json.dumps(ServiceRegistry().register(service_desc))
