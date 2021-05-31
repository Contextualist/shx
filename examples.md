The following is a more involved example that uploads files while calculating their checksum.

```python
#!/usr/bin/env shx
__.trace = False
__.capture = 'o' # capture stdout by default

*files, dest = __.argv[1:]

async def checksum(files):
    rs = await gather(*($f"sha1sum {f}" for f in sorted(files)))
    return (r.strip().split() for r in rs)

# You can run async functions along with commands
_, cs_names = await gather(
    $(f"echo scp {' '.join(files)} {dest}", capture=False), # We want to display scp's progress bar ...
    checksum(files), # ... while capturing the checksum output for last.
)

print("sha1sum records:")
maxlen = max(map(len, files))
for cs, name in cs_names:
    print(f"{name.ljust(maxlen)} {cs}")

question("Delete files (Enter) or abort (^C)?") # Question could be used as a user checkpoint.
[Path(x).unlink() for x in files]
print("Done!")
```

The following demonstrates how to limit the maximum number of concurrency with AsyncIO. This snippet down-samples all wav files in a directory, while limiting 32 processes to run at any time.

```python
#!/usr/bin/env shx
__.trace = False

sema = Semaphore(32) # max concurrence

async def runone(fi):
    async with sema:
        await $f'sox {fi} -r 16000 wavs-16k/{fi.name} &> /dev/null'

await gather(*map(runone, Path('wavs-raw/').glob('*.wav')))
```
