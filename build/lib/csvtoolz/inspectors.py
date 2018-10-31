import csv
import chardet
from toolz.functoolz import pipe
from functools import reduce
from csvtoolz.models import Properties

def chardetect(stream, limit=20):
    """Recibe la referencia al archivo abierto en modo binario.
    Lo itera hasta que se termine el archivo o llegue a limite del parametro
    `limit`. Lo analiza y devuelve el resultado.

    :params: stream
    :params: limit
    :returns: chardet
    """

    buffer_lines = []
    stream_buffer = bytearray()
    for line in stream:
        buffer_lines.append(line)
        line=bytearray(line)
        stream_buffer += line
        if len(buffer_lines) > limit:
            break

    res = chardet.detect(stream_buffer)
    res.update({'lines': buffer_lines })

    return res

def convert_bytearray(encoding, lines):
    #: El map convierte la linea de bytes en str text de una
    #: sola linea.
    text = reduce(lambda y,z: "{}{}".format(y, z) ,
                 list(map(lambda x: x.decode(encoding), lines)))

    return text

def separators(text):
    """Recibe un array con las lineas en bytes capturado
    por chardetect.

    Los decodifica a string segun el chardetect obtenido.

    """

    options = ['|', ';', ',']
    counts = 0
    separator = None
    for o in options:
        c = text.count(o)
        if c > counts:
            counts = c
            separator = o
    return separator

def transform(r):
    """
    Toma el resultado, descarta lo que no sirve y realiza una namedtuple
    para responder. A la vez permite utilizar esta ultima funcion
    como interfaz para modificar el formato de la respuesta
    sin afectar el resto.



    """

    if r['sniffer']:
        props = Properties(r['encoding'],
                           r['sniffer'].delimiter,
                           r['sniffer'].quotechar)
    else:
        props = Properties(r['encoding'],
                           None,
                           None)

    return props

def inspect(arch):
    """
    Revisa un archivo csv y devuelve un namedtupple con
    el encoding, el delimitador y el quotechar.

    """

    with open(arch, "rb") as f:
        #result = pipe(f, chardetect, separators, transform)
        coding = chardetect(f)

    text = convert_bytearray(coding['encoding'], coding['lines'])
    field_separator = separators(text)
    sniffer = csv.Sniffer().sniff(text)
    props = Properties(coding['encoding'],
                       field_separator,
                       sniffer.quotechar)

    return props


if __name__=='__main__':
    import sys

    #example = "../tests/files/ARG-22-MPF-tabla1-06-2018_2018_08_15__15_40_01.csv"
    if len(sys.argv) == 3:
        test = inspect(sys.argv[2])
        print (test)
        assert type(test.encoding) == str
        print("Assert [ok]")
    else:
        print("Es necesario indicar el archivo a analizar")


