import os
import sqlite3
from jinja2 import Template


class Cache():

    def __init__(self, model, path="lite.db", in_memory=False):

        if in_memory:
            self.memory=True
            self.conn =sqlite3.connect(":memory:")
        else:
            self.path = path
            self.conn = sqlite3.connect(path)

        self.c = self.conn.cursor()
        self.model = model

    def _table_t(self):
        return  Template('''
                         CREATE TABLE {{ name }}(
                         {% for c in columns %}
                         {{c.name }} {{ c.type }} {{ c.constraint }} {{ c.end }}
                         {% endfor %}
                         )
                         ''')
    def _insert_t(self):
        return Template('''
                        INSERT INTO {{ table }}
                        (
                        {% for v in values %}
                            v
                        )
                        ''')
    def create_table(self, name, headers):
        template = self._table_template()
        _table = template.render(name=name, columns=self.model)
        print(_table)

        self.c.execute(_table)
        self.conn.commit()

    def insert_row(self, values):
        pass

    def close(self):
        self.conn.close()

def make_model(headers):
    model =[{'name': 'id',
             'type': 'int',
             'constraint': 'PRIMARY KEY NOT NULL',
             'end': ','}]
    count = 0
    while count < (len(headers)-1):
        model.append({'name': headers[count],
                      'type': 'text',
                      'constraint': '',
                      'end': ','})
        count += 1


    model.append({'name': headers[count],
                  'type': 'text',
                  'constraint': '',
                  'end': ''})
    return model


if __name__ == '__main__':
    c = Cache()
    c.create_table("test", ['test1', 'test2', 'test3'])
    c.close()
