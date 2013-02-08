

def discard_leftovers(leftovers, size):
  return None


def include_leftovers(leftovers, size):
  return leftovers

class pad_leftovers_with(object):
  def __init__(self, value):
    self.value = value

  def __call__(self, leftovers, size):
    padding = [self.value] * (size - len(leftovers))
    return leftovers + padding


class BatchesOf(object):
  def __init__(self, size, on_leftovers = discard_leftovers):
    if not isinstance(size, int):
      raise TypeError("size must be an integer")
    
    if size < 1:
      raise ValueError("size must be >= 1")

    self.size = size
    self.on_leftovers = on_leftovers

  def __call__(self, iterable):
    try:
      while True:
        batch = []
        for x in xrange(self.size):
          batch.append(iterable.next())
        yield batch
    except StopIteration:
      if len(batch) > 0:
        batch = self.on_leftovers(batch, self.size)
        if batch:
          yield batch
