from nose.tools import assert_equals, timed
from csvtools import bylines, chardetect


filetest = "./files/ARG-22-MPF-tabla1-06-2018_2018_08_15__15_40_01.csv"

@timed(1.1)
def test_chardetect():
    result= {'encoding': 'ISO-8859-1', 'confidence': 0.73, 'language': ''}
    encoding = chardetect(filetest)
    assert_equals(result, encoding)


