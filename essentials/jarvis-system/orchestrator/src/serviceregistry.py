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

class _RedisEntryType(Enum):
  SERVICE_REGISTRY = 'service_registry'
  REGEX_MAP = 'regex_map'

_KEY_SEPARATOR = '::'

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
          Required(RegistryKeys.ACCEPTANCE_REGEX): Any(str, unicode)
        }]
    })

  def register(self, service_dict):
    # Validate the service that needs to be registered
    try:
      self.validateschema(service_dict)
      service_id = service_dict[RegistryKeys.SERVICE_ID]
      service_key = self._create_service_key(service_id)

      # Update the regex key list
      self._update_regex_list(service_id,service_dict[RegistryKeys.ENDPOINTS]);
      self.redisinstance.set(service_key, self._serialize_data(service_dict))
      return True
    except MultipleInvalid as e:
      return False

  def get(self, service_id):
    service_key = self._create_service_key(service_id)
    return self._deserialize_data(self.redisinstance.get(service_key))

  def get_regex_map(self):
    return self._deserialize_data(self.redisinstance.get(_RedisEntryType.REGEX_MAP))

  def _serialize_data(self, data):
    return None if data == None else pickle.dumps(data)

  def _deserialize_data(self, data):
    return None if data == None else pickle.loads(data)

  def _create_service_key(self, rawkey):
    keybuilder = [_RedisEntryType.SERVICE_REGISTRY]
    keybuilder.append(_KEY_SEPARATOR)
    keybuilder.append(rawkey)

    return string.join(keybuilder, '')

  def _update_regex_list(self, service_id, endpoints_list):
    re_map = self.get_regex_map()
    re_map = {} if re_map == None else re_map
    for endpoint in endpoints_list:
      regex = endpoint[RegistryKeys.ACCEPTANCE_REGEX]
      uri = endpoint[RegistryKeys.URI]
      
      re_map.update({
          uri: {
            'regex': re.compile(regex),
            'service_id': service_id
          }
      })

    # Update to the new list in redis
    self.redisinstance.set(_RedisEntryType.REGEX_MAP, self._serialize_data(re_map))
