"""
Wrapper for built-in open() that uses RAM for file contents. Only works on *Nix platforms.
Copyright (C) 2025 LIZARD-OFFICIAL-77

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from __future__ import annotations

from random import randint
from pathlib import Path

import os

## INTELLISENSE / AUTO COMPLETIONS / TYPE HINTS ##

from io import (
    BufferedRandom, 
    BufferedReader, 
    BufferedWriter, 
    FileIO,
    TextIOWrapper,
)

from typing import ( 
    IO,
    Any,
    BinaryIO,
    Iterable,
    Union,
    TYPE_CHECKING
)

if TYPE_CHECKING:
    from _typeshed import WriteableBuffer, StrOrBytesPath

BuiltinIO = Union[BufferedRandom, BufferedReader, BufferedWriter, FileIO, TextIOWrapper, BinaryIO, IO[Any]]

##################################################

class PlatformError(BaseException): pass

def compat_check():
    if not Path("/dev/shm").is_dir():
        raise PlatformError("/dev/shm is not a directory. Please make sure that the shared memory folder exists.")

def remove(path: StrOrBytesPath):
    os.remove(os.path.realpath(path))
    os.remove(path)


compat_check()
class __memoryopen:
    def __init__(self,dir_: str,op_: str = "r",*args,**kwargs):        
        self._dir = dir_
        self._args = args
        self._opmode = op_
        self._kwargs = kwargs
        self.__open()

    def __enter__(self):
        ctx = self.__file
        ctx.unlink = self.unlink
        return ctx
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.__file.close()
        return None
    
    def __open(self):
        """
        Process memoryopen() request.
        """
        self.__dir = self._dir.rstrip("/")
        self.__dir = os.path.split(self.__dir)[-1]
        self.__dir = os.path.join("/dev/shm",self.__dir)
        self.__dir = self.__dir.rstrip("/")
        
        if Path(self._dir).is_file() and not Path(self._dir).is_symlink():
            raise IOError("Attempted to use memoryopen() on a regular file.")
        
        if not Path(self._dir).is_symlink():
            self.__dir = self.__dir+"-memoryopen"+str(randint(11111111,99999999))
            os.symlink(self.__dir,self._dir)
        else:
            if Path(self._dir).is_dir():
                raise IOError("Attempted to use memoryopen() on a folder.")

            if (
                os.path.realpath(self._dir).startswith("/dev/shm/") 
                and 
                "-memoryopen" in os.path.realpath(self._dir)
            ):
                self.__dir = os.path.realpath(self._dir)
            else:
                raise IOError("Attempted to use memoryopen() on a symlink not created with memoryopen().")    
        
        self.__file: builtin_io = open(self.__dir,self._opmode,*self._args,*self._kwargs)
    
    def unlink(self):
        """"""        
        if self._opmode != "w":
            raise IOError("Incorrect mode for unlinking. Please use write mode")
        self.__file.close()
        remove(self._dir)
        return True
    # Non-context manager support
    def __getattr__(self, name):
        return self.__file.__getattr__["name"]
    def isatty(self):
        return self.__file.isatty()
    def detach(self):
        return self.__file.detach()
    def fileno(self):
        return self.__file.fileno()
    def flush(self):
        return self.__file.flush()
    def writable(self):
        return self.__file.writable()
    def write(self,s: str):
        return self.__file.write(s)
    def writelines(self,lines: Iterable[str]):
        return self.__file.writelines(lines)
    def read(self,size: int = -1):
        return self.__file.read(size)
    def readlines(self,hint: int = -1):
        return self.__file.readlines(hint)
    def readline(self,size: int = -1):
        return self.__file.readline(size)
    def tell(self):
        return self.__file.tell()
    def truncate(self,pos: int | None = None):
        return self.__file.truncate(pos)
    def reconfigure(self,*args,**kwargs):
        return self.__file.reconfigure(*args,**kwargs)
    def seek(self,cookie: int, whence: int = 0):
        return self.__file.seek(cookie,whence)
    def seekable(self):
        return self.__file.seekable()
    def readinto(self,buffer: WriteableBuffer):
        return self.__file.readinto(buffer)
    def readinto1(self,buffer: WriteableBuffer):
        return self.__file.readinto1(buffer)
    def peek(self,size: int = -1):
        return self.__file.peek(size)
    def read1(self,size: int = -1):
        return self.__file.read1(size)
    def readable(self):
        return self.__file.readable()
    def close(self):
        return self.__file.close()



def memoryopen(*args,**kwargs) -> builtin_io:
    """        
    Backwards-compatible wrapper for built-in open() that uses RAM for file contents.
    Only works on *Nix platforms.
        
    Raises IOError if:
        *memoryopen()* is used on a file/symlink that was not created by *memoryopen()*
        *memoryopen()* is used on a folder (just like built-in *open()*)
    
    open() built-in:
    
    Open file and return a stream.  Raise OSError upon failure.

    file is either a text or byte string giving the name (and the path
    if the file isn't in the current working directory) of the file to
    be opened or an integer file descriptor of the file to be
    wrapped. (If a file descriptor is given, it is closed when the
    returned I/O object is closed, unless closefd is set to False.)

    mode is an optional string that specifies the mode in which the file
    is opened. It defaults to 'r' which means open for reading in text
    mode.  Other common values are 'w' for writing (truncating the file if
    it already exists), 'x' for creating and writing to a new file, and
    'a' for appending (which on some Unix systems, means that all writes
    append to the end of the file regardless of the current seek position).
    In text mode, if encoding is not specified the encoding used is platform
    dependent: locale.getencoding() is called to get the current locale encoding.
    (For reading and writing raw bytes use binary mode and leave encoding
    unspecified.) The available modes are:

    ========= ===============================================================
    Character Meaning
    --------- ---------------------------------------------------------------
    'r'       open for reading (default)
    'w'       open for writing, truncating the file first
    'x'       create a new file and open it for writing
    'a'       open for writing, appending to the end of the file if it exists
    'b'       binary mode
    't'       text mode (default)
    '+'       open a disk file for updating (reading and writing)
    ========= ===============================================================

    The default mode is 'rt' (open for reading text). For binary random
    access, the mode 'w+b' opens and truncates the file to 0 bytes, while
    'r+b' opens the file without truncation. The 'x' mode implies 'w' and
    raises an `FileExistsError` if the file already exists.

    Python distinguishes between files opened in binary and text modes,
    even when the underlying operating system doesn't. Files opened in
    binary mode (appending 'b' to the mode argument) return contents as
    bytes objects without any decoding. In text mode (the default, or when
    't' is appended to the mode argument), the contents of the file are
    returned as strings, the bytes having been first decoded using a
    platform-dependent encoding or using the specified encoding if given.

    buffering is an optional integer used to set the buffering policy.
    Pass 0 to switch buffering off (only allowed in binary mode), 1 to select
    line buffering (only usable in text mode), and an integer > 1 to indicate
    the size of a fixed-size chunk buffer.  When no buffering argument is
    given, the default buffering policy works as follows:

    * Binary files are buffered in fixed-size chunks; the size of the buffer
    is chosen using a heuristic trying to determine the underlying device's
    "block size" and falling back on `io.DEFAULT_BUFFER_SIZE`.
    On many systems, the buffer will typically be 4096 or 8192 bytes long.

    * "Interactive" text files (files for which isatty() returns True)
    use line buffering.  Other text files use the policy described above
    for binary files.

    encoding is the name of the encoding used to decode or encode the
    file. This should only be used in text mode. The default encoding is
    platform dependent, but any encoding supported by Python can be
    passed.  See the codecs module for the list of supported encodings.

    errors is an optional string that specifies how encoding errors are to
    be handled---this argument should not be used in binary mode. Pass
    'strict' to raise a ValueError exception if there is an encoding error
    (the default of None has the same effect), or pass 'ignore' to ignore
    errors. (Note that ignoring encoding errors can lead to data loss.)
    See the documentation for codecs.register or run 'help(codecs.Codec)'
    for a list of the permitted encoding error strings.

    newline controls how universal newlines works (it only applies to text
    mode). It can be None, '', '\n', '\r', and '\r\n'.  It works as
    follows:

    * On input, if newline is None, universal newlines mode is
    enabled. Lines in the input can end in '\n', '\r', or '\r\n', and
    these are translated into '\n' before being returned to the
    caller. If it is '', universal newline mode is enabled, but line
    endings are returned to the caller untranslated. If it has any of
    the other legal values, input lines are only terminated by the given
    string, and the line ending is returned to the caller untranslated.

    * On output, if newline is None, any '\n' characters written are
    translated to the system default line separator, os.linesep. If
    newline is '' or '\n', no translation takes place. If newline is any
    of the other legal values, any '\n' characters written are translated
    to the given string.

    If closefd is False, the underlying file descriptor will be kept open
    when the file is closed. This does not work when a file name is given
    and must be True in that case.

    A custom opener can be used by passing a callable as *opener*. The
    underlying file descriptor for the file object is then obtained by
    calling *opener* with (*file*, *flags*). *opener* must return an open
    file descriptor (passing os.open as *opener* results in functionality
    similar to passing None).

    open() returns a file object whose type depends on the mode, and
    through which the standard file operations such as reading and writing
    are performed. When open() is used to open a file in a text mode ('w',
    'r', 'wt', 'rt', etc.), it returns a TextIOWrapper. When used to open
    a file in a binary mode, the returned class varies: in read binary
    mode, it returns a BufferedReader; in write binary and append binary
    modes, it returns a BufferedWriter, and in read/write mode, it returns
    a BufferedRandom.

    It is also possible to use a string or bytearray as a file for both
    reading and writing. For strings StringIO can be used like a file
    opened in a text mode, and for bytes a BytesIO can be used like a file
    opened in a binary mode.
    """
    return __memoryopen(*args,**kwargs)


    
__all__ = [
    memoryopen,
    remove
]