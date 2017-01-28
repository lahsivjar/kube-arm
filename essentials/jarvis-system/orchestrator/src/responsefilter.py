# Filters the response recieved from external service on the basis of set
# conventions and returns the message that jarvis will convey to requester
from constants import ResponseType

def do(service_name, response_dict):
  try:
    response_type = response_dict['type']
    return _parse_map[response_type](response_dict)
  except KeyError:
    return 'Invalid response recieved from service: {0}'.format(service_name)

def _parse_state(response_dict):
  state = response_dict['state'] == 'true'
  if state:
    return 'Successfully executed'
  else:
    return 'Failed to execute'

def _parse_message(response_dict):
  return response_dict['result']

def _parse_redirect():
  # TODO
  return 'Not implemented'

def _parse_forward():
  # TODO
  return 'Not implemented'

_parse_map = {
  ResponseType.STATE : _parse_state,
  ResponseType.MESSAGE: _parse_message,
  ResponseType.REDIRECT: _parse_redirect,
  ResponseType.FORWARD: _parse_forward
}
