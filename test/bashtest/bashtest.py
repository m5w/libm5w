#!/usr/bin/env python3

# Copyright (C) 2018 Matthew Marting
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import stat
import subprocess
import unittest


def _chmod_px(path):
    """
    Make a file executable.

    This function changes the file mode bits of ``path`` just as the following
    example would.

    ::

        $ chmod +x <path>

    The ``p`` in the function's name stands for the ``+`` ("plus") in
    ``chmod +x``.

    :param path: the file's path
    :raises FileNotFoundError: if the file does not exist
    :raises PermissionError: if this process is not running as the file's owner
    """
    os.chmod(
        path,
        os.stat(path).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def run(executable_path, executable_text, args, *popenargs, **kwargs):
    """
    Make, run, and then remove a Bash script with ``srcdir`` in the ``PATH``.

    :param executable_path: the path of the Bash script to make
    :param executable_text: the Bash code to run after adding ``srcdir`` to the
        ``PATH``
    :param args: command-line arguments to pass to the Bash script
    :param popenargs: positional arguments to forward to ``subprocess.run``
    :param kwargs: keyword arguments to forward to ``subprocess.run``
    :returns: the return value of ``subprocess.run``
    :raises PermissionError: if a file of path ``executable_path`` already
        exists, and this process does not have write access to the file; this
        process does not have permission to resolve the path
        ``executable_path``; or a file of path ``executable_path`` does not
        exist, and this process does not have write access to the file's parent
        directory
    :raises Exception: if ``subprocess.run`` raises an exception
    """
    with open(executable_path, mode="w") as executable:
        executable.write(fr"""#!/usr/bin/env bash

PATH=\
"$srcdir"\
':'\
"$PATH"
{executable_text}""")

    _chmod_px(executable_path)
    p = subprocess.run([executable_path] + args, *popenargs, **kwargs)
    os.remove(executable_path)
    return p


class BashTestCase(unittest.TestCase):
    def _test(self, executable_path, executable_text, expected_returncode,
              expected_stdout, expected_stderr):
        p = run(
            executable_path,
            executable_text, [],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True)
        self.assertEqual(p.returncode, expected_returncode)
        self.assertEqual(p.stdout, expected_stdout)
        self.assertEqual(p.stderr, expected_stderr)
