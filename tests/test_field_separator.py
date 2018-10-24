import os
import unittest
import types
from nose.tools import assert_equals, timed
from sqlalchemy import MetaData, Table, Column
from csvtoolz import CSVFile
from csvtoolz.reader import name_file


class test_reader(unittest.TestCase):

    sfile = "./files/field_separator.csv"


    def setUp(self):
        self.csvfile = CSVFile(self.sfile)

    def tearDown(self):
        tmpfs = name_file(self.csvfile.path)
        if os.path.exists(tmpfs):
            os.remove(tmpfs)

    def test_setting_delimiter(self):
        csv = CSVFile(self.sfile, delimiter=";")
        headers = self.csvfile.set_headers().headers


        self.assertEqual(len(headers), 10)

    def test_auto_inspect(self):
        headers = self.csvfile\
            .set_props(auto_inspect=True)\
            .set_headers()\
            .headers

        self.assertEqual(len(headers), 10)

    def test_auto_inspect2(self):
        csv = CSVFile("./files/field_separator2.csv")
        headers = csv\
            .set_props(auto_inspect=True)\
            .set_headers()\
            .headers
        self.assertEqual(len(headers), 2)






