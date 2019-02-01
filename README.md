# General
cli and package to work with csv files. 

it gives you a quick look about the files and it can convert and transform encode file, separator fields, and quotes types.

## Install

```
    git clone http://github.com/nuxion/csvtools
    cd csvtools
```

From pip, is the same: 

```
pip3 install git+https://github.com/nuxion/csvtools
```

## Build and distribute

```
    python setup.py build
    python setup.py sdist
```

## Cli usage

```
csvtool --help
Usage: csvtool [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  convert  Convierte el csv que se pasa como parametro a...
  show

```

*convert*

```
csvtool convert --help
Usage: csvtool convert [OPTIONS] PATH

  Convierte el csv que se pasa como parametro a lo que se seleccione.

Options:
  --delimiter TEXT  delimitador
  --encode TEXT     delimitador
  --bom             agregar bom al archivo
  --help            Show this message and exit.

```
*show*
```
csvtool show --help
Usage: csvtool show [OPTIONS] PATH

Options:
  -l, --lines INTEGER  El numero de lineas que se quiere mostrar
  --help               Show this message and exit.

```
