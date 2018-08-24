import csv
from profiling import memory, MemoryProfiler
from concurrent.futures import ThreadPoolExecutor
prof = MemoryProfiler()
#example="ARG-22-MPF-tabla1-06-2018_2018_08_15__15_40_01.csv"
example="big.csv"


class Csvfile():

    def __init__(self, path, encoding="utf-8"):
        self.path = path
        self.enco = encoding
        self.gfile = None

    def readcsv(self):
        with open(self.path, 'r', encoding=self.enco) as f:
            for line in csv.reader(f):
                yield line

    def read(self):
        self.gfile = self.readcsv()
        return self

    def make_chunks(self, lines=10):
        """
        Recibe el path
        """

        count = 0
        chunk = []
        #while line <= lines:
        while 1:
            try:
                chunk.append(self.gfile.__next__())
                count +=1
            except StopIteration:
                break
            if count >= lines:
                yield chunk
                del chunk[:]
                count = 0




@memory(prof)
def read_in_chunks(file_object, chunk_size=1024):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

def read2(csvfile, encoding="utf-8"):
    with open(csvfile, 'r', encoding=encoding) as f:
        lines = csv.reader(f)
        a = []
        for line in lines:
            #print(line)
            a.append(line)



@memory(prof)
def readcsv(csvfile, encoding="utf-8"):
    with open(csvfile, 'r', encoding=encoding) as f:
        for line in csv.reader(f):
            yield line

@memory(prof)
def make_chunks(csvfile, encoding, lines=10):
    """
    Recibe el path
    """
    g_result = readcsv(csvfile, encoding=encoding)
    count = 0
    chunk = []
    #while line <= lines:
    while 1:
        try:
            chunk.append(g_result.__next__())
            count +=1
        except StopIteration:
            break
        if count >= lines:
            yield chunk
            del chunk[:]
            count = 0

def test(chunk):
    for c in chunk:
        if type(c[0]) is int:
            pass
        else:
            pass
if __name__=='__main__':
    #gFile = readcsv(example, encoding="ISO-8859-1")

    #for c in make_chunks(example, encoding="ISO-8859-1", lines=500):
        #with ThreadPoolExecutor(max_workers=None) as executor:
        #    for result in executor.map(test, c):
        #        passa
    #    test(c)

    c = Csvfile(example, encoding="ISO-8859-1")

    for _c in c.read().make_chunks():
        pass

    #for c in make_chunks(example, encoding="ISO-8859-1", lines=500):
    #    pass

    #for l in readcsv(example, encoding="ISO-8859-1"):
    #    pass
        #print(c)
    prof.start
    prof.end


    #size = sys.getsizeof(gFile)
    #print(size)

