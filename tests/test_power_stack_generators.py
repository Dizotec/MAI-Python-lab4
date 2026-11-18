import random
import unittest

from algolab.generators import KINDS, generate
from algolab.recurrent import iter as iterative_power
from algolab.recurrent import recur
from algolab.stack import Stack


class PowerTests(unittest.TestCase):
    def test_matches_integer_power(self):
        for power in (iterative_power, recur):
            for value in (-7, 0, 1, 2, 2**53 + 1):
                for degree in (0, 1, 2, 9, 20):
                    result = power(value, degree)
                    self.assertIs(type(result), int)
                    self.assertEqual(result, value ** degree)

    def test_rejects_invalid_input_at_function_boundary(self):
        for power in (iterative_power, recur):
            with self.assertRaises(ValueError):
                power(2, -1)
            for args in ((2, 2.5), ("2", 3), (2, True), (False, 3), (3, None)):
                with self.subTest(power=power.__name__, args=args), self.assertRaises(TypeError):
                    power(*args)


class StackTests(unittest.TestCase):
    def test_lifo_peek_and_size(self):
        stack = Stack()
        self.assertFalse(stack)
        self.assertEqual(len(stack), 0)
        stack.push("first")
        stack.push(None)
        self.assertTrue(stack)
        self.assertIsNone(stack.peek())
        self.assertEqual(len(stack), 2)
        self.assertIsNone(stack.pop())
        self.assertEqual(stack.pop(), "first")
        self.assertFalse(stack)

    def test_push_then_pop_restores_previous_top_and_length(self):
        stack = Stack()
        stack.push("original")
        before = len(stack), stack.peek()
        value = object()
        stack.push(value)
        self.assertIs(stack.pop(), value)
        self.assertEqual((len(stack), stack.peek()), before)

    def test_empty_operations_raise_index_error(self):
        stack = Stack()
        for operation in (stack.peek, stack.pop):
            with self.assertRaises(IndexError):
                operation()


class GeneratorTests(unittest.TestCase):
    def test_sizes_and_seed(self):
        for kind in KINDS:
            for size in (0, 1, 2, 101):
                data = generate(kind, size, 42)
                self.assertEqual(len(data), size)
                self.assertEqual(data, generate(kind, size, 42))
            with self.assertRaises(ValueError):
                generate(kind, -1, 42)

    def test_random_generators_use_local_seed(self):
        state = random.getstate()
        for kind in ("random", "almost-sorted", "duplicates"):
            self.assertNotEqual(generate(kind, 200, 42), generate(kind, 200, 43))
        self.assertEqual(random.getstate(), state)

    def test_shapes(self):
        ascending = list(range(100))
        self.assertEqual(generate("sorted", 100), ascending)
        self.assertEqual(generate("reverse", 100), ascending[::-1])
        almost = generate("almost-sorted", 100, 42)
        self.assertEqual(sorted(almost), ascending)
        self.assertEqual(sum(a != b for a, b in zip(almost, ascending)), 10)
        self.assertLessEqual(len(set(generate("duplicates", 100, 42))), 5)
