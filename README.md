# wslpath-compdb

Converts all Windows paths in a `compile_commands.json` to WSL compatible ones.

# Prerequisites

This script must be run on WSL, which must have the `wslpath` utility.

The JSON database must be in "arguments" format, not "command" (see
[example](https://clang.llvm.org/docs/JSONCompilationDatabase.html#format)).

# Usage

A `compile_commands.json` can be generated using [compiledb][], which can be
installed as follows:
```sh
pip install git+https://github.com/shyun3/compiledb@support-cl-clang-cl
```
This fork and branch contains fixes for some issues in the main repo, see
[#120][issue-120] and [#124][issue-124].

To generate the database, the following can be used when in the directory of a
makefile:
```sh
make -Bnwk all | compiledb -f -o /path/to/compile_commands.json
```
This will create a `compile_commands.json` at the specified path.

Convert the JSON database using the script:
```sh
python3 wslpath_compdb.py -i /path/to/compile_commands.json
```
Note how the in-place option is used to modify the file.

[compiledb]: https://github.com/shyun3/compiledb/tree/support-cl-clang-cl
[issue-120]: https://github.com/nickdiego/compiledb/issues/120
[issue-124]: https://github.com/nickdiego/compiledb/issues/124
