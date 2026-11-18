import itertools
import random
import unittest
from dataclasses import dataclass

from algolab.sorting import effective, quadratic


@dataclass(frozen=True)
class Record:
    priority: int
    name: str

    def __lt__(self, other: "Record") -> bool:
        """Порядок определяется только приоритетом, имя различает записи."""
        return self.priority < other.priority


class SortingTests(unittest.TestCase):
    def test_edge_cases_and_input_preservation(self):
        cases = ([], [7], [-4, -1, 3], [7, 2, -1], [2, -3, 2, 0, -3])
        for sort in (quadratic, effective):
            for original in cases:
                with self.subTest(sort=sort.__name__, original=original):
                    data = original.copy()
                    result = sort(data)
                    self.assertEqual(result, sorted(original))
                    self.assertIsNot(result, data)
                    self.assertEqual(data, original)

    def test_matches_reference_on_random_arrays(self):
        rng = random.Random(2026)
        for _ in range(40):
            data = [rng.randint(-10, 10) for _ in range(rng.randrange(80))]
            for sort in (quadratic, effective):
                self.assertEqual(sort(data), sorted(data))
                self.assertEqual(sort(data, reverse=True), sorted(data, reverse=True))

    def test_invalid_inputs(self):
        for sort in (quadratic, effective):
            for data in (None, (2, 1), "abc", [1, "2"]):
                with self.subTest(sort=sort.__name__, data=data), self.assertRaises(TypeError):
                    sort(data)

    def test_merge_comparison_bound_on_basic_inputs(self):
        class Counted:
            comparisons = 0

            def __init__(self, value):
                self.value = value

            def __lt__(self, other):
                Counted.comparisons += 1
                return self.value < other.value

        rng = random.Random(42)
        n = 128
        cases = (range(n), range(n - 1, -1, -1), [0] * n,
                 [rng.randrange(n) for _ in range(n)])
        for values in cases:
            Counted.comparisons = 0
            result = effective([Counted(value) for value in values])
            self.assertEqual([row.value for row in result], sorted(values))
            self.assertLessEqual(Counted.comparisons, n * (n - 1).bit_length())

    def test_equal_priorities_keep_names_in_order_in_both_directions(self):
        data = [Record(2, "B"), Record(1, "Z"), Record(2, "A"),
                Record(1, "Y"), Record(2, "C"), Record(1, "X")]
        for sort in (quadratic, effective):
            for reverse, expected in ((False, "ZYXBAC"), (True, "BACZYX")):
                with self.subTest(sort=sort.__name__, reverse=reverse):
                    result = sort(data, reverse=reverse)
                    self.assertEqual("".join(row.name for row in result), expected)
                    self.assertEqual("".join(row.name for row in data), "BZAYCX")

    def test_stability_for_every_small_priority_sequence(self):
        for size in range(7):
            for priorities in itertools.product(range(3), repeat=size):
                data = [Record(priority, str(i)) for i, priority in enumerate(priorities)]
                for sort in (quadratic, effective):
                    for reverse in (False, True):
                        result = sort(data, reverse=reverse)
                        self.assertEqual([row.priority for row in result], sorted(priorities, reverse=reverse))
                        for group in range(3):
                            self.assertEqual([row.name for row in result if row.priority == group],
                                             [row.name for row in data if row.priority == group])
