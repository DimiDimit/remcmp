# remcmp
Extensible program to compare local and remote directories.

Since it uses the `fs` module, any extensions (such as [`fs.smbfs`](https://pypi.org/project/fs.smbfs/)) can be used simply by installing them, and [you can write your own](https://docs.pyfilesystem.org/en/latest/extension.html).
## Installation
You can install it using `pip`:
```bash
pip3 install remcmp
``` 
Or download it directly from [PyPI](https://pypi.org/project/remcmp/).
## Usage
```
$ usage: remcmp [-h] [-c] [-lf LOG_FILE] [-ll LOG_LEVEL] dir1 dir2

Remote compare directories.

positional arguments:
  dir1                  First directory to compare
  dir2                  Second directory to compare

optional arguments:
  -h, --help            show this help message and exit
  -c, --no-color        Do not output colorful text
  -lf LOG_FILE, --log-file LOG_FILE
                        Log into a file. This disables colored output
  -ll LOG_LEVEL, --log-level LOG_LEVEL
                        Which logging level to use. SUMMARY can be used to
                        only show the summary. By default this is INFO for
                        terminal and DEBUG for log file
```