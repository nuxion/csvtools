import unittest
import types
from nose.tools import assert_equals, timed
from sqlalchemy import MetaData, Table, Column
from csvtoolz import Cache, DynamicTable
from csvtoolz.cache import SQL
from csvtoolz.utils import TableHelper


class test_SQL(unittest.TestCase):

    urlsql = "sqlite://"

    def setUp(self):
        self.sql = SQL(self.urlsql)

    def tearDown(self):
        self.sql.close()


    @timed(0.1)
    def test_sql(self):

        self.assertIsInstance(self.sql, SQL)

    @timed(0.1)
    def test_MetaData(self):

        self.assertIsInstance(self.sql.metadata, MetaData)

    def test_close(self):
        self.sql.close()
        self.assertEqual(self.sql.conn.closed, True)

class test_TableHelper(unittest.TestCase):

    headers = ['name', 'last', 'age']

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_make_columns(self):
        c = TableHelper.make_columns("test", self.headers)

        self.assertEqual(len(c), len(self.headers) + 1)

    def test_make_columns_coltype(self):
        c = TableHelper.make_columns("test", self.headers)
        self.assertIsInstance(c[0], Column)


    def test_make_table(self):
        urlsql = "sqlite://"
        sql = SQL(urlsql)
        table = TableHelper.make_table("test",
                                       sql.metadata,
                                       self.headers)
        self.assertIsInstance(table, Table)


class test_Cache(unittest.TestCase):

    headers = ['name', 'last', 'age']
    values = ["jose", "peres", '45']
    values_bad = ["peres", '45']
    values_bad2 = ["peres", '45', "test", "more_column"]
    urlsql = "sqlite://"

    def setUp(self):
        self.cache = Cache(self.urlsql)
        self.cache.create_table("test_init", self.headers)

    def tearDown(self):
        self.cache.close()

    def test_cache(self):
        self.assertIsInstance(self.cache, Cache)

    def test_add_table(self):
        table = TableHelper.make_table("addtable",
                                       self.cache.metadata,
                                       self.headers)
        self.cache.add_table("addtable", table)
        self.assertIsInstance(self.cache._tables['addtable'],
                              Table)

    def test_create_table(self):

        self.cache.create_table("testcreate",
                                self.headers)

        self.assertIsInstance(self.cache._tables['testcreate'], Table)

    def test_create_db(self):
        pass

    def test_insert_values(self):
        self.cache.create_db()
        self.cache.insert_row("test_init", self.values)
        result = self.cache.select_all("test_init")
        values = [(1, "jose", "peres", '45')]
        print(result)
        print(values)


        self.assertListEqual(values, list(result))

    def test_select_count(self):
        self.cache.create_db()
        self.cache.insert_row("test_init", self.values)
        self.cache.insert_row("test_init", self.values)
        count = self.cache.select_count("test_init")

        self.assertEqual(count, 2)


    def test_insert_chunk(self):
        self.cache.create_db()
        chunk = [self.values, self.values, self.values, self.values]
        self.cache.insert_chunk('test_init', chunk)
        count = self.cache.select_count("test_init")
        self.assertEqual(count, 4)













