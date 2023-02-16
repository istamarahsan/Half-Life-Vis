import unittest
from half_life import HalfLifeCalculator
import csv

TOLERANCE: float = 0.005


class TestDecayCalculation(unittest.TestCase):

    def test_n_remaining(self) -> None:
        calculator = HalfLifeCalculator()
        with open("tests/test_data.csv", newline='') as data_file:
            reader = csv.DictReader(data_file, delimiter=',')
            for row in reader:
                n_0 = float(row["N_0"])
                half_life = float(row["Half-life"])
                time_passed = float(row["Time passed"])
                expected = float(row["N_t"])
                actual = calculator.n_remaining(n_0, half_life, time_passed)
                diff = abs(expected - actual)
                self.assertTrue(diff <= TOLERANCE)


if __name__ == '__main__':
    unittest.main()