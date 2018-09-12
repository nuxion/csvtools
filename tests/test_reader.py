import os
import unittest
import types
from nose.tools import assert_equals, timed
from sqlalchemy import MetaData, Table, Column
from csvtoolz import CSVFile
from csvtoolz.reader import name_file


class test_reader(unittest.TestCase):

    sfile = "./files/simple.csv"


    def setUp(self):
        self.csvfile = CSVFile(self.sfile)

    def tearDown(self):
        tmpfs = name_file(self.csvfile.path)
        if os.path.exists(tmpfs):
            os.remove(tmpfs)

    @timed(0.1)
    def test_CSVFile(self):

        self.assertIsInstance(self.csvfile, CSVFile)

    @timed(0.1)
    def test_read_file(self):
        count = 0
        for c in self.csvfile.inspect().set_headers().open_csv():
            count += 1

        self.assertEqual(count, 3)

    def test_chunks(self):
        count = 0
        for c in self.csvfile.inspect().set_generator(True).make_chunks():
            count += 1
        self.assertEqual(count, 1)

    def test_export_bom(self):
        result=self.csvfile.export(with_bom=True)

        self.assertTrue(os.path.isfile(result))

    def test_export_delimiter(self):
        result=self.csvfile.export(delimiter=",")
        with open(result, 'r') as f:
            line = f.readline()
            result = len(line.split(','))

        self.assertEqual(result, 4)






