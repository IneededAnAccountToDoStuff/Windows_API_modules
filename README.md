# Windows_API_modules
A few single-file modules to make life on Windows easer.

## clipboard_new.py
Handles the basic Windows API commands for clipboards, and converts them into simple dictionaries and bytes. Custom handler and delayed values are not handled.
Meant for freezing/restoring the clipboard state, and for pulling out text-ish data.

## win_stayon_API.py
Handles the basic WIndows API commands for keeping the screen on. It supports the `with` statement.

## wincurconapi.py
Before Windows 10, the default Windows console does not support ANSI escape codes. Instead, one must use custom Windows API calls to achieve similar effects.
So this program simplifies that into Python function calls. THat way the end user doesn't need to deal with the windows API.
