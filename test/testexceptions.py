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

import os.path
import unittest

import bashtest.bashtest


class TestExceptions(bashtest.bashtest.BashTestCase):
    def test_die(self):
        executable_path = os.path.join(os.path.curdir, "test_die")
        self._test(
            executable_path,
            r"""
. exceptions.bash || exit 2

main() {
  m5w::exceptions::die && exit 3
}

main
""",
            expected_returncode=1,
            expected_stdout="",
            expected_stderr=f"{executable_path}: ")
        self._test(
            executable_path,
            r"""
. exceptions.bash || exit 2

main() {
  m5w::exceptions::die 'error\n' && exit 3
}

main
""",
            expected_returncode=1,
            expected_stdout="",
            expected_stderr=f"{executable_path}: error\n")
        self._test(
            executable_path,
            r"""
. exceptions.bash || exit 2

main() {
  unset var
  m5w::exceptions::die 'error\n' -v var && exit 3
  [[ -z ${var+x} ]] || exit 4
}

main
""",
            expected_returncode=0,
            expected_stdout="",
            expected_stderr=f"{executable_path}: error\n")
        self._test(
            executable_path,
            r"""
. exceptions.bash

main() {
  m5w::exceptions::die 'error\n' 'foo' && exit 3
}

main
""",
            expected_returncode=1,
            expected_stdout="",
            expected_stderr=f"{executable_path}: error\n")
        self._test(
            executable_path,
            r"""
. exceptions.bash

main() {
  m5w::exceptions::die '%s\n' 'error' && exit 3
}

main
""",
            expected_returncode=1,
            expected_stdout="",
            expected_stderr=f"{executable_path}: error\n")

    def test_warn(self):
        executable_path = os.path.join(os.path.curdir, "test_warn")
        self._test(
            executable_path,
            r"""
. exceptions.bash || exit 2

main() {
  m5w::exceptions::warn || exit 3
}

main
""",
            expected_returncode=0,
            expected_stdout="",
            expected_stderr=f"{executable_path}: ")
        self._test(
            executable_path,
            r"""
. exceptions.bash || exit 2

main() {
  m5w::exceptions::warn 'warning\n' || exit 3
}

main
""",
            expected_returncode=0,
            expected_stdout="",
            expected_stderr=f"{executable_path}: warning\n")
        self._test(
            executable_path,
            r"""
. exceptions.bash || exit 2

main() {
  unset var
  m5w::exceptions::warn 'warning\n' -v var || exit 3
  [[ -z ${var+x} ]] || exit 4
}

main
""",
            expected_returncode=0,
            expected_stdout="",
            expected_stderr=f"{executable_path}: warning\n")
        self._test(
            executable_path,
            r"""
. exceptions.bash

main() {
  m5w::exceptions::warn 'warning\n' 'foo' || exit 3
}

main
""",
            expected_returncode=0,
            expected_stdout="",
            expected_stderr=f"{executable_path}: warning\n")
        self._test(
            executable_path,
            r"""
. exceptions.bash

main() {
  m5w::exceptions::warn '%s\n' 'warning' || exit 3
}

main
""",
            expected_returncode=0,
            expected_stdout="",
            expected_stderr=f"{executable_path}: warning\n")


if __name__ == "__main__":
    unittest.main()
