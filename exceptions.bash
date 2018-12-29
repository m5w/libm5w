#!/usr/bin/env bash

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

if [[ -z ${M5W_EXCEPTIONS_BASH+x} ]]; then
  readonly M5W_EXCEPTIONS_BASH=

  # Print the program's name.
  #
  # This function should be called only by `_warn`, which has its own
  # preconditions.
  #
  # The `prog` in this function's name is inspired by the argument `prog` to
  # the constructor of Python's class `argparse.ArgumentParser`.
  m5w::exceptions::_get_the_prog() {
    echo "${BASH_SOURCE[-1]}"
  }

  # Print an error message, which includes the program's name, to `stderr`.
  #
  # The first argument concatenated to the program's name is passed as the
  # first argument to `printf`.  The rest of the arguments are forwarded to
  # `printf`, which interprets them as positional arguments.
  #
  # This function should be called only by `die` or `warn`, which both should
  # be called only within functions.  Otherwise, this file's name will be
  # printed instead of the program's name.
  m5w::exceptions::_warn() {
    printf -- "$(m5w::exceptions::_get_the_prog)"': '"$@" >&2
  }

  # Print an error message, and return a non-zero status.
  #
  # Note that this function does not exit the program.  It should be called as
  # in the following example to propagate errors.
  #
  #     m5w::exceptions::die 'error\n' || return 1
  #
  # This function forwards all arguments to `_warn`.
  #
  # This function's name is inspired by the Perl function of the same name.
  m5w::exceptions::die() {
    m5w::exceptions::_warn "$@"
    return 1
  }

  # Print a warning message.
  #
  # This function forwards all arguments to `_warn`.
  #
  # This function's name is inspired by the Perl function of the same name.
  m5w::exceptions::warn() {
    m5w::exceptions::_warn "$@"
  }
fi
