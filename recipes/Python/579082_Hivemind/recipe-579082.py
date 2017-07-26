from collections import defaultdict
from json import dumps

class Hivemind:
  __shared_states = defaultdict(dict)
  def __init__(self, *args, **kwargs):
    key = type(self).__name__, dumps(args, sort_keys=True), dumps(kwargs, sort_keys=True)
    self.__dict__ = self.__shared_states[key]
