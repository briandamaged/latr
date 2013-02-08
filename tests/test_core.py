from latr.core import Latr

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
    