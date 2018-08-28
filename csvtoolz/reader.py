import csv
from csvtoolz.inspectors import inspect
from csvtoolz.models import Properties


class CSVFile():

    def __init__(self, path, encoding="utf-8",delimiter=";", quotechar='"'):
        self.path = path
        self.props = Properties(encoding, delimiter, quotechar)
        self.gfile = None
        self._headers = []


    def set_headers(self):
        self._headers = self.gfile.__next__()

    def set_generator(self, headers=True):
        self.gfile = self.open_csv()
        if not headers:
            self.gfile.__next__()

        return self

    def inspect(self):
        self.props = inspect(self.path)
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
        self.gfile = self.setcsv()
        return self

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

    def wrapper(self, lines=10):

        count = 0
        chunk = []
        while True:
            yield from self.gfile
            count +=1
            if count >= lines:
                yield chunk




if __name__=='__main__':
    import sys

    if len(sys.argv) >= 2:
        f = CSVFile(sys.argv[1])
        #assert type(f) == "__main__.CSVFile"
        #for l in f.inspect().open_csv():
        #    print (l)
        result = []
        #for c in f.inspect().set_generator().make_chunks():
        #    import pdb; pdb.set_trace()
        #    result.append(c)

        for c in f.inspect().set_generator(True).make_chunks():
            print("====== CHUNK ====")
            print("Longitud del chunk: {}".format(len(c)))
            print(c)












