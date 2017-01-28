# Gets a list of services from the service resolver for each query. The module then
# requests each service with the query and returns a json response with predefined keys
import requests
import string
import responsefilter

from constants import RegistryKeys
from serviceregistry import ServiceRegistry

class ServiceResolver:
  def __init__(self):
    self.registry = ServiceRegistry()

  def get_resolved_services(self, query):
    regex_map = self.registry.get_regex_map()
    service_list = []
    for uri, value in regex_map.iteritems():
      service_id = value.get(RegistryKeys.SERVICE_ID)
      regex = value.get(RegistryKeys.ACCEPTANCE_COMPILED_REGEX)

      # Evaluate regex if matches then add the service to the list
      match = regex.match(query)
      if match != None:
        service_dict = self.registry.get(service_id)
        assert service_dict != None
        service_list.append({
            RegistryKeys.SERVICE_ID: service_dict[RegistryKeys.SERVICE_ID],
            RegistryKeys.SERVICE_NAME: service_dict[RegistryKeys.SERVICE_NAME],
            RegistryKeys.NAMESPACE: service_dict[RegistryKeys.NAMESPACE],
            RegistryKeys.SERVICE_PORT: service_dict[RegistryKeys.SERVICE_PORT],
            RegistryKeys.URI: uri
        })
    return service_list

class Worker:
  def __init__(self):
    self.resolver = ServiceResolver()

  def do(self, query):
    service_list = self.resolver.get_resolved_services(query)
    print service_list
    response_list = []
    for service in service_list:
      response_list.append(requests.get(self._get_url(service, query)).json())
    return response_list

  def _get_url(self, service, query):
    url_builder = ['http://']
    url_builder.append(service[RegistryKeys.SERVICE_ID])
    url_builder.append('.')
    url_builder.append(service[RegistryKeys.NAMESPACE])
    url_builder.append('.svc.cluster.local:')
    url_builder.append(str(service[RegistryKeys.SERVICE_PORT]))
    url_builder.append(service[RegistryKeys.URI])
    url_builder.append('?query=')
    url_builder.append(query)

    print string.join(url_builder, '')

    return string.join(url_builder, '')
