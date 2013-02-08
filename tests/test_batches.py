from latr.core    import latr
from latr.batches import BatchesOf, include_leftovers, discard_leftovers, pad_leftovers_with

from collections import Iterator
from unittest import TestCase


class Test_BatchesOf(TestCase):
  def setUp(self):
    self.items = ["c", "c++", "java", "c#", "python", "ruby", "perl", "bash"]
  
  def test_it_raises_a_TypeError_when_size_is_not_an_int(self):
    self.assertRaises(TypeError, BatchesOf, 3.2)

  def test_it_raises_a_ValueError_when_size_is_less_then_1(self):
    self.assertRaises(ValueError, BatchesOf, 0)
    self.assertRaises(ValueError, BatchesOf, -4)

  def test_it_returns_an_Iterator(self):
    result = latr(self.items) >> BatchesOf(1)
    self.assertTrue(isinstance(result, Iterator))


  def test_each_list_has_1_item_when_size_is_1(self):
    result = latr(self.items) >> BatchesOf(1)
    
    for i in self.items:
      self.assertEqual(result.next(), [i])

  def test_1_batch_is_returned_when_size_exactly_equals_number_of_items(self):
    result = list(latr(self.items) >> BatchesOf(len(self.items)))

    self.assertEqual(len(result), 1)
    self.assertEqual(result[0], self.items)
  
  def test_all_items_are_returned_when_batch_size_divides_items_evenly(self):
    result = list(latr(self.items) >> BatchesOf(4))
    
    self.assertEqual(len(result), 2)
    self.assertEqual(result[0] + result[1], self.items)

  def test_items_that_do_not_fit_in_a_batch_are_discarded_by_default(self):
    result = list(latr(self.items) >> BatchesOf(3))
    
    self.assertEqual(len(result), 2)
    self.assertEqual(result[0], self.items[0:3])
    self.assertEqual(result[1], self.items[3:6])

  def test_discard_leftovers_causes_remaining_items_to_be_discarded(self):
    result = list(latr(self.items) >> BatchesOf(3, on_leftovers = discard_leftovers))
    
    self.assertEqual(len(result), 2)
    self.assertEqual(result[0], self.items[0:3])
    self.assertEqual(result[1], self.items[3:6])

  def test_include_leftovers_causes_remaining_items_to_be_yielded_as_the_final_batch(self):
    result = list(latr(self.items) >> BatchesOf(3, on_leftovers = include_leftovers))
    
    self.assertEqual(len(result), 3)
    self.assertEqual(result[0], self.items[0:3])
    self.assertEqual(result[1], self.items[3:6])
    self.assertEqual(result[2], self.items[6:8])


  def test_pad_leftovers_with_causes_a_default_value_to_be_used_in_place_of_missing_items(self):
    result = list(latr(self.items) >> BatchesOf(5, on_leftovers = pad_leftovers_with('stuff')))
    
    self.assertEqual(len(result), 2)
    self.assertEqual(result[0], self.items[0:5])
    self.assertEqual(result[1], self.items[5:8] + ['stuff', 'stuff'])