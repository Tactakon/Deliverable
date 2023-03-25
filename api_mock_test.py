"""
This module contains unit tests for the API calls.
"""

import unittest
from unittest.mock import patch
import mocks
import search

class TestingApiCalls(unittest.TestCase):
    """
    This class contains unit tests for the API calls.
    """
    @patch('search.sp.search')
    # pylint: disable=invalid-name
    def testSearch(self, mockcreate):
        """
        Test the search_song function using mocked data.

        The test case calls the search_song function with 
        a query and compares the result with the expected output.
        """
        mockcreate.return_value = mocks.mocked_api_data
        query = 'smooth operator'
        self.assertEqual(search.search_song(query), search.parse_results(mockcreate.return_value))

if __name__=='__main__':
    unittest.main()
