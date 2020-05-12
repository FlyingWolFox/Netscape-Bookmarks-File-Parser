from NetscapeBookmarksFileParser import *

warning = list()
warning.append('<!-- This is an automatically generated file.')
warning.append('     It will be read and overwritten.')
warning.append('     DO NOT EDIT! -->')


def http_verifier(url):
    if not any(x in url[:10] for x in ['http://', 'https://']):
        return 'http://' + url
    else:
        return url


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
    ret = list()
    ret.append('<!DOCTYPE ' + doctype + '>')
    ret.extend(warning)
    ret.append('<META HTTP-EQUIV="' + meta[0] + '" CONTENT="' + meta[1] + '">')
    ret.append('<TITLE>' + title + '</TITLE>')
    ret.append('<H1>' + h1 + '</H1>')
    return ret


def shortcut_creator(entry):
    attributes = dict()
    if entry.feed:
        attributes['FEED'] = "true"
        attributes['FEEDURL'] = entry.feed_url
    elif entry.web_slice:
        attributes['WEBSLICE'] = "true"
        attributes['ISLIVEPREVIEW'] = str(entry.is_live_preview).lower()
        attributes['PREVIEWSIZE'] = entry.preview_size
    elif entry.href:
        attributes['HREF'] = entry.href

    if entry.add_date_unix:
        attributes['ADD_DATE'] = str(entry.add_date_unix)
        if entry.last_modified_unix:
            attributes['LAST_MODIFIED'] = str(entry.last_modified_unix)
            if entry.last_visit_unix:
                attributes['LAST_VISIT'] = str(entry.last_visit_unix)

    if entry.private:
        attributes['PRIVATE'] = str(entry.private)

    if entry.tags:
        attributes['TAGS'] = ','.join(entry.tags)

    if entry.icon_url_fake or entry.icon_url:
        fake = 'fake-favicon-uri:' if entry.icon_url_fake else ''
        icon_url = entry.href if entry.icon_url else entry.icon_url
        attributes['ICON_URI'] = fake + icon_url

    if entry.icon_base64:
        attributes['ICON'] = entry.icon_base64

    ret = list()
    ret.append('<DT><A' + attribute_printer(attributes) + '>' + entry.name + '</A>')
    if entry.comment:
        ret.append('<DD>' + entry.comment)

    return ret


def folder_creator(folder: BookmarkFolder):
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
    for item in folder.items:
        if isinstance(item, BookmarkShortcut):
            folder.entries.append(item)

        elif isinstance(item, BookmarkFolder):
            folder.children.append(item)
            if recursive:
                split_items(item)


def sort_items(folder: BookmarkFolder, recursive=True):
    def sort_by_number(e):
        return e.num

    folder.items.sort(key=sort_by_number)
    split_items(folder)
    if recursive:
        for child in folder.children:
            sort_items(child)


def add_creator(cls):
    def to_class(func):
        def method(netscape_bookmarks_file: NetscapeBookmarksFile, folder: BookmarkFolder = None, recursive=True):
            if folder is None:
                folder = netscape_bookmarks_file.bookmarks
            return func(folder, recursive)

        return method

    cls.create_file = create_file
    cls.split_items = to_class(split_items)
    cls.sort_items = to_class(sort_items)


add_creator(NetscapeBookmarksFile)
