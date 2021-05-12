from .shx import *
from .shx import __
__.capture = True
__.env["BASH_ENV"] = ""
X = SHX

import pytest
pytestmark = pytest.mark.asyncio

async def test_capture():
    hello = (await X("echo Error >&2; echo Hello")).stderr.strip()
    assert int((await X(f"echo {hello} | wc -c")).stdout) == 6

async def test_env():
    __.env["FOO"] = "foo"
    assert (await X("echo $FOO")).stdout == "foo\n"

async def test_quote():
    greeting = '"quota\'" & pwd'
    assert (await X(f"echo {Q(greeting)}")).stdout == f"{greeting}\n"
    foo = "hi; ls"
    assert int((await X(f"echo {Q(foo)} | wc -l")).stdout) == 1
    bar = 'bar"";baz!$#^$\'&*~*%)({}||\\/'
    assert (await X(f"echo {Q(bar)}")).stdout.strip() == bar
    __.env["FOO"] = "hi; exit 1"
    await X("echo $FOO")

async def test_exception():
    try:
        p = await X("cat /dev/not_found | sort")
    except CalledProcessError as e:
        p = e
    assert p.returncode == 1
