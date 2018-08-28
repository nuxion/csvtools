import unittest
import types
from nose.tools import assert_equals, timed
from csvtoolz import inspect, transform, separators
from csvtoolz import models, CSVFile


filetest = "./files/ARG-22-MPF-tabla1-06-2018_2018_08_15__15_40_01.csv"

@timed(1.1)
def test_chardetect():
    esperado = models.Properties('ISO-8859-1', ';', '"')
    #CSVProperties(encoding='ISO-8859-1', delimiter=';', quotechar='"')
    result = inspect(filetest)


    assert_equals(esperado, result)

class test_CSVFile(unittest.TestCase):

    SIMPLEF = "./files/simple.csv"
    def setUp(self):
        self.file_obj = CSVFile(self.SIMPLEF)

    @timed(0.1)
    def test_instanceCSV(self):
        self.assertIsInstance(self.file_obj, CSVFile)

    @timed(0.1)
    def test_opencsv(self):
        csv = self.file_obj.inspect().open_csv()
        self.assertIsInstance(csv, types.GeneratorType)

    @timed(0.1)
    def test_headers(self):
        header= ['id','names','lastnames', 'age']
        self.file_obj.inspect().set_generator().set_headers()
        self.assertEqual(self.file_obj.headers,header)

    @timed(0.2)
    def test_lenght(self):
        count = 0
        for l in self.file_obj.inspect().open_csv():
            count += 1
        self.assertEqual(count,3)

    def test_chunks(self):
        result = []
        for c in self.file_obj.inspect().set_generator().make_chunks():
            result.append(c)

        self.assertEqual(len(result[0]), 3)











