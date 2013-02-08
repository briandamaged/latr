


class Latr(object):
  def __init__(self, iterable):
    self.iterable = iter(iterable)
    
    self.__next_value = None
    self.__next_value_ready = False
  
  
  def peek(self):
    if self.__next_value_ready:
      return self.__next_value
    else:
      self.__next_value = self.iterable.next()
      self.__next_value_ready = True
      return self.__next_value

  def next(self):
    retval = self.peek()
    self.__next_value_ready = False
    return retval

  @property
  def is_empty(self):
    try:
      self.peek()
      return False
    except StopIteration:
      return True

  @property
  def has_next(self):
    try:
      self.peek()
      return True
    except StopIteration:
      return False


  def __iter__(self):
    return self

  def __rshift__(self, consumer):
    return Latr(consumer(self))


def latr(iterable):
  if isinstance(iterable, Latr):
    return iterable
  else:
    return Latr(iterable)



class Map(object):
  def __init__(self, map_function):
    self.map_function = map_function

  def __call__(self, iterable):
    for item in iterable:
      yield self.map_function(item)


class Filter(object):
  def __init__(self, filter_function):
    self.filter_function = filter_function

  def __call__(self, iterable):
    for item in iterable:
      if self.filter_function(item):
        yield item



def chain(iterable):
  for data in iterable:
    for value in data:
      yield value



def cycle(iterable):
  memory = []
  for item in iterable:
    memory.append(item)
    yield item
  while True:
    for item in memory:
      yield item

