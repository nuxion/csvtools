#!/bin/env python3
import click
from csvtoolz import CSVFile

@click.group()
def printcsv():
    pass

@printcsv.command()
@click.argument('path')
@click.option('--lines', '-l', default=5, help="El numero de lineas que se quiere mostrar")
def show(path, lines):
    csvfile = CSVFile(path)
    result = csvfile\
        .inspect()\
        .set_generator(True)\
        .make_chunks(lines=lines).__next__()
    for r in result:
        click.echo(r)

@click.group()
def export():
    pass

@export.command()
@click.argument('path')
@click.option('--delimiter', default=';', help="delimitador")
@click.option('--encode', default='utf-8', help="delimitador")
@click.option('--bom', is_flag=True, help="agregar bom al archivo")
def convert(path, delimiter, encode, bom):
    """
    Convierte el csv que se pasa como parametro a lo que se seleccione.
    """
    csvfile = CSVFile(path)
    result = csvfile.export(encode=encode,
                            delimiter=delimiter,
                            with_bom=bom)
    click.echo(result)

printcsv.add_command(show)
export.add_command(convert)
cli = click.CommandCollection(sources=[printcsv, export])

if __name__ == '__main__':
    cli()


