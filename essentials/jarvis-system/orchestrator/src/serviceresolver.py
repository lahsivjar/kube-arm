# Gets a query and tries to resolve the services that claim to fulfill
# the query and then passes the result to the next phase
import asyncworker

def do(query):
  # TODO: Implement service resolver logic. The below is only for testing
  if ('helloworld' in query):
    return asyncworker.do({
      'service_id': 'py-helloworld',
      'service_name': 'Hello World',
      'service_port': '8080',
      'namespace': 'default',
      'endpoint': '/module/py/helloworld',
      'query': query
    })
  else:
    return asyncworker.do({
      'service_id': 'goog-knowledge-graph',
      'service_name': 'Knowlege Graph API',
      'service_port': '8080',
      'namespace': 'default',
      'endpoint': '/module/googknowledge/v1/describe',
      'query': query
    })
