from nose.tools import assert_equals, timed
from csvtoolz import inspect, transform, separators
from csvtoolz import models


filetest = "./files/ARG-22-MPF-tabla1-06-2018_2018_08_15__15_40_01.csv"

@timed(1.1)
def test_chardetect():
    esperado = models.Properties('ISO-8859-1', ';', '"')
    #CSVProperties(encoding='ISO-8859-1', delimiter=';', quotechar='"')
    result = inspect(filetest)


    assert_equals(esperado, result)


