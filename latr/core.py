


class Latr(object):
  def __init__(self, iterable):
    self.iterable = iter(iterable)

  def next(self):
    return self.iterable.next()

  def __iter__(self):
    return self

  def __rshift__(self, consumer):
    return latr(consumer(self.iterable))


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

