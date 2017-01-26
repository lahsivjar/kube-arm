from enum import Enum

class ResponseType(Enum):
  MESSAGE = 'message'
  STATE = 'state'
  REDIRECT = 'redirect'
  FORWARD = 'forward'
