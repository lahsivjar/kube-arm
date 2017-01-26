import queryanalyzer

from flask import Flask
from flask import request

mapping = Flask(__name__)

@mapping.route("/v1", methods=['GET'])
def query():
  query = request.args.get('query')
  return queryanalyzer.do(query)
