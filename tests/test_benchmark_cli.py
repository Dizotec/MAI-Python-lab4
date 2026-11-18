
import io
import unittest
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch

from algolab import benchmark
from algolab.cli import main


class BenchmarkTests(unittest.TestCase):
    def test_independent_inputs_and_median(self):
        original = [10, -1, 2]
        received = []
        events = []
        timestamps = iter([0, 8, 10, 12, 20, 23, 30, 35, 40, 41])

        def clock():
            events.append("clock")
            return next(timestamps)

        def consume(data):
            events.append("sort")
            self.assertEqual(data, original)
            received.append(data)
            data.clear()
            return []

        with patch.object(benchmark, "perf_counter", side_effect=clock):
            self.assertEqual(benchmark._measure_sort(consume, original), 3)
        self.assertEqual(events, ["clock", "sort", "clock"] * 5)
        self.assertEqual(len({id(value) for value in received}), 5)
        self.assertEqual(original, [10, -1, 2])

    def test_report_generates_once_and_times_both_algorithms(self):
        with (
            patch.object(benchmark, "generate", wraps=benchmark.generate) as generate,
            patch.object(benchmark, "quadratic", wraps=benchmark.quadratic) as bubble,
            patch.object(benchmark, "effective", wraps=benchmark.effective) as merge,
            patch.object(benchmark, "perf_counter", return_value=0),
        ):
            report = benchmark.sorting_report((3,), seed=42)
        self.assertEqual(generate.call_count, 5)
        self.assertEqual(bubble.call_count, 25)
        self.assertEqual(merge.call_count, 25)
        for group, kind in enumerate(benchmark.KINDS):
            data = benchmark.generate(kind, 3, 42)
            for index in range(group * 5, group * 5 + 5):
                self.assertEqual(bubble.call_args_list[index].args[0], data)
                self.assertEqual(merge.call_args_list[index].args[0], data)
            self.assertIn(f"| {kind} | 3 | 0.000 | 0.000 |", report)


class InterfaceTests(unittest.TestCase):
    def command(self, *args):
        out = io.StringIO()
        with patch("sys.argv", ["algolab", *args]), redirect_stdout(out):
            main()
        return out.getvalue()

    def test_descending_via_cli(self):
        for method in ("--effective", "--quadratic"):
            result = self.command("sorting", method, "--reverse", "-2", "2", "1")
            self.assertEqual(result.strip(), "[2, 1, -2]")

    def test_help_for_every_command(self):
        commands = (
            ((), "generate"),
            (("sorting",), "--effective"),
            (("recurrent",), "--recur"),
            (("struct",), "стека"),
            (("generate",), "--kind"),
            (("benchmark",), "{sorting,recurrent}"),
            (("benchmark", "sorting"), "--sizes"),
            (("benchmark", "sorting", "--effective"), "--quadratic"),
            (("benchmark", "recurrent"), "--iter"),
        )
        for command, expected in commands:
            for flag in ("-h", "--help"):
                with self.subTest(command=command, flag=flag):
                    out = io.StringIO()
                    err = io.StringIO()
                    with patch("sys.argv", ["algolab", *command, flag]), redirect_stdout(out), redirect_stderr(err):
                        try:
                            main()
                        except SystemExit as error:
                            self.assertEqual(error.code, 0)
                    self.assertEqual(err.getvalue(), "")
                    self.assertIn("usage:", out.getvalue())
                    self.assertIn(expected, out.getvalue())

    def test_report_via_cli(self):
        with patch.object(benchmark, "perf_counter", return_value=0):
            result = self.command("benchmark", "sorting", "--sizes", "4", "--seed", "3")
        self.assertIn("| duplicates | 4 | 0.000 | 0.000 |", result)

    def test_negative_power_is_rejected_in_benchmark(self):
        err = io.StringIO()
        with redirect_stderr(err), self.assertRaises(SystemExit) as caught:
            self.command("benchmark", "recurrent", "--recur", "2", "-1")
        self.assertEqual(caught.exception.code, 2)
        self.assertIn("неотрицательным", err.getvalue())
