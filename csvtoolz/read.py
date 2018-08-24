import csv


def read_line(csvfile,
               encoding="utf-8",
               separator=";",
               quotechar='"',
               **kwargs):
    """
    return a generator for the file
    """

    with open(csvfile, 'r', encoding=encoding) as f:
        for line in csv.reader(f,
                               separator=separator,
                               quotechar=quotechar):
            yield line

def make_chunks(gfile, lines=50):
    """
    Debe recibir el generator del archivo ya abierto
    y devolvera tambien un generador.
    """
    count = 0
    chunk = []
    while True:
        try:
            chunk.append(gfile.__next__())
        except StopIteration:
                break
        if count >= lines:
            yield chunk
            del chunk[:]
            count = 0

def extract_header(gfile):
    return gfile.__next__()


if __name__=='__main__':
    pass

