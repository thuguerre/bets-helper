import pytest
import unittest
from baseball_japan import SpreadSheetHelper
from LocalExecHelper import LocalExecHelper

class TestSpreadSheetHelper(unittest.TestCase):

    helper = None

    def setUp(self):
        LocalExecHelper()
        self.helper = SpreadSheetHelper()

    def tearDown(self):
        pass

    @pytest.mark.unittest
    def test_format_date(self):
        date = '2021-06-22'
        self.assertEqual(self.helper.formatDate(date), '22/06/2021')
