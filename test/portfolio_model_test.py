import unittest
import json

from db import Portfolio


class PortfolioTestCase(unittest.TestCase):
    def test_portfolio__green_path(self):
        json_dict = {
            "FB": 0.2,
            "AMZN": 0.2,
            "GOOG": 0.2,
            "AAPL": 0.2,
            "TSLA": 0.2, }
        json_str = json.dumps(json_dict)
        portfolio = Portfolio("x", json_str)
        assert set(portfolio.symbols) == set(json_dict.keys())
        assert portfolio.percentages == list(json_dict.values())

    def test_portfolio_sum_of_percentage_wrong__throws_ValueError(self):
        json_dict = {
            "FB": 0.2,
            "AMZN": 0.2,
            "GOOG": 0.2,
            "AAPL": 0.3,
            "TSLA": 0.2, }
        json_str = json.dumps(json_dict)
        with self.assertRaises(ValueError):
            Portfolio("x", json_str)


if __name__ == '__main__':
    unittest.main()
