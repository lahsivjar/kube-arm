# Gets a list of services from the service resolver for each query. The module then
# requests each service with the query in async fashion and returns a json response
import requests
import string
import responsefilter

def do(service_dict):
  url = _get_service_url(service_dict)
  return responsefilter.do(service_dict['service_name'], requests.get(url).json())

def _get_service_url(service_dict):
  # TODO: Error handling
  url_builder = ['http://']
  url_builder.append(service_dict['service_id'])
  url_builder.append('.')
  url_builder.append(service_dict['namespace'])
  url_builder.append('.svc.cluster.local:')
  url_builder.append(service_dict['service_port'])
  url_builder.append(service_dict['endpoint'])
  url_builder.append('?query=')
  url_builder.append(service_dict['query'])

  return string.join(url_builder, '')
