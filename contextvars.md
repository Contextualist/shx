## How does task local var work?

```Python
#!/usr/bin/env shx

__.trace = False
cd("/tmp")

async def _inner():
    __.trace = True
    cd("a")
    assert __.cwd == Path("/tmp/a") and __.trace is True

# The coroutine in a different task get a copy of context vars
await asyncio.create_task(_inner())
assert __.cwd == Path("/tmp") and __.trace is False

# The coroutines in the same task share one set of context vars
await _inner()
assert __.cwd == Path("/tmp/a") and __.trace is True
```

When you are running multiple tasks concurrently, you don't want the settings in one task affect other tasks. That's why the `__` setttings are task local (context) variables instead of global variables. Whenever a task is spawned, it inherits a *copy* of context varibles from its parent task, so that any modification since then will not affect the parent task's variables, nor the sibling task's.

This is implemented on top of Python's [`contextvars`](https://docs.python.org/3/library/contextvars.html#asyncio-support) module.
