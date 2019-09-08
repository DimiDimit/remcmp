# remcmp
Extensible program to compare local and remote directories.
## Installation
You can install it using `pip`:
```bash
pip3 install remcmp
``` 
Or download it directly from [PyPI](https://pypi.org/project/remcmp/).
## Usage
```
$ remcmp -h
usage: remcmp [-h] [-s] [-f] [-c] [-lf LOG_FILE] [-ll LOG_LEVEL]
              type1 dir1 type2 dir2

Remote compare directories.

positional arguments:
  type1                 Type of the first directory to compare
  dir1                  First directory to compare
  type2                 Type of the second directory to compare
  dir2                  Second directory to compare

optional arguments:
  -h, --help            show this help message and exit
  -s, --shallow         Don't compare if dates and sizes are equal
  -f, --files-only      Do not recurse into folders, only compare the files
  -c, --no-color        Do not output colorful text
  -lf LOG_FILE, --log-file LOG_FILE
                        Log into a file. This disables colored output
  -ll LOG_LEVEL, --log-level LOG_LEVEL
                        Which logging level to use. SUMMARY can be used to
                        only show the summary. By default this is INFO for
                        terminal and DEBUG for log file
```