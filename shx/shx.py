import asyncio
from asyncio import *
from pathlib import Path
from shlex import quote as Q
import shutil

from typing import Optional
from subprocess import CalledProcessError

async def run_subprocess(cmd: str, capture: Optional[bool], **kwargs) -> asyncio.subprocess.Process:
    dest = asyncio.subprocess.PIPE if capture else None
    s = await create_subprocess_shell(cmd, stdout=dest, stderr=dest, executable=__.shell, cwd=__.cwd, **kwargs)
    await s.wait()
    if capture:
        s.stdout = (await s.stdout.read()).decode() # should we assume unicode?
        s.stderr = (await s.stderr.read()).decode()
    if s.returncode:
        raise CalledProcessError(s.returncode, cmd, s.stdout, s.stderr)
    return s

def _deft(l, g):
    return l if l is not None else g

def SHX(cmd: str, prefix=None, trace=None, capture=None, **kwargs):
    if _deft(trace, __.trace):
        print(f"$ {cmd}")
    cmd = _deft(prefix, __.prefix) + cmd
    return run_subprocess(cmd, _deft(capture, __.capture), **kwargs)

try:
    from aiocontextvars import ContextVar
except ModuleNotFoundError:
    from contextvars import ContextVar
from sys import argv
from os import environ
class ROVar:
    def __init__(self, name, default):
        self.k, self.v = name, default
    def set(self, v):
        raise TypeError(f"{self.k} is immutable")
    def get(self):
        return self.v
_CVAR = dict(
    argv    =      ROVar("argv",    default=argv[1:]),
    env     =      ROVar("env",     default=environ),
    shell   = ContextVar("shell",   default=shutil.which("bash")),
    prefix  = ContextVar("prefix",  default="set -euo pipefail;"),
    trace   = ContextVar("trace",   default=True),
    capture = ContextVar("capture", default=False),
    cwd     = ContextVar("cwd",     default=None),
)
class CVar:
    def __getattr__(self, k):
        return _CVAR[k].get()
    def __setattr__(self, k, v):
        _CVAR[k].set(v)
__ = CVar()

def question(s="Proceed (Enter) or abort (^C)?"):
    try:
        return input(s)
    except KeyboardInterrupt:
        print()
        exit(0)

def cd(cwd: str):
    cwd = Path(cwd)
    if __.cwd is None or cwd.is_absolute():
        __.cwd = cwd
        return
    __.cwd = __.cwd.joinpath(cwd)

def _cmdstmt(s: str) -> str:
    from tokenize import tokenize, untokenize, ERRORTOKEN, STRING, NAME, OP
    from io import BytesIO
    result = []
    g = tokenize(BytesIO(s.encode('utf-8')).readline)  # tokenize the string
    post_et = False
    for toknum, tokval, _, _, _ in g:
        if toknum == ERRORTOKEN and tokval == '$':
            post_et = True
            toknum, tokval = NAME, 'SHX'
        elif post_et:
            post_et = False
            if toknum == STRING:
                result.extend([(OP, '('), (STRING, tokval), (OP, ')')])
                continue
            elif toknum == OP and tokval == '(':
                pass
            else:
                raise SyntaxError("'$' should be followed by a str or '('")
        result.append((toknum, tokval))
    return untokenize(result).decode('utf-8')

def main():
    snippet = Path(argv[1]).read_text()
    snippet = _cmdstmt(snippet)
    async def amain(snippet):
        exec(
            'async def __ex(): ' +
            ''.join(f'\n {l}' for l in snippet.split('\n'))
        )
        await locals()['__ex']()
    run(amain(snippet))
if __name__ == "__main__":
    main()
