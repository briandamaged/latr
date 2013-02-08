from latr.core import Latr, clone_each

from collections import Iterator

from unittest import TestCase
from mock import MagicMock

class Test_latr(TestCase):
  def test_it_wraps_an_iterable(self):
    l = Latr(xrange(10))
    for i in xrange(10):
      self.assertEqual(l.next(), i)


  
  def test_it_provides_a_shorthand_syntax_for_composing_consumers(self):
    def consumer(iterable):
      for i in iterable:
        yield i * 2

    l = Latr(xrange(10)) >> consumer
    
    for i in xrange(10):
      self.assertEqual(l.next(), i * 2)


  def test_the_composition_shortcut_returns_a_new_Latr_instance(self):
    def consumer(iterable):
      for i in iterable:
        yield i * 2

    l1 = Latr([1, 2, 3])
    l2 = l1 >> consumer

    self.assertNotEqual(l1, l2)
  
  
  def test_values_are_handed_to_consumers_lazily(self):
    m = MagicMock('m')
    
    def supplier():
      for i in xrange(3):
        m()
        yield i
    
    def consumer(iterable):
      for i in iterable:
        yield i * 2
    
    l = Latr(supplier()) >> consumer
    
    self.assertFalse(m.called)
    self.assertEqual(l.next(), 0)
    self.assertTrue(m.called)


  def test_peek_raises_StopIteration_when_there_are_not_more_items(self):
    l = Latr([])
    self.assertRaises(StopIteration, l.peek)
  
  
  def test_peek_returns_the_same_item_until_next_is_called(self):
    l = Latr([1, 2, 3])
    self.assertEqual(l.peek(), 1)
    self.assertEqual(l.peek(), 1)
    self.assertEqual(l.next(), 1)
    self.assertEqual(l.peek(), 2)
    self.assertEqual(l.next(), 2)
    self.assertEqual(l.peek(), 3)
    self.assertEqual(l.peek(), 3)

  def test_is_empty_returns_True_when_there_are_no_more_items(self):
    l = Latr([])
    self.assertTrue(l.is_empty)
  
  
  def test_is_empty_returns_False_when_there_are_more_items(self):
    l = Latr([1])
    self.assertFalse(l.is_empty)


  def test_is_empty_does_not_move_the_item_iterator(self):
    l = Latr([1])
    l.is_empty
    self.assertEqual(l.next(), 1)

  def test_has_next_returns_False_when_there_are_no_more_items(self):
    l = Latr([])
    self.assertFalse(l.has_next)

  def test_has_next_returns_True_when_there_are_more_items(self):
    l = Latr([1, 2, 3])
    self.assertTrue(l.has_next)

  def test_has_next_does_not_move_the_iterator(self):
    l = Latr([1])
    l.has_next
    self.assertEqual(l.next(), 1)



class Test_clone_each(TestCase):
  def test_it_returns_an_iterator(self):
    result = clone_each([1, 2, 3])
    self.assertTrue(isinstance(result, Iterator))
    
  def test_it_returns_a_copy_of_each_item(self):
    items = [
      {"numbers" : [1, 2, 3]},
      {"I'm" : "awesome", "how" : "are you?"},
      ["bob", "dole"]
    ]
    
    retval = clone_each(items)
    for r in retval:
      # Values are the same
      self.assertTrue(r in items)
      
      # But the id's are different
      original_item = items[items.index(r)]
      self.assertNotEqual(id(r), id(original_item))


