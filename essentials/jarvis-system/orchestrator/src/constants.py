from enum import Enum

class ResponseType(Enum):
  MESSAGE = 'message'
  STATE = 'state'
  REDIRECT = 'redirect'
  FORWARD = 'forward'

class RegistryKeys(Enum):
  SERVICE_ID = 'service_id'
  SERVICE_NAME = 'service_name'
  SERVICE_PORT = 'service_port'
  NAMESPACE = 'namespace'
  ENDPOINTS = 'endpoints'
  URI = 'uri'
  ACCEPTANCE_REGEX = 'acceptance_regex'
