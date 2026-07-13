import unittest

from src.analytics.ratios import *


class TestRatios(unittest.TestCase):

    # 1
    def test_net_profit_margin(self):
        self.assertEqual(net_profit_margin(200, 1000), 20)

    # 2
    def test_net_profit_zero_sales(self):
        self.assertIsNone(net_profit_margin(100, 0))

    # 3
    def test_operating_profit_margin(self):
        opm, mismatch = operating_profit_margin(250, 1000, 25)
        self.assertEqual(opm, 25)
        self.assertFalse(mismatch)

    # 4
    def test_opm_mismatch(self):
        opm, mismatch = operating_profit_margin(250, 1000, 20)
        self.assertTrue(mismatch)

    # 5
    def test_return_on_equity(self):
        self.assertEqual(return_on_equity(100, 300, 200), 20)

    # 6
    def test_negative_equity(self):
        self.assertIsNone(return_on_equity(100, -100, 50))

    # 7
    def test_return_on_assets(self):
        self.assertEqual(return_on_assets(100, 1000), 10)

    # 8
    def test_roa_zero_assets(self):
        self.assertIsNone(return_on_assets(100, 0))


if __name__ == "__main__":
    unittest.main()