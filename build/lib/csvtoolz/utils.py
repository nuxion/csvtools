import itertools
from sqlalchemy import Table, Column, String, Sequence, Integer


class TableHelper():
    """
    Se encarga de fabricar el objeto Table propio de sqlalchemy
    make_columns, y make_table comparten la misma interfaz entre si, y
    a su vez con Table para poder hacer piping,
    """


    @classmethod
    def make_columns(cls, name, headers):
        """
        arma un vector de columnas.
        """
        columns=[cls.make_id(name)]
        for h in headers:
            columns.append(Column(h, String))

        return columns

    @classmethod
    def make_table(cls, name, metadata, headers):
        """ devuelve la tabla """
        columns = cls.make_columns(name, headers)

        return Table(name, metadata,
                     *columns)

    @staticmethod
    def make_id(name):
        """
        Genera una column para usar como ID en el cache.
        Como se piensa en sqlite, es necesario especificar la secuencia.
        """
        seq_name="{}_id_seq".format(name)
        return Column('id', Integer, Sequence(seq_name), primary_key=True)

    @staticmethod
    def prepare_values(headers, values):
        """
        Mapea dos array a un diccionario.
        zip_longest funciona para casos de array dispares.

        El diccianrio es para poder ser pasado como **kwargs
        al momento de hacer un insert o update de multiples
        parametros.
        """

        return dict(itertools.zip_longest(headers, values))







