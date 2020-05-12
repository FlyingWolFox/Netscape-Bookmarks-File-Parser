from NetscapeBookmarksFileParser import *

# warning at the top of the file
warning = list()
warning.append('<!-- This is an automatically generated file.')
warning.append('     It will be read and overwritten.')
warning.append('     DO NOT EDIT! -->')


def http_verifier(url):
    """
    verifies if the url starts with
    http:// or https://. If not, http://
    is put in the start of url
    :param url: url to be verified
    :return: url with http://
    """
    if not any(x in url[:10] for x in ['http://', 'https://']):
        return 'http://' + url
    else:
        return url


def attribute_printer(attributes: dict):
    """
    Creates a string representing the
    attributes received, ready to be
    put in a tag
    :param attributes: dictionary with attributes and its value
    :return: string with all attributes formatted
    """
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
    """
    creates the start of the file
    :param doctype: the doc type
    :param meta: the list with both meta attributes
    :param title: title of the file
    :param h1: "name of the root folder"
    :return: the meta with lines as a list, without \n
    """
    if meta is None:
        meta = ["Content-Type", "text/html; charset=UTF-8"]
    ret = list()
    ret.append('<!DOCTYPE ' + doctype + '>')
    ret.extend(warning)
    ret.append('<META HTTP-EQUIV="' + meta[0] + '" CONTENT="' + meta[1] + '">')
    ret.append('<TITLE>' + title + '</TITLE>')
    ret.append('<H1>' + h1 + '</H1>')
    return ret


def shortcut_creator(shortcut: BookmarkShortcut):
    """
    creates a shortcut A tag from a BookmarkShortcut. If a
    value is the default, it won't be printed
    :param shortcut: the BookmarkShortcut
    :return: the list with two lines: first the A tag and the second the DD, if comment is present
    """
    attributes = dict()
    if shortcut.feed:
        attributes['FEED'] = "true"
        attributes['FEEDURL'] = shortcut.feed_url
    elif shortcut.web_slice:
        attributes['WEBSLICE'] = "true"
        attributes['ISLIVEPREVIEW'] = str(shortcut.is_live_preview).lower()
        attributes['PREVIEWSIZE'] = shortcut.preview_size
    elif shortcut.href:
        attributes['HREF'] = shortcut.href

    if shortcut.add_date_unix:
        attributes['ADD_DATE'] = str(shortcut.add_date_unix)
        if shortcut.last_modified_unix:
            attributes['LAST_MODIFIED'] = str(shortcut.last_modified_unix)
            if shortcut.last_visit_unix:
                attributes['LAST_VISIT'] = str(shortcut.last_visit_unix)

    if shortcut.private:
        attributes['PRIVATE'] = str(shortcut.private)

    if shortcut.tags:
        attributes['TAGS'] = ','.join(shortcut.tags)

    if shortcut.icon_url_fake or shortcut.icon_url:
        fake = 'fake-favicon-uri:' if shortcut.icon_url_fake else ''
        icon_url = shortcut.href if shortcut.icon_url else shortcut.icon_url
        attributes['ICON_URI'] = fake + icon_url

    if shortcut.icon_base64:
        attributes['ICON'] = shortcut.icon_base64

    ret = list()
    ret.append('<DT><A' + attribute_printer(attributes) + '>' + shortcut.name + '</A>')
    if shortcut.comment:
        ret.append('<DD>' + shortcut.comment)

    return ret


def folder_creator(folder: BookmarkFolder):
    """
    Creates a folder H3 tag from a BookmarkFolder. If a
    value is the default, it won't be printed
    :param folder: BookmarkFolder to be created
    :return: the list containing the H3 tag and folder tree
    """
    attributes = dict()
    if folder.add_date_unix:
        attributes['ADD_DATE'] = str(folder.add_date_unix)
        if folder.last_modified_unix:
            attributes['LAST_MODIFIED'] = str(folder.last_modified_unix)

    if folder.personal_toolbar:
        attributes['PERSONAL_TOOLBAR_FOLDER'] = "true"

    ret = list()
    ret.append('<DT><H3' + attribute_printer(attributes) + '>' + folder.name + '</H3>')
    ret.append('<DL><p>')
    for item in folder.items:
        if isinstance(item, BookmarkShortcut):
            entry = shortcut_creator(item)
            for i in range(len(entry)):
                entry[i] = '    ' + entry[i]
            ret.extend(entry)

        elif isinstance(item, BookmarkFolder):
            folder = folder_creator(item)
            for i in range(len(folder)):
                folder[i] = '    ' + folder[i]
            ret.extend(folder)

    ret.append('</DL><p>')
    return ret


def create_file(netscape_bookmarks_file: NetscapeBookmarksFile, print_meta=True):
    """
    creates the file. netscape_bookmarks_file.html is the string containing
     the html ready to be writen in a file. The lines of the string are
     return as list
    :param netscape_bookmarks_file: the file to be created as html
    :param print_meta: if the start of the file should be included
    :return: lines of html as list
    """
    lines = list()
    file = netscape_bookmarks_file
    if print_meta:
        if file.doc_type:
            meta = [file.http_equiv_meta, file.content_meta]
            lines.extend(meta_creator(file.doc_type, meta, file.title, file.bookmarks.name))
        else:
            lines.extend(meta_creator())

    if file.bookmarks:
        lines.extend(folder_creator(file.bookmarks)[1:])

    lines.append('')  # add final line break

    for line in lines:
        file.html += line + '\n'

    return lines


def split_items(folder: BookmarkFolder, recursive=True):
    """
    splits the items list into children and shortcuts
    :param folder: folder to have items splitted
    :param recursive: if subfolders should have their items splitted
    :return: nothing
    """
    for item in folder.items:
        if isinstance(item, BookmarkShortcut):
            folder.shortcuts.append(item)

        elif isinstance(item, BookmarkFolder):
            folder.children.append(item)
            if recursive:
                split_items(item)


def sort_items(folder: BookmarkFolder, recursive=True):
    """
    sort the items list by the num of each item.
     split_items() is ran before sorting happens
    :param folder: folder to have its items sorted
    :param recursive: if subfolders will have their items sorted too
    :return: nothing
    """
    def sort_by_number(e):
        return e.num

    folder.items.sort(key=sort_by_number)
    split_items(folder)
    if recursive:
        for child in folder.children:
            sort_items(child)


def add_creator(cls):
    """
    adds creator functions
    to NetscapeBookmarksFile
    :param cls: NetscapeBookmarksFile class
    :return: nothing
    """
    def to_class(func):
        """
        gets a folder utility functions
        and converts them into methods
        :param func: function to be converted
        :return: the method
        """
        def method(netscape_bookmarks_file: NetscapeBookmarksFile, folder: BookmarkFolder = None, recursive=True):
            if folder is None:
                folder = netscape_bookmarks_file.bookmarks
            return func(folder, recursive)
        method.__doc__ = func.__doc__

        return method

    cls.create_file = create_file
    cls.split_items = to_class(split_items)
    cls.sort_items = to_class(sort_items)


add_creator(NetscapeBookmarksFile)  # enables creator usage
