import csv
import os
from csvtoolz.inspectors import inspect
from csvtoolz.models import Properties


class CSVFile():
    """
    Objeto que se encarga de manejar el csv.
    Tener en cuenta que hace chain de elementos pero siempre va a modificar
    al objeto inicial ya que devuelve la referencia a si mismo y no una copia
    del objeto.
    """

    def __init__(self, path, encoding="utf-8",delimiter=";", quotechar='"'):
        self.path = path
        self.props = Properties(encoding, delimiter, quotechar)
        self.gfile = None
        self._headers = []


    def set_headers(self):
        g = self.open_csv()
        self._headers = g.__next__()
        g.close()
        return self

    def set_generator(self, headers=True):
        """
        Inicia y crea el generator para el archivo csv.

        """
        self.gfile = self.open_csv()
        if not headers:
            self.gfile.__next__()

        return self

    def inspect(self):
        """
        Deberia deprecar en futuras versiones
        """
        self.props = inspect(self.path)
        return self

    def set_props(self, encode='utf-8', delimiter=';',
                  quotechar='"', auto_inspect=False):
        """
        Establece las propiedades del csv, que tiene que ver con los
        delimitadores, quotechar y encode.

        Si se sete auto_inspect = True, revisara el archivo para
        tomar dichos valores.
        """

        if auto_inspect:
            self.props = inspect(self.path)
            return self

        self.props = Properties(encoding, delimiter, quotechar)

        return self


    def open_csv(self):
        with open(self.path, 'r', encoding=self.props.encoding) as f:
            for line in csv.reader(f,
                                   delimiter=self.props.delimiter,
                                   quotechar=self.props.quotechar):
                yield line

    @property
    def headers(self):
        return self._headers

    def generator(self):
        """
        Property para devovler el generator.
        """
        return self.gfile

    def read(self):
        pass

    def make_chunks(self, lines=10):
        """
        Recibe el path
        """
        #if not with_head:
        #    self.gfile.__next__()

        count = 0
        chunk = []
        #while line <= lines:
        try:
            while 1:
                #import pdb; pdb.set_trace()
                chunk.append(self.gfile.__next__())
                count +=1
                if count >= lines:
                    yield chunk
                    del chunk[:]
                    count = 0
        except StopIteration:
            yield chunk

    def export(self,
                encode='utf-8',
                delimiter=";",
                quotechar='"',
                with_bom = False):
        """
        Metodo para cambiar el encode line por line y agregar BOM
        al principio del archivo.
        """
        bom = '\uFEFF'
        export_fs =  name_file(self.path)

        with open(export_fs, 'a', encoding=encode)  as tmp_file:
            if with_bom:
                tmp_file.write(bom)
            writer = csv.writer(tmp_file,
                                delimiter=delimiter,
                                quotechar=quotechar)
            for line in self.inspect().open_csv():
                writer.writerow(line)

        return export_fs

def name_file(fullpath):
    abspath = os.path.abspath(fullpath)
    splited = os.path.split(abspath)

    exported = "exported_{}".format(splited[1])
    return os.path.join(splited[0], exported)


if __name__=='__main__':
    import sys

    import pdb; pdb.set_trace()

    if len(sys.argv) >= 2:
        f = CSVFile(sys.argv[1])
        #assert type(f) == "__main__.CSVFile"
        #for l in f.inspect().open_csv():
        #    print (l)
        result = []
        #for c in f.inspect().set_generator().make_chunks():
        #    import pdb; pdb.set_trace()
        #    result.append(c)
        test = name_file(sys.argv[1])

        for c in f.inspect().set_generator(True).make_chunks():
            print("====== CHUNK ====")
            print("Longitud del chunk: {}".format(len(c)))
            print(c)














