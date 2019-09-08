import typing

import remcmp
import remcmp.remcmpd


def check_stats(stats: typing.Dict[str, remcmp.remcmpd.Stat], check: typing.Dict[str, int]) -> bool:
    seen = 0
    for n, s in stats.items():
        c = check.get(n)
        if c is None:
            if s.times != 0:
                return False
        elif s.times != c:
            return False
        else:
            seen += 1
    return seen == len(check)
