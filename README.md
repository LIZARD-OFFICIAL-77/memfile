# memfile

*Nix SYSTEMS ONLY!

Python `open()` wrapper that stores file content in ram (ramdisk)

# Usage

```python
from memfile import memoryopen

## Simply replace built-in open() with memoryopen() 

with memoryopen("myfile.txt","w") as file:
    file.write("Hello, world!")

with memoryopen("rawbytes","wb") as file:
    file.write(b"Hello, world!")

# OR #
file = memoryopen("myfile.txt","w")
file.write("Hello, world!")
file.close()

file = memoryopen("rawbytes","wb")
file.write(b"Hello, world!")
file.close()
## Exact behaviour of open(), but the contents are stored in RAM.
```

You _can_ use `memoryopen()` like the built-in `open()` without a context manager, but you are **highly encouraged** to use context managers.

# How does it work?

It uses symlinks and sharedmemory (`/dev/shm`).

We first generate a name for the "real" file, and store it in /dev/shm. Then, create a symlink as the intended directory. Then do any of the operations on the real file.

Example:

```python
with memoryopen("myfile.txt","w") as file:
    file.write("Hello, world!"*30)

with open("myfile2.txt","w") as file:
    file.write("Hello, world!"*30)
```

The reason I multiplied the string is because I wanted to show the difference.

As you can see, `myfile.txt` (`memoryopen()`) uses 38 bytes of disk space, while `myfile2.txt` (built-in `open()`) uses **390** bytes.

That is because, the file is stored in RAM, or more precisely, `/dev/shm/`. The 38 bytes are the symlink.

```bash
-rw-rw-r-- 1 lizard lizard  390 12. Feb 22:43 myfile2.txt
lrwxrwxrwx 1 lizard lizard   38 12. Feb 22:42 myfile.txt -> /dev/shm/myfile.txt-memoryopen71020452
```

# Why was this created

Because my new project needs to use as little disk space as possible, it will be run on an SBC with more ram than disk space.

# Dangling links / Memory leaks

This library lets you "leak" memory. The tmpfs files that are created must be properly removed using 

```python
memfile.remove("<filepath>")
```

or

```python
with memoryopen("<file>","w") as file: # MUST BE WRITE MODE.
    file.unlink()
```

These 2 clean up a memfile properly, by deleting both the tmpfs file, _and_ the symlink. If you don't delete the file using these methods, it will not only "leak" memory, once you reboot, the file is gone, because it was in RAM. Why is it "leaking" and not leaking memory? well, because the memory is still accessible, you just have to free it in a cursed way. You have to go to /dev/shm, and look through the files and manually delete the memfile if you delete the symlink.