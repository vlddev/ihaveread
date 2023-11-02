

# Distribute

## pyinstaller

Run `pyinstaller -F ui_app.py` to distribute application

## PEX

`pex -o ../ihaveread.pex --python-shebang='/usr/bin/env python3' -D . PySimpleGUI -e ui_app`

Database must be in `data/ihaveread.db` relatively to `ihaveread.pex`

__TODO__ make database path configurable
