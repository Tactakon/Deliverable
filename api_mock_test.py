import unittest 
from unittest.mock import patch
import mocks
import search

class TestingApiCalls(unittest.TestCase):
    @patch('search.sp.search')
    def testSearch(self, mockcreate):
        mockcreate.return_value = mocks.mocked_api_data
        query = 'smooth operator'
        self.assertEquals(search.search_song(query), search.parse_results(mockcreate.return_value))  

if __name__=='__main__':
    unittest.main()