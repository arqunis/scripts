# Copyright (c) 2025 Alex M. M.
# Distributed under the terms of the BSL-1.0 License.
# SPDX-License-Identifier: BSL-1.0

import sys

from do_clang_format.main import main as real_main

_MSG = """INTERNAL ERROR:
Program encountered a fatal error it could not recover from.
Please provide the following error to the developer of this Software:
"""


def main() -> int:
    try:
        return real_main(sys.argv[1:]).value
    except Exception as e:
        print(
            _MSG,
            file=sys.stderr,
        )

        raise e
