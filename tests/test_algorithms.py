import unittest

from page_replacemet.kod import PageReplacementSimulator


class TestPageReplacementAlgorithms(unittest.TestCase):

    def test_standard_example(self):
        sim = PageReplacementSimulator(
            capacity=3,
            reference_string=[1, 2, 3, 1, 4, 5, 2, 1]
        )
        results = sim.run_all()

        self.assertEqual(results["FIFO"]["page_faults"], 7)
        self.assertEqual(results["LRU"]["page_faults"], 7)
        self.assertEqual(results["OPTIMAL"]["page_faults"], 5)

    def test_empty_reference_string(self):
        sim = PageReplacementSimulator(3, [])
        results = sim.run_all()

        for result in results.values():
            with self.subTest(algorithm=result["algorithm"]):
                self.assertEqual(result["page_faults"], 0)
                self.assertEqual(result["hits"], 0)
                self.assertEqual(result["history"], [])

    def test_repeated_page(self):
        sim = PageReplacementSimulator(3, [1, 1, 1])
        results = sim.run_all()

        for result in results.values():
            with self.subTest(algorithm=result["algorithm"]):
                self.assertEqual(result["page_faults"], 1)
                self.assertEqual(result["hits"], 2)

    def test_single_frame(self):
        sim = PageReplacementSimulator(1, [1, 2, 1, 3])
        results = sim.run_all()

        for result in results.values():
            with self.subTest(algorithm=result["algorithm"]):
                self.assertEqual(result["page_faults"], 4)
                self.assertEqual(result["hits"], 0)

    def test_history_length_and_counts(self):
        references = [1, 2, 3, 1, 4, 5, 2, 1]
        sim = PageReplacementSimulator(3, references)
        results = sim.run_all()

        for name, result in results.items():
            with self.subTest(algorithm=name):
                history = result["history"]

                self.assertEqual(len(history), len(references))
                self.assertEqual(
                    sum(step["is_fault"] for step in history),
                    result["page_faults"]
                )
                self.assertEqual(
                    result["page_faults"] + result["hits"],
                    len(references)
                )

    def test_optimal_is_not_worse_than_other_algorithms(self):
        references = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3]
        sim = PageReplacementSimulator(3, references)
        results = sim.run_all()

        optimal_faults = results["OPTIMAL"]["page_faults"]

        for name, result in results.items():
            with self.subTest(algorithm=name):
                self.assertLessEqual(
                    optimal_faults,
                    result["page_faults"]
                )


    def test_zero_and_negative_capacity_rejected(self):
        for capacity in (0, -1):
            with self.subTest(capacity=capacity):
                with self.assertRaises(ValueError):
                    PageReplacementSimulator(capacity, [1, 2, 3])

    def test_non_integer_capacity_rejected(self):
        for capacity in (1.5, "3", True):
            with self.subTest(capacity=capacity):
                with self.assertRaises(ValueError):
                    PageReplacementSimulator(capacity, [1, 2, 3])

    def test_invalid_page_values_rejected(self):
        invalid_sequences = [[1, -2, 3], [1, "abc", 3], [1, 2.5], [True, 2]]

        for references in invalid_sequences:
            with self.subTest(references=references):
                with self.assertRaises(ValueError):
                    PageReplacementSimulator(3, references)

    def test_non_list_reference_string_rejected(self):
        with self.assertRaises(ValueError):
            PageReplacementSimulator(3, (1, 2, 3))


if __name__ == "__main__":
    unittest.main(verbosity=2)
