# copycat

Concatenate and copy files to clipboard.

Each file is prefixed with a comment containing its location.

Useful for providing AI tools with context about your codebase.

```bash
% copycat .vscode ./*.*
lines   filepath
30      .vscode/tasks.json
30      ./README.md
148     ./copycat.py
40      ./copycat.spec
10      ./requirements.txt
copied 263 lines to clipboard
```

# Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
.venv/bin/pyinstaller copycat.spec
cp -f dist/copycat /directory/to/bin/ # example: /usr/local/bin/
```

Alias to `cc` for convenience:
```bash
echo "alias cc='copycat'" >> ~/.zshrc
```

# Reference

```
usage: copycat [-h] [--version] [--no-copy] [--log LOG] [--log-level {1,2,3,4,5}] [--log-format {1,2,3}] [-v] [patterns ...]

Concatenate and copy files to clipboard.

positional arguments:
  patterns              File names, file paths, or glob patterns matching the files to concatenate. Defaults to current directory.

optional arguments:
  -h, --help            show this help message and exit
  --version             Show the version number and exit
  --no-copy             Do not copy results to clipboard and print instead.
  --log LOG             Log file to use. Defaults to stdout.
  --log-level {1,2,3,4,5}
                        Logging level. Defaults to 2. DEBUG=1 INFO=2 WARNING=3 ERROR=4 CRITICAL=5
  --log-format {1,2,3}  Logging format. Defaults to 3. 1='DATE TIME:LEVEL:MESSAGE' 2='LEVEL:MESSAGE' 3='MESSAGE'
  -v, --verbose         Sets `--log-level 1 --log-format 1`
```