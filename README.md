*You probably want to use `rsync` instead.*
# remcmp
Extensible program to compare local and remote directories.

Since it uses the `fs` module, any extensions (such as [`fs.smbfs`](https://pypi.org/project/fs.smbfs/)) can be used simply by installing them, and [you can write your own](https://docs.pyfilesystem.org/en/latest/extension.html).
## Installation
You can install it using `pip`:
```shell script
pip3 install remcmp
``` 
Or download it directly from [PyPI](https://pypi.org/project/remcmp/).
## Usage
```
$ remcmp -h
usage: remcmp.py [-h] [-f] [-c] [-lf LOG_FILE] [-ll LOG_LEVEL] dir1 dir2

Remote compare directories.

positional arguments:
  dir1                  First directory to compare
  dir2                  Second directory to compare

optional arguments:
  -h, --help            show this help message and exit
  -f, --files-only      Do not recurse into folders, only compare the files
  -c, --no-color        Do not output colorful text
  -lf LOG_FILE, --log-file LOG_FILE
                        Log into a file. This disables colored output
  -ll LOG_LEVEL, --log-level LOG_LEVEL
                        Which logging level to use. SUMMARY can be used to
                        only show the summary. By default this is INFO for
                        terminal and DEBUG for log file
```
## Exit codes
Each stat (e.g. `Equal`, `File only exists on one side`) has a flag. If it is encountered at least once then it is OR-ed with the exit code. E.g. `Directory only exists on one side` and `File only exists on one side`: `8 | 32 = 40`.
```
No stat: 0
Error: 1
Equal: 2
Not equal: 4
Directory only exists on one side: 8
Directory is file on the other side: 16
File only exists on one side: 32
File is directory on the other side: 64
```
