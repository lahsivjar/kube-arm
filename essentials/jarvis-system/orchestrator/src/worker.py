# Gets a list of services from the service resolver for each query. The module then
# requests each service with the query and returns a json response with predefined keys
import requests
import string
import grequests
import responsefilter

from constants import RegistryKeys
from serviceregistry import ServiceRegistry

# Fix agressive monkey patching of grequests by being overly aggressive
# WARNING: If curious george continues to cause problems kick him out
from gevent import monkey as curious_george_messed_up
curious_george_messed_up.patch_all()

class ServiceResolver:
  def __init__(self):
    self.registry = ServiceRegistry()

  def get_resolved_services(self, query):
    regex_map = self.registry.get_regex_map()
    service_list = []
    if regex_map != None:
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
              RegistryKeys.URI: uri,
              RegistryKeys.FILTER_COMPILED_REGEX: value.get(RegistryKeys.FILTER_COMPILED_REGEX)
          })
    return service_list

class Worker:
  def __init__(self):
    self.resolver = ServiceResolver()

  def do(self, query):
    service_list = self.resolver.get_resolved_services(query)
    response_list = []
    if service_list:
      urls = []
      for service in service_list:
        filtered_query = self._filter_query(query, service[RegistryKeys.FILTER_COMPILED_REGEX])
        urls.append(self._get_url(service, filtered_query))

      # Create a set of unsent requests
      response_set = (grequests.get(url) for url in urls)
      # Send the requests
      response_array = grequests.map(response_set)
      # Get the response content from the response and close the response
      for response in response_array:
        if response:
          response_list.append(response.json())
          response.close()
        # TODO: Else response should contain the fact that it failed to get anything from the service
        # Probably handle it via responsefilter
    return response_list

  def _get_url(self, service, query):
    url_builder = ['http://']
    url_builder.append(service[RegistryKeys.SERVICE_ID])
    url_builder.append('.')
    url_builder.append(service[RegistryKeys.NAMESPACE])
    url_builder.append('.svc.cluster.local:')
    url_builder.append(str(service[RegistryKeys.SERVICE_PORT]))
    url_builder.append(service[RegistryKeys.URI])
    if query:
      url_builder.append('?query=')
      url_builder.append(query)

    return string.join(url_builder, '')

  def _filter_query(self, query, filter_regex):
    if filter_regex == None:
      return query

    pattern = filter_regex[RegistryKeys.COMPILED_PATTERN]
    repl = filter_regex[RegistryKeys.REPLACE]

    return pattern.sub(repl, query)
