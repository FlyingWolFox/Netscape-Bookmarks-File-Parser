from NetscapeBookmarksFileParser import *


def attribute_printer(attributes: dict):
    string = ''
    for attribute in attributes:
        string += ' '
        string += attribute
        if not attributes[attribute] == '':
            string += '="'
            string += attributes[attribute]
            string += '"'

    return string


def meta_creator(doctype='NETSCAPE-Bookmark-file-1', meta=None, title='Bookmarks', h1='Bookmarks'):
    if meta is None:
        meta = ["Content-Type", "text/html; charset=UTF-8"]
    string = ''
    string += '<!DOCTYPE ' + doctype + '>\n'
    string += warning
    string += '<META HTTP-EQUIV="' + meta[0] + '" CONTENT="' + meta[1] + '">\n'
    string += '<TITLE>' + title + '</TITLE>\n'
    string += '<H1>' + h1 + '</H1>\n'
    return string


def entry_creator(entry: BookmarkEntry):
    pass


def folder_creator(folder: BookmarkFolder):
    pass


class NetscapeBookmarksFile(object):
    __metaclass__ = NetscapeBookmarksFile

    def parse_file(self):
        pass

    def create_file(self):
        pass


def get_netscape_bookmarks_file():
    return NetscapeBookmarksFile()
