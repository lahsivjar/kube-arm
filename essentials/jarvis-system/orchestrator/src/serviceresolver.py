# Gets a query and tries to resolve the services that claim to fulfill
# the query and then passes the result to the next phase
import asyncworker

def do(query):
  # TODO: Implement service resolver logic
  return asyncworker.do({
    'service_id': 'goog-knowledge-graph',
    'service_port': '8080',
    'namespace': 'default',
    'endpoint': '/module/googknowledge/v1/describe',
    'query': query
  })
