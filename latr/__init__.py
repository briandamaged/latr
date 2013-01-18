
def empty():
  """
  Returns an empty iterator
  """
  return iter(())

def identity(iterable):
  for item in iterable:
    yield item


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


class Cycle(object):
  def __init__(self):
    self.__memory = []

  def __call__(self, iterable):
    for item in iterable:
      self.__memory.append(item)
      yield item
    while True:
      for item in self.__memory:
        yield item



class BatchesOf(object):
  def __init__(self, size):
    self.size = size

  def __call__(self, iterable):
    while True:
      batch = []
      for x in xrange(self.size):
        batch.append(iterable.next())
      yield batch



class latr(object):
  def __init__(self, iterable):
    self.iterable = iter(iterable)

  def next(self):
    return self.iterable.next()

  def __iter__(self):
    return self

  def __rshift__(self, consumer):
    return latr(consumer(self.iterable))




def lmap(map_function, iterable):
  return LMap(map_function)(iterable)

def lfilter(filter_function, iterable):
  return LFilter(filter_function)(iterable)

def cycle(iterable):
  return Cycle()(iterable)

