# Copyright (c) 2025 Alex M. M.
# Distributed under the terms of the BSL-1.0 License.
# SPDX-License-Identifier: BSL-1.0

import argparse
import subprocess
import sys
from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path
from typing import Generator


class Status(IntEnum):
    SUCCESS = 0
    ERROR = 1


@dataclass
class Arguments:
    src: list[Path]
    clangformat: str
    dry: bool


def _parse_arguments(args: list[str]) -> Arguments:
    parser = argparse.ArgumentParser(
        description="Recursively runs clang-format on C and C++ source code"
    )

    parser.add_argument("src", type=Path, nargs="+", help="Directories to format files in")

    parser.add_argument(
        "--clang-format",
        type=str,
        nargs="?",
        default="clang-format",
        const="clang-format",
        help="clang-format binary to use",
    )

    parser.add_argument(
        "-d",
        "--dry-run",
        action=argparse.BooleanOptionalAction,
        help="Do not actually format.",
    )

    parsed = parser.parse_args(args)

    return Arguments(
        src=parsed.src, clangformat=parsed.clang_format, dry=parsed.dry_run
    )


_SOURCE_FILES = [
    ".c",
    ".C",
    ".cpp",
    ".cc",
    ".cxx",
    ".h",
    ".hpp",
    ".hh",
]


def _walk_source_files(path: Path) -> Generator[Path, None, None]:
    for p in path.iterdir():
        if p.is_dir():
            yield from _walk_source_files(p)

        if p.suffix in _SOURCE_FILES:
            yield p.resolve()


def _run_clang_format(clangformat: str, path: Path) -> None:
    subprocess.check_output(
        [clangformat, "--style=file", "-i", path], shell=False
    )


def main(args: list[str]) -> Status:
    parsed = _parse_arguments(args)

    for src in parsed.src:
        try:
            for p in _walk_source_files(src):
                print(f"Formatting {p}")

                _run_clang_format(parsed.clangformat, p)

        except FileNotFoundError:
            print(
                f"Error: Unable to find `{src}`. Perhaps you misspelt it?",
                file=sys.stderr,
            )

            return Status.ERROR

    print("Completed.")

    return Status.SUCCESS
