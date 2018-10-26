import os
import itertools
import sqlite3
from jinja2 import Template
from sqlalchemy import (create_engine,
                        Table,
                        Column,
                        Integer,
                        String,
                        Sequence,
                        MetaData,
                        select,
                        func)
from sqlalchemy.sql import text
from csvtoolz.utils import TableHelper

class DynamicTable():

    """
    Tabla dinamica, permite devolver
    """
    def __init__(self, name, headers, metadata):
        self.headers = headers
        self._name = name
        self.columns = self.make_columns()
        self.table = self.make_table(metadata)

    @property
    def name(self):
        return self._name

    def insert_values(self, *values):
        r = dict(itertools.zip_longest(self.headers, values))
        return self.table.insert().values(**r)

    def prepare_values(self, values):
        return dict(itertools.zip_longest(self.headers, values))

    def insert(self):
        return self.table.insert()

    def select(self):
        return select([self.table])

    def select_table(self):
        return select([self.table])

    def select_injectable(self, injectable):
        return select(injectable).select_from(self.table)

    def make_columns(self):
        """
        arma un vector de columnas.
        """
        seq_name="{}_id_seq".format(self.name)
        columns=[Column('id', Integer, Sequence(seq_name), primary_key=True)]
        for h in self.headers:
            columns.append(Column(h, String))

        return columns

    def make_table(self, metadata):
        return Table(self.name, metadata,
                     *self.columns)


class SQL():

    def __init__(self, engine):
        self.engine = create_engine(engine)
        self.meta = MetaData()
        self.conn = self.engine.connect()

    def __str__(self):
        return self.engine

    @property
    def metadata(self):
        return self.meta

    def create_db(self, check=True):
        self.meta.create_all(self.engine, checkfirst=check)

    def insert_row(self):
        pass

    def close(self):
        self.conn.close()

class Cache(SQL):

    _tables = {}

    def __init__(self, engine):
        super().__init__(engine)

    def add_table(self, name, table):
        self._tables.update({name: table})

    def get_table(self, name):
        """
        Recibe el nombre de la tabla que debe buscar en el
        diccionario _tables.

        Devuelve la tabla segun el nombre que se le pasa.
        En caso que la tabla no exista o no este registrada
        devolvera None
        """
        try:
            return self._tables[name]
        except KeyError:
            return None

    def insert_row(self, name, values):
        """
        Recibe `name` str es el tipo de tabla.
        Y values que puede ser un vector. :
        """
        headers = self.get_headers(name)
        # tiene que borrar el id
        headers.pop(0)
        keys_values = TableHelper.prepare_values(
            headers, values
        )

        #keys_values=self._tables[name].prepare_values(values)
        self.conn.execute(self._tables[name].insert(), **keys_values)

    def get_headers(self, name, del_id=False):
        """
        Retorna un array con el nombre de las columnas, tener en cuenta
        que incluye el nombre de la tabla:
            ['test.id', 'test.name', ... ]

        """
        headers = self._tables[name].columns.keys()
        if del_id:
            headers.pop(0)
        return headers


    def select_all(self, name):
        s = select([self._tables[name]])
        return self.conn.execute(s)

    def select_count(self, name):
        #count = self._tables[name].select_injectable([func.count('*')])
        count = select([func.count('*')]).select_from(self._tables[name])
        #count2 = select([func.count('*')]).select_from(self._tables[name].table)
        return self.conn.scalar(count)

    def select_column(self, name, column):
        """Devuelve una columna pasada como parametro.
        Retorn un ResultProxy.

        """
        col = getattr(self._tables[name].c, column)
        select_col = select(col)
        return self.conn.execute(select_col)

    def get_select(self, name):
        """
        Retorna el objeto select y ademas la tabla para poder
        personalizar los queries en caso que se requiera.
        """
        return select([self._tables[name]])

    def select_limit_offset(self, name, limit, offset):
        return select([self._tables[name]]).limit(limit).offset(offset)

    def find_duplicates(self, name):
        """Busca duplicados en la tabla.
        """
        headers = self.get_headers(name)
        #query = text("SELECT *, count(*) FROM :table GROUP BY :column HAVING count(*)>1")
        query = text("SELECT *, count(*) FROM {} GROUP BY {} HAVING count(*)>1".format(name, headers[1]))
        #query = query.bindparams(table=name, column=headers[1])
        #import pdb; pdb.set_trace()
        #result = self.conn.execute(query, table=name, column=headers[1])
        result = self.conn.execute(query)
        return result

    def insert_chunk(self, name, chunk):
        headers = self.get_headers(name, del_id=True)

        values= list(map(lambda x:
                          TableHelper.prepare_values(headers, x),
                          chunk))

        self.conn.execute(self._tables[name].insert(), values)

    def create_table(self, name, headers):
        table = TableHelper.make_table(name, self.metadata, headers)
        table.create(self.engine, checkfirst=True)
        self.add_table(name, table)

    def flush(self):
        #for k in self._tables.keys():
        #    flush_table(k)

        for tbl in reversed(self.metadata.sorted_tables):
            self.conn.execute(tbl.drop(self.engine))
            self._tables.pop(tbl, None)

    def flush_table(self, name):
        self._tables[name].drop(self.engine)
        self._tables.pop(name, None)

    def execute(self, query):
        """
        wrap de con.execute, al objeto que devuleve se puede hacer
        un fetchall() para ejecutar el proxy
        """

        proxy = self.conn.execute(query)
        return proxy




if __name__ == '__main__':
    #c = Cache('sqlite:///test2.db')
    c = Cache('sqlite:///test3.db')
    c.create_table("test", ['title', 'name', 'age'])
    c.create_db()
    c.insert_row('test', ['nacion', 'alberto'])
    c.insert_row('test', ['nacion', 'alberto'])
    c.insert_row('test', ['nacion', 'alberto'])
    c.insert_row('test', ['nacion', 'alberto'])
    c.insert_row('test', ['nacion', 'alberto'])
    c.insert_row('test', ['nacion2', 'alberto'])
    c.insert_row('test', ['nacion3', 'alberto'])
    c.insert_row('test', ['nacion4', 'alberto'])
    count = c.select_count('test')
    print(count)
    duplicates = c.find_duplicates("test")
    import pdb; pdb.set_trace()
    table = c.select_limit_offset("test", 2, 2)
    #import pdb; pdb.set_trace()
    print("count result")

    r = c.select_all('test')

    for i in r:
        print(i)

