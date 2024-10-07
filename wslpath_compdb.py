#!/usr/bin/env python3

import argparse
import json
import re
import subprocess
from typing import Any, Dict, List

CompileDb = List[Dict[str, Any]]


def run() -> None:
    arg_parser = argparse.ArgumentParser(
        description=(
            "Converts Windows paths in a JSON compilation database to WSL compatible"
            " ones"
        )
    )
    arg_parser.add_argument(
        "-i",
        "--in-place",
        default=False,
        action="store_true",
        help="Perform in-place conversion",
    )
    arg_parser.add_argument("file", help="Path to JSON file")

    args = arg_parser.parse_args()
    with open(args.file) as file:
        compdb = json.load(file)

    wsl_compdb = to_wsl_compdb(compdb)
    ser = json.dumps(wsl_compdb, indent=2)

    if args.in_place:
        with open(args.file, "w") as file:
            file.write(ser)
    else:
        print(ser)


def to_wsl_compdb(compdb: CompileDb) -> CompileDb:
    return [
        {
            "directory": wslpath_filter(obj["directory"]),
            "arguments": [wslpath_filter(arg) for arg in obj["arguments"]],
            "file": wslpath_filter(obj["file"]),
        }
        for obj in compdb
    ]


def wslpath_filter(arg: str) -> str:
    winpath_regex = re.compile(r"[A-Za-z]:[/\\].*$")
    convert = lambda match_obj: wslpath(match_obj.group())
    return winpath_regex.sub(convert, arg)


def wslpath(path: str) -> str:
    result = subprocess.run(
        ["wslpath", path], check=True, stdout=subprocess.PIPE, text=True
    )
    return result.stdout.rstrip("\n")


if __name__ == "__main__":
    run()
