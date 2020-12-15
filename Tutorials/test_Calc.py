import unittest
import Calc


class TestCalc(unittest.TestCase):

    def test_add(self):
        self.assertEqual(Calc.add(2, 8), 10)
        self.assertEqual(Calc.add(-2, -8), -10)
        self.assertEqual(Calc.add(-1, 1), 0)

    def test_subtract(self):
        self.assertEqual(Calc.subtract(10, 8), 2)
        self.assertEqual(Calc.subtract(-2, -8), 6)
        self.assertEqual(Calc.subtract(-1, 1), -2)

    def test_multiply(self):
        self.assertEqual(Calc.multiply(10, 8), 80)
        self.assertEqual(Calc.multiply(-2, -8), 16)
        self.assertEqual(Calc.multiply(-1, 1), -1)
        self.assertEqual(Calc.multiply(0, 0), 0)

    def test_divide(self):
        self.assertEqual(Calc.divide(10, 5), 2)
        self.assertEqual(Calc.divide(-1, -1), 1)
        self.assertEqual(Calc.divide(5, -2), -2.5)

        with self.assertRaises(ValueError):
            Calc.divide(10, 0)


if __name__ == '__main__':
    unittest.main()
