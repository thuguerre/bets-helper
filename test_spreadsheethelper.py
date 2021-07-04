# Standard Library imports
import pytest
import unittest

# Local imports
import localcontextloader
from baseball_japan.SpreadSheetHelper import SpreadSheetHelper

class TestSpreadSheetHelper(unittest.TestCase):

    helper = None

    def setUp(self):
        self.helper = SpreadSheetHelper()

    def tearDown(self):
        pass

    @pytest.mark.unittest
    def test_format_date(self):
        date = '2021-06-22'
        self.assertEqual(self.helper.formatDate(date), '22/06/2021')
