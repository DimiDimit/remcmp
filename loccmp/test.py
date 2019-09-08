import logging
import os
import tempfile
import typing
import unittest

import loccmp
import remcmp


def test_with_contents(case: unittest.TestCase, cont1: str, cont2: str, check: typing.Dict[str, int]) -> None:
    with tempfile.TemporaryDirectory() as temp1, tempfile.TemporaryDirectory() as temp2:
        with open(os.path.join(temp1, "file.txt"), "w") as tempf1, \
                open(os.path.join(temp2, "file.txt"), "w") as tempf2:
            tempf1.write(cont1)
            tempf2.write(cont2)
        stats = remcmp.cmp_dirs(loccmp.create_local_path(temp1, True),
                                loccmp.create_local_path(temp2, True))
        case.assertTrue(remcmp.test_utils.check_stats(stats, check))


class TestLocCmp(unittest.TestCase):
    def setUp(self) -> None:
        logging.root.setLevel(logging.CRITICAL)
    
    def test_same(self):
        c = "This is a text document. It's the same in both directories."
        test_with_contents(self, c, c, {"eq": 1})
    
    def test_diff(self):
        c = "This is a text document. It's in the {} directory."
        test_with_contents(self, c.format("first"), c.format("second"), {"not_eq": 1})
    
    def test_miss(self):
        with tempfile.TemporaryDirectory() as temp1, tempfile.TemporaryDirectory() as temp2:
            open(os.path.join(temp1, "file1"), "x").close()
            open(os.path.join(temp2, "file2"), "x").close()
            
            os.mkdir(os.path.join(temp1, "dir1"))
            os.mkdir(os.path.join(temp2, "dir2"))
            
            open(os.path.join(temp1, "fd1"), "x").close()
            os.mkdir(os.path.join(temp2, "fd1"))
            
            os.mkdir(os.path.join(temp1, "fd2"))
            open(os.path.join(temp2, "fd2"), "x").close()
            stats = remcmp.cmp_dirs(loccmp.create_local_path(temp1, True), loccmp.create_local_path(temp2, True))
            self.assertTrue(remcmp.test_utils.check_stats(stats, {
                "file_ex_one": 2, "dir_ex_one": 2, "file_dir": 2, "dir_file": 2}))


if __name__ == '__main__':
    unittest.main()
