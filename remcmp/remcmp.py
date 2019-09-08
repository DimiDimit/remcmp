import argparse
import copy
import filecmp
import importlib
import logging
import sys
import typing

import colorama

import remcmp
from remcmp import Stat


base_stats: typing.Dict[str, Stat] = {
    "eq"         : Stat("Equal", "Equal"),
    "not_eq"     : Stat("Not equal", "Not equal"),
    "dir_ex_one" : Stat("Directory only exists on one side", "Directory {} exists in {} but not in {}"),
    "dir_file"   : Stat("Directory is file on the other side", "Directory {} in {} is a file in {}"),
    "file_ex_one": Stat("File only exists on one side", "File {} exists in {} but not in {}"),
    "file_dir"   : Stat("File is directory on the other side", "File {} in {} is a directory in {}")
}

colored = True

logging.addLevelName(45, "SUMMARY")
SUMMARY = logging.getLevelName("SUMMARY")


def join(*a: any, sep: str = " ") -> str:
    return sep.join([str(o) for o in a])


def log(*a: any, level: int = logging.INFO, sep: str = " ", prefix: str = "", suffix: str = "") -> None:
    logging.log(level, prefix + join(*a, sep = sep) + suffix)


def log_colored(*a: any, level: int = logging.INFO, color: any = colorama.Fore.RED,
                sep: str = " ", prefix: str = "", suffix: str = "") -> None:
    log(*a, level = level, sep = sep, prefix = (str(color) if colored else "") + prefix,
        suffix = suffix + (str(colorama.Style.RESET_ALL) if colored else ""))


def report_stat(stats: typing.Dict[str, Stat], stat: str, f: any, dir1: any, dir2: any, level: int = logging.ERROR,
                color: any = colorama.Fore.RED):
    s = stats[stat]
    s.times += 1
    log_colored(s.explanation.format(f, dir1, dir2), level = level, color = color)


def cmp_dirs(dir1: remcmp.Directory, dir2: remcmp.Directory, files_only: bool = False, shallow: bool = False,
             stats: typing.Optional[typing.Dict[str, Stat]] = None) -> typing.Dict[str, Stat]:
    if stats is None:
        stats = copy.deepcopy(base_stats)
    log_colored("Comparing directory", dir1, "with", dir2, level = logging.INFO, color = colorama.Fore.BLUE)
    dir1lf = dir1.list()
    dir1l = [p.name for p in dir1lf]
    dir2lf = dir2.list()
    dir2l = [p.name for p in dir2lf]
    for f in dir1lf:
        fe = f.name in dir2l
        d2sp: remcmp.Path = dir2.get_sub_path(f.name) if fe else None
        if isinstance(f, remcmp.Directory):
            if files_only:
                continue
            if not fe:
                report_stat(stats, "dir_ex_one", f, dir1, dir2)
                continue
            if not isinstance(d2sp, remcmp.Directory):
                report_stat(stats, "dir_file", f, dir1, dir2)
                continue
            cmp_dirs(f, d2sp, files_only, shallow, stats)
        else:
            if not fe:
                report_stat(stats, "file_ex_one", f, dir1, dir2)
                continue
            if not isinstance(d2sp, remcmp.File):
                report_stat(stats, "file_dir", f, dir1, dir2)
                continue
            f: remcmp.File
            log_colored("Comparing", f.path, "with", d2sp.path, suffix = "...", color = colorama.Fore.CYAN)
            if f.tmp_file_msg is not None:
                log(f.tmp_file_msg, "1...")
            with f.get_tmp_file() as temp1:
                if d2sp.tmp_file_msg is not None:
                    log(d2sp.tmp_file_msg, "2...")
                with d2sp.get_tmp_file() as temp2:
                    log("Comparing...")
                    if filecmp.cmp(temp1.name, temp2.name, shallow):
                        report_stat(stats, "eq", f, dir1, dir2, level = logging.INFO, color = colorama.Fore.GREEN)
                    else:
                        report_stat(stats, "not_eq", f, dir1, dir2, logging.INFO, color = colorama.Fore.RED)
    for f in dir2lf:
        nfe = f.name not in dir1l
        d1sp: remcmp.Path = dir1.get_sub_path(f.name) if not nfe else None
        if isinstance(f, remcmp.Directory):
            if nfe:
                report_stat(stats, "dir_ex_one", f, dir2, dir1)
            elif not isinstance(d1sp, remcmp.Directory):
                report_stat(stats, "dir_file", f, dir2, dir1)
        else:
            if nfe:
                report_stat(stats, "file_ex_one", f, dir2, dir1)
            elif not isinstance(d1sp, remcmp.File):
                report_stat(stats, "file_dir", f, dir2, dir1)
    return stats


def main():
    global colored
    colorama.init()
    
    argp = argparse.ArgumentParser(description = "Remote compare directories.")
    argp.add_argument('type1', help = "Type of the first directory to compare")
    argp.add_argument('dir1', help = "First directory to compare")
    argp.add_argument('type2', help = "Type of the second directory to compare")
    argp.add_argument('dir2', help = "Second directory to compare")
    argp.add_argument('-s', '--shallow', action = 'store_true',
                      help = "Don't compare if dates and sizes are equal")
    argp.add_argument('-f', '--files-only', action = 'store_true',
                      help = "Do not recurse into folders, only compare the files")
    argp.add_argument('-c', '--no-color', action = 'store_true',
                      help = "Do not output colorful text")
    argp.add_argument('-lf', '--log-file', help = "Log into a file. This disables colored output")
    argp.add_argument('-ll', '--log-level',
                      help = "Which logging level to use. SUMMARY can be used to only show the summary. "
                             "By default this is INFO for terminal and DEBUG for log file")
    
    args = argp.parse_args()
    colored = not args.no_color
    if args.log_file is not None:
        colored = False
        logging.basicConfig(filename = args.log_file, format = "%(asctime)s:%(levelname)s:%(message)s",
                            level = logging.getLevelName(
                                    args.log_level.upper()) if args.log_level is not None else logging.DEBUG)
    else:
        logging.basicConfig(format = "%(message)s", stream = sys.stdout, level = logging.getLevelName(
                args.log_level.upper()) if args.log_level is not None else logging.INFO)
    
    try:
        type1 = importlib.import_module(args.type1 + "cmp")
        type2 = importlib.import_module(args.type2 + "cmp")
    except ModuleNotFoundError as e:
        log_colored("Module", e.name, "not found!", level = logging.FATAL)
        sys.exit(1)
    stats = cmp_dirs(type1.create_path(args.dir1, True), type2.create_path(args.dir2, True), args.files_only)
    log(level = SUMMARY)
    log_colored("Summary:", level = SUMMARY, color = colorama.Fore.BLUE + colorama.Style.BRIGHT)
    for s in stats.values():
        if s.times <= 0:
            continue
        log(s.summary, ": ", s.times, sep = "", level = SUMMARY)


if __name__ == '__main__':
    main()
