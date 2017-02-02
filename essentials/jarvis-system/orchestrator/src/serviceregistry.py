import os
import re
import redis
import pickle
import string

from enum import Enum
from constants import RegistryKeys
from voluptuous import Schema, Required, Any, MultipleInvalid

# Get redis host and port via environment variable
REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = os.environ['REDIS_PORT']

# Redis key for service registry
_SERVICE_REGISTRY = 'service_registry'

class ServiceRegistry:
  def __init__(self):
    self.redisinstance = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    self.validateschema = Schema({
        Required(RegistryKeys.SERVICE_ID): Any(str, unicode),
        Required(RegistryKeys.SERVICE_NAME): Any(str, unicode),
        Required(RegistryKeys.SERVICE_PORT): int,
        Required(RegistryKeys.NAMESPACE, default='default'): Any(str, unicode),
        Required(RegistryKeys.ENDPOINTS): [{
          Required(RegistryKeys.URI): Any(str, unicode),
          Required(RegistryKeys.ACCEPTANCE_REGEX): Any(str, unicode),
          RegistryKeys.FILTER_REGEX: {
            Required(RegistryKeys.PATTERN): Any(str, unicode),
            Required(RegistryKeys.REPLACE): Any(str, unicode)
          }
        }]
    })

  def register(self, service_dict):
    # Validate the service that needs to be registered
    try:
      self.validateschema(service_dict)
      service_id = service_dict[RegistryKeys.SERVICE_ID]

      # Compile each endpoint regex
      endpoints = service_dict[RegistryKeys.ENDPOINTS]
      for endpoint in endpoints:
        a_regex = endpoint.pop(RegistryKeys.ACCEPTANCE_REGEX)
        f_regex = endpoint.pop(RegistryKeys.FILTER_REGEX, None)
        compiled_a_regex = re.compile(a_regex)
        if f_regex:
          compiled_f_regex = {
            RegistryKeys.COMPILED_PATTERN: re.compile(f_regex.pop(RegistryKeys.PATTERN), re.I),
            RegistryKeys.REPLACE: f_regex.pop(RegistryKeys.REPLACE, None)
          }
        # Update the endpoint object
        endpoint[RegistryKeys.ACCEPTANCE_COMPILED_REGEX] = compiled_a_regex
        endpoint[RegistryKeys.FILTER_COMPILED_REGEX] = compiled_f_regex

      self.redisinstance.hset(_SERVICE_REGISTRY, service_id, self._serialize_data(service_dict))
      return True
    except MultipleInvalid as e:
      return False

  def deregister(self, service_id):
    if service_id:
      self.redisinstance.hdel(_SERVICE_REGISTRY, service_id)
      return not self.redisinstance.hexists(_SERVICE_REGISTRY, service_id)
    return False

  def get(self, service_id):
    return self._deserialize_data(self.redisinstance.hget(_SERVICE_REGISTRY, service_id))

  def getall(self):
    all_services_map = self.redisinstance.hgetall(_SERVICE_REGISTRY)
    all_services_list = all_services_map.values() if all_services_map else []
    deserialized_all_services_list = []
    for service in all_services_list:
      deserialized_all_services_list.append(self._deserialize_data(service))

    return deserialized_all_services_list

  def clear(self):
    self.redisinstance.flushdb()

  def _serialize_data(self, data):
    return None if data == None else pickle.dumps(data)

  def _deserialize_data(self, data):
    return None if data == None else pickle.loads(data)
