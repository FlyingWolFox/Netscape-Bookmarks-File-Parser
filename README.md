# Netscape Bookmarks File Parser

This is a parser for the Netscape Bookmarks file format, which generated by browsers 
when exporting bookmarks to html. It parses the file and deliver you an object 
representing the file with the bookmark structure of folders and shortcuts as 
objects too. The folder tree can be navigated by the "." notation. This also can
create a file too (like reverse parsing)

## Installation

Run in your command line (might need to run as administrator on Windows):
 ```bash
pip install git+https://github.com/FlyingWolFox/Netscape-Bookmarks-File-Parser.git
```
To update add the `--upgrade` flag at the end

## How to use

Import the classes and the parser. If you want to create a file, import the creator
 ```python
from NetscapeBookmarksFileParser import *
from NetscapeBookmarksFileParser import parser   # if you want to parse a file
from NetscapeBookmarksFileParser import creator  # if you want to create a file
```
Create a the NetscapeBookmarksFile `NetscapeBookmarkFile(bookmarks)`, being bookmarks 
the opened file or a string with the content. Then call `parse()` to parse the file. 
If you want to create the file call `create_file()`. To know about the classes
that the parser and the creator will work with, see the [wiki Classes section](https://github.com/FlyingWolFox/Netscape-Bookmarks-File-Parser/wiki/Code-Documentation#classes) 

## Notice about this parser

The parser will play like a browser and will ignore most error,
warning some tags missing. But if a folder has a body opening, but not a body closing,
an exception will be raised. Since Netscape Bookmarks File is commonly generated by
browsers when exporting bookmarks in html, such warning and exception shouldn't be
common. This parser was built on top of
[Microsoft's documentation on the Netscape File Format](https://docs.microsoft.com/en-us/previous-versions/windows/internet-explorer/ie-developer/platform-apis/aa753582(v=vs.85)?redirectedfrom=MSDN)
mainly, but also from file examples [here](https://sixtwothree.org/posts/homesteading-a-decades-worth-of-shared-links),
[here](https://stackoverflow.com/questions/38029954/parse-a-netscape-style-bookmarks-html-file-into-nested-array),
[here](https://gist.github.com/jgarber623/cdc8e2fa1cbcb6889872),
[here](https://www.npmjs.com/package/netscape-bookmarks) and my own browser exports
(`test\test.html` is one of them).
Some more uncommon attributes and items may not be supported, I tried to support to support
the common ones and some uncommon that may still be used. Look at the
[Attributes Supported](https://github.com/FlyingWolFox/Netscape-Bookmarks-File-Parser/wiki/The-Parser#attributes-supported)
and 
[Items Supported](https://github.com/FlyingWolFox/Netscape-Bookmarks-File-Parser/wiki/The-Parser#items-supported)
sections in the wiki. If you want to know more about how a file has to be accepted by te parser look at the
[Netscape Bookmarks File Format page](https://github.com/FlyingWolFox/Netscape-Bookmarks-File-Parser/wiki/Netscape-Bookmarks-File-Format)
in the wiki

## Notice about the creator

The creator is the parser in reverse. If you parse a file and create it again, if all
lines are valid, the files will be equal. You can see this with test.html and
created_file.html, both in /test/, the first was parsed, then the creation
process created the second. Look at the [wiki Creator page]() to know more about the
creator

## About legacy support

Due to the Netscape Bookmark file format not having an official standard, many things
of this parser was got by file examples in the internet (see the [Nestcape Bookmarks File format](https://github.com/FlyingWolFox/Netscape-Bookmarks-File-Parser/wiki/Netscape-Bookmarks-File-Format)
and [The parser](https://github.com/FlyingWolFox/Netscape-Bookmarks-File-Parser/wiki/The-Parser)
in the wiki).
This has legacy support for some types of items that aren't in use today. These are:
- Feed: Probably RSS feeds, just some attributes following the Microsoft's Documentation
- Web Slices: "Live bookmarks". They showed a piece of the page you saved. Extinct but in the Microsoft's Documentation.
If you want more details look at the [Legacy section](https://github.com/FlyingWolFox/Netscape-Bookmarks-File-Parser/wiki/The-Parser#about-legacybasic-support)
in the wiki

## Help
- If you would like to report a bug or ask a question please [open an issue](https://github.com/FlyingWolFox/Netscape-Bookmarks-File-Parser/issues/new).
- If you would like to help this project, you can open a Pull Request
- If you want more information about this project, have a look at the [wiki](https://github.com/FlyingWolFox/Netscape-Bookmarks-File-Parser/wiki)
