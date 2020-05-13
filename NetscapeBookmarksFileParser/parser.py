import html
import warnings

from NetscapeBookmarksFileParser import *
from NetscapeBookmarksFileParser.exceptions import *


def attribute_extractor(inside: str) -> dict:
    """
    Extracts the attributes and its values and
    put them in a dictionary
    :param inside: The inside of the tag, just the attributes
    :return: dictionary with the attributes and its values as string
    """
    attributes = dict()
    attribute = ""
    value = ""
    in_value = False
    in_icon = False  # prevents padding cause an infinite loop
    for i in range(len(inside)):
        if (inside[i].isspace() or inside[i] == '\n') and not in_value:
            continue
        elif inside[i] == '=' and not in_value:
            in_value = True
        elif not in_value:
            attribute += inside[i]
        elif in_value:
            if inside[i] == '"' and inside[i - 1] == '=' and not in_icon:
                if attribute == 'ICON':
                    in_icon = True
                continue
            elif inside[i] == '"':
                in_icon = False
                in_value = False
            if not in_value:
                attributes[attribute] = value
                attribute = ""
                value = ""
                continue
            else:
                value += inside[i]
    return attributes


def doc_type_extractor(tag: str) -> str:
    """
    Verifies if the <!DOCTYPE> tag is correct.
    Prints an warning if it doesn't match the expected
    :param tag: <!DOCTYPE> tag's line
    :return: the conten of the tag (the doc type)
    """
    start = tag.find('<') + len('<!DOCTYPE ')
    end = tag.find('>')
    content = tag[start:end]
    if content != 'NETSCAPE-Bookmark-file-1':
        warnings.warn(
            'This does not look like a Netscape Bookmark File'
            ' make sure it is a valid Bookmark File that was'
            ' exported from a browser'
        )
    return content[:]


def folder_tag_extractor(tag: str) -> BookmarkFolder:
    """
    Makes a BookmarkFolder with the
    <H3> tag info
    :param tag: <H3> tag
    :return: BookmarkFolder with the tag info
    """
    start = tag.find('<') + 7
    end = tag[start:].find('>') + start
    attributes = attribute_extractor(tag[start:end])
    name_start = end + 1
    name_end = (len(tag) - 1) - 4
    bookmark_folder = BookmarkFolder()
    bookmark_folder.name = html.unescape(tag[name_start:name_end])
    bookmark_folder.add_date_unix = int(attributes.get('ADD_DATE', '0'))
    bookmark_folder.last_modified_unix = int(attributes.get('LAST_MODIFIED', 0))
    bookmark_folder.personal_toolbar = bool(attributes.get('PERSONAL_TOOLBAR_FOLDER', None) == 'true')
    return bookmark_folder


def shortcut_tag_extractor(tag: str, comment='') -> BookmarkShortcut:
    """
    Makes an BookmarkShortcut (or one of its subclasses, rare)
    with the info of the <A> tag, the comment (<DD> tag) is
    passed a part
    :param tag: <A> tag
    :param comment: <DD> tag, if exists
    :return: BookmarkShortcut (or one of the subclasses, rare) with the <A> tag info and comment
    """
    start = tag.find('<') + 6
    end = tag[start:].find('>') + start
    attributes = attribute_extractor(tag[start:end])
    name_start = end + 1
    name_end = (len(tag) - 1) - 3
    bookmark_entry = BookmarkShortcut()
    if attributes.get('FEED', '') == "true":
        bookmark_entry = BookmarkFeed()
        bookmark_entry.feed_url = attributes.get('FEEDURL', '')
    if attributes.get('WEBSLICE', '') == "true":
        bookmark_entry = BookmarkWebSlice()
        if attributes.get('ISLIVEPREVIEW', '') == 'true':
            bookmark_entry.is_live_preview = True
        bookmark_entry.preview_size = attributes.get('PREVIEWSIZE', '')
    bookmark_entry.name = html.unescape(tag[name_start:name_end])
    bookmark_entry.href = attributes.get('HREF', '')
    bookmark_entry.add_date_unix = int(attributes.get('ADD_DATE', '0'))
    bookmark_entry.last_modified_unix = int(attributes.get('LAST_MODIFIED', '0'))
    bookmark_entry.last_visit_unix = int(attributes.get('LAST_VISIT', '0'))
    bookmark_entry.private = int(attributes.get('PRIVATE', '0'))
    bookmark_entry.tags = attributes.get('TAGS', '').split(',')
    if bookmark_entry.tags == ['']:
        bookmark_entry.tags = []
    icon_uri = attributes.get('ICON_URI', '')
    if len(icon_uri) != 0:
        if 'fake-favicon-uri' in icon_uri[:17]:
            bookmark_entry.icon_url_fake = True
        else:
            bookmark_entry.icon_url = icon_uri
    bookmark_entry.icon_base64 = attributes.get('ICON', '')
    bookmark_entry.comment = comment
    return bookmark_entry


def shortcut_handler(line: int, a_tag: str, dd_tag: str = '') -> BookmarkShortcut:
    """
    Handles shortcuts in the bookmark tree
    :param line: the line number of the <A> tag
    :param a_tag: the <A> tag
    :param dd_tag: the <DD> tag
    :return: BookmarkShortcut (or one of its subclasses, rare) with the <A> and <DD> tag info
    """
    if '<A' not in a_tag or '</A>' not in a_tag:
        warnings.warn('"A" tag missing in shortcut item at line ' + str(line + 1))
    return shortcut_tag_extractor(a_tag, dd_tag)


def folder_handler(line: int, h3_tag: str, body: list) -> BookmarkFolder:
    """
    Handles folders in the bookmark tree. Puts the position number
    of the items and creates the bookmark tree. It's called recursively
    :param line: the line number of the <H3> tag
    :param h3_tag: the <H3> tag
    :param body: the body of the folder, from <DL><p> to </Dl><p> tag
    :return: BookmarkFolder with all the info and its tree
    """
    if '<H3' not in h3_tag or '</H3>' not in h3_tag:
        warning_ = '"H3" tag missing in folder item at line ' + str(line + 1)
        warnings.warn(warning_)
    bookmark_folder = folder_tag_extractor(h3_tag)

    if len(body) != 0:
        i = 1

        while i < len(body):

            if '<DT><A' in body[i]:
                dd_tag = ''
                if '<DD>' in body[i + 1]:
                    dd_tag = body[i + 1]
                item = shortcut_handler(line + i, body[i], dd_tag)
                item.num = len(bookmark_folder.items)
                item.parent = bookmark_folder
                bookmark_folder.items.append(item)
                bookmark_folder.shortcuts.append(item)

            elif '<DT><H3' in body[i]:
                if '<DL><p>' not in body[i + 1]:
                    subfolder_empty = folder_handler(line=i, h3_tag=body[i], body=[''])
                    subfolder_empty.num = len(bookmark_folder.items)
                    subfolder_empty.parent = bookmark_folder
                    bookmark_folder.items.append(subfolder_empty)
                    bookmark_folder.children.append(subfolder_empty)
                    i += 1
                    continue

                elif '</DL><p>' in body[i + 2]:
                    subfolder_empty = folder_handler(line=i, h3_tag=body[i], body=[''])
                    subfolder_empty.num = len(bookmark_folder.items)
                    subfolder_empty.parent = bookmark_folder
                    bookmark_folder.items.append(subfolder_empty)
                    bookmark_folder.children.append(subfolder_empty)
                    i += 2
                    i += 1
                    continue

                elif '</DL><p>' not in body[i + 2]:
                    body_start = i + 1
                    i += 2
                    tag_counter = 1
                    while tag_counter != 0 and i < len(body):
                        if '<DL><p>' in body[i]:
                            tag_counter += 1
                        if '</DL><p>' in body[i]:
                            tag_counter -= 1
                        if tag_counter == 0:
                            break
                        i += 1
                    if tag_counter != 0:
                        exception_message = 'Closing "DL" tag expected. Opening at line ' + str(i + 1)
                        raise TagNotPresentException(exception_message)
                    body_end = i + 1
                    subfolder = folder_handler(body_start - 1, body[body_start - 1], body[body_start:body_end])
                    subfolder.num = len(bookmark_folder.items)
                    subfolder.parent = bookmark_folder
                    bookmark_folder.items.append(subfolder)
                    bookmark_folder.children.append(subfolder)
            elif '</DL><p>' not in body[i]:
                non_parsed[line + i] = body[i]
            i += 1

    return bookmark_folder


def parse(netscape_bookmarks_file: NetscapeBookmarksFile):
    """
    Responsible to start parsing, getting metadata information
    and start the folder recursion
    :param netscape_bookmarks_file: a NetscapeBookMarkFile
    :return: the NetscapeBookMarkFile, but parsed
    """
    line_num = 0
    file = netscape_bookmarks_file
    lines = netscape_bookmarks_file.html.splitlines()

    while '<' not in lines[line_num]:
        line_num += 1

    if not line_num < len(lines):
        warnings.warn('Empty file/string')

    root_name = ''
    while '<DL><p>' not in lines[line_num] and line_num < len(lines):
        if not file.doc_type and '<!DOCTYPE' in lines[line_num]:
            file.doc_type = doc_type_extractor(lines[line_num])
        elif not file.http_equiv_meta and '<META' in lines[line_num]:
            start = lines[line_num].find('<') + len('<META')
            end = lines[line_num].rfind('>')
            attributes = attribute_extractor(lines[line_num][start:end])
            file.http_equiv_meta = attributes.get('HTTP-EQUIV', '')
            file.content_meta = attributes.get('CONTENT', '')
        elif not file.title and '<TITLE>' in lines[line_num]:
            start = lines[line_num].find('<TITLE>') + len('<TITLE>')
            end = lines[line_num].rfind('</TITLE>')
            file.title = lines[line_num][start:end]
        elif not file.bookmarks.name and '<H1>' in lines[line_num]:
            start = lines[line_num].find('<H1>') + len('<H1>')
            end = lines[line_num].rfind('</H1>')
            h1 = lines[line_num][start:end]
            root_name = h1
        else:
            non_parsed[line_num] = lines[line_num]
        line_num += 1

    if line_num > len(lines):
        warnings.warn('Root bookmarks folder not found')
        return file

    body_start = line_num
    tag_counter = 0
    while line_num < len(lines):
        if '<DL><p>' in lines[line_num]:
            tag_counter += 1
        if '</DL><p>' in lines[line_num]:
            tag_counter -= 1
        if tag_counter == 0:
            break
        line_num += 1
    else:
        raise TagNotPresentException('Root bookmarks folder body end tag ("</DL><p>") not found')
    body_end = line_num

    pseud_h3_tag = '<DT><H3>' + file.bookmarks.name + '</H3>'
    file.bookmarks = folder_handler(body_start - 1, pseud_h3_tag, lines[body_start:body_end + 1])
    file.bookmarks.name = root_name
    return file


def add_parser(cls):
    """
    adds the parse functions to
    NetscapeBookmarksFile
    """
    cls.parse = parse
    return cls


add_parser(NetscapeBookmarksFile)  # enables parse usage
