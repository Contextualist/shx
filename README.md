# shx

[![PyPI version](https://img.shields.io/pypi/v/shx.svg)](https://pypi.org/project/shx)

> Inspired by [zx](https://github.com/google/zx)

```python
#!/usr/bin/env shx

await $"cat setup.py | grep name"

branch = await $("git branch --show-current", capture='o')
await $f"dep deploy --branch={branch}"

await gather(
  $"sleep 1; echo 1",
  $"sleep 2; echo 2",
  $"sleep 3; echo 3",
)

name = "foo bar"
await $f"mkdir /tmp/{Q(name)}"
```

(Take a look at [more examples](examples.md).)

`shx` makes your script writing experience better by taking the advantages of Python's sugary syntax, AsyncIO, and the extensive Python ecosystem. `shx` does three things:

1. Wrap `asyncio.create_subprocess_shell` around with a [syntax sugar](#about-the-subprocess-syntax). `await $"command"` returns an [`asyncio.subprocess.Process`](https://docs.python.org/3/library/asyncio-subprocess.html#asyncio.asyncio.subprocess.Process) instance; on non-zero return code, raise [`subprocess.CalledProcessError`](https://docs.python.org/3/library/subprocess.html#subprocess.CalledProcessError).
2. Provide a top-level async environment.
3. Preload commonly used imports and utilities. Currently, the imports are:

```Python
import asyncio
from asyncio import *
from pathlib import Path
from shlex import quote as Q
import shutil
```

> Note that `shx` does not perform quote escape automatically. Use function `Q` (alias of [`shlex.quote`](https://docs.python.org/3/library/shlex.html#shlex.quote)) to escape unsafe arguments.

## Install

```bash
pip install shx
```

## Settings and utility functions

Settings can either be [task local](contextvars.md) (e.g. `__.trace = True`) or per-command (e.g. `await $("echo 42", trace=True)`):

* `shell` (Default: `$(which bash)`): Shell to be used.
* `prefix` (Default: `set -euo pipefail;`): String to be prepended to a command.
* `trace` (Default: `True`): Display command if set to True. Same as `set -x` in bash.
* `capture` (Default: `False`): If set to True, capture stdout and stderr instead of displaying them. The captured strings will replace the `.stdout` and `.stderr` attributes of the `asyncio.subprocess.Process` instance returned. `await $("...", capture='o')` and `await $("...", capture='e')` are the aliases of `(await $("...", capture=True)).stdout` and `(await $("...", capture=True)).stderr`, respectively.

Attributes:

* `__.argv`: alias of `sys.argv`, a list of command line arguments
* `__.env`: alias of `os.environ`, a dict of environment variables

### `cd(cwd: str)`

Change working directory to `cwd`. Same as the task local settings, the changes are only effective within the current task.

### `question(prompt: str)`

[`input()`](https://docs.python.org/3/library/functions.html#input) with `KeyboardInterrupt` handling.


## About the subprocess syntax

No magic, no meta-programming, and no hacking, whatsoever. Prior execution, the script is [tokenized](https://docs.python.org/3/library/tokenize.html), and the following replacements occur:

* "str prefix" `$"command"` -> `SHX("command")`
* "function" `$("command", k1=v1, ...)` -> `SHX("command", k1=v1, ...)`

where `SHX` is an async function wrapping around `asyncio.create_subprocess_shell`.
