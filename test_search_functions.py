"""
This module tests every function inside of search.py
"""
import unittest
from unittest.mock import patch
import mocks
import search

class TestingApiCalls(unittest.TestCase):
    """
    Boiler plate code which utilizes the unittest library
    """
    @patch('search.sp.search')
    def test_search(self, mockcreate):
        """
        Function mocks JSON data from mocks.py in place of API call
        in order to test the search_songs fucntion
        """
        mockcreate.return_value = mocks.mocked_api_data
        query = 'smooth operator'
        self.assertEqual(search.search_song(query),
                          search.parse_results(mockcreate.return_value))

    def test_parse(self):
        """
        Function tests that parse_results function correctly parses data 
        and always returns a tuple containing 3 lists, given a JSON input   
        """
        test_value = (['Smooth Operator - Single Version', 'Smooth Operator', 'Smooth Operator'],
                      ['Sade', 'MoWetTheDon', 'Sade'],
                      ['1Hv1VTm8zeOeybub15mA2R', '1XtY7ZTN4W1diEt5ArXKvm',
                        '7pLuEMFougkSHXrPBtNxTR'])
        self.assertEqual(search.parse_results(mocks.mocked_api_data),
                                              test_value)

if __name__=='__main__':
    unittest.main()
