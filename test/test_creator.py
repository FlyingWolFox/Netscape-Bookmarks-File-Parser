import unittest
from NetscapeBookmarksFileParser import NetscapeBookmarksFileCreator as C
import NetscapeBookmarksFileParser as P


class TestAttributePrinter(unittest.TestCase):
    def test_single(self):
        arg = dict()
        arg['ATTRIBUTE'] = 'value'
        out = C.attribute_printer(arg)
        exp = ' ATTRIBUTE="value"'
        self.assertEqual(exp, out)

    def test_double(self):
        arg = dict()
        arg['ATTRIBUTE1'] = 'value1'
        arg['ATTRIBUTE2'] = 'value2'
        out = C.attribute_printer(arg)
        exp = ' ATTRIBUTE1="value1" ATTRIBUTE2="value2"'
        self.assertEqual(exp, out)

    def test_empty_value(self):
        arg = dict()
        arg['EMPTY'] = ''
        out = C.attribute_printer(arg)
        exp = ' EMPTY'
        self.assertEqual(exp, out)

    def test_empty_value_double_last(self):
        arg = dict()
        arg['EMPTY'] = ''
        arg['ATTRIBUTE'] = 'value'
        out = C.attribute_printer(arg)
        exp = ' EMPTY ATTRIBUTE="value"'
        self.assertEqual(exp, out)

    def test_empty_value_double_first(self):
        arg = dict()
        arg['ATTRIBUTE'] = 'value'
        arg['EMPTY'] = ''
        out = C.attribute_printer(arg)
        exp = ' ATTRIBUTE="value" EMPTY'
        self.assertEqual(exp, out)


class TestMetaCreator(unittest.TestCase):
    def test_default(self):
        out = C.meta_creator()
        exp = list()
        exp.append('<!DOCTYPE NETSCAPE-Bookmark-file-1>')
        exp.append('<!-- This is an automatically generated file.')
        exp.append('\tIt will be read and overwritten.')
        exp.append('\tDO NOT EDIT! -->')
        exp.append('<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">')
        exp.append('<TITLE>Bookmarks</TITLE>')
        exp.append('<H1>Bookmarks</H1>')
        self.assertEqual(exp, out)

    def test_non_default(self):
        out = C.meta_creator('x', ['y', 'z'], 'B', 'b')
        exp = '''<!DOCTYPE x>
        <!-- This is an automatically generated file.
             It will be read and overwritten.
             DO NOT EDIT! -->
        <META HTTP-EQUIV="y" CONTENT="z">
        <TITLE>B</TITLE>
        <H1>b</H1>
        '''


class TestHttpVerifier(unittest.TestCase):
    def test_without(self):
        arg = 'duckduckgo.com'
        out = C.http_verifier(arg)
        exp = 'http://duckduckgo.com'
        self.assertEqual(exp, out)

    def test_with_it(self):
        arg = 'https://duckduckgo.com'
        out = C.http_verifier(arg)
        exp = arg
        self.assertEqual(exp, out)


class TestEntryCreator(unittest.TestCase):
    def test_empty(self):
        arg = P.BookmarkEntry()
        out = C.entry_creator(arg)
        exp = list()
        exp.append('<DT><A></A>')
        self.assertEqual(exp, out)

    def test_entry_common(self):
        arg = P.BookmarkEntry()
        arg.href = 'https://duckduckgo.com'
        arg.name = 'Duck Duck Go'
        out = C.entry_creator(arg)
        exp = list()
        exp.append('<DT><A HREF="https://duckduckgo.com">Duck Duck Go</A>')
        self.assertEqual(exp, out)

    def test_add_date(self):
        arg = P.BookmarkEntry()
        arg.href = 'https://duckduckgo.com'
        arg.name = 'Duck Duck Go'
        arg.add_date_unix = 1515
        out = C.entry_creator(arg)
        exp = list()
        exp.append('<DT><A HREF="https://duckduckgo.com" ADD_DATE="1515">Duck Duck Go</A>')
        self.assertEqual(exp, out)

    def test_comment(self):
        arg = P.BookmarkEntry()
        arg.href = 'https://duckduckgo.com'
        arg.name = 'Duck Duck Go'
        arg.comment = 'Duck Duck Go'
        out = C.entry_creator(arg)
        exp = list()
        exp.append('<DT><A HREF="https://duckduckgo.com">Duck Duck Go</A>')
        exp.append('<DD>Duck Duck Go')
        self.assertEqual(exp, out)

    def test_feed(self):
        arg = P.BookmarkFeed()
        arg.feed_url = 'test.rss'
        out = C.entry_creator(arg)
        exp = list()
        exp.append('<DT><A FEED="true" FEEDURL="test.rss"></A>')
        self.assertEqual(exp, out)

    def test_web_slice(self):
        arg = P.BookmarkWebSlice()
        arg.is_live_preview = True
        arg.preview_size = "100 x 200"
        out = C.entry_creator(arg)
        exp = list()
        exp.append('<DT><A WEBSLICE="true" ISLIVEPREVIEW="true" PREVIEWSIZE="100 x 200"></A>')
        self.assertEqual(exp, out)


class TestFolderCreator(unittest.TestCase):
    def test_empty(self):
        arg = C.BookmarkFolder()
        out = C.folder_creator(arg)
        exp = list()
        exp.append('<DT><H3></H3>')
        exp.append('<DL><p>')
        exp.append('</DL><p>')
        self.assertEqual(exp, out)

    def test_item(self):
        arg = C.BookmarkFolder()
        arg.name = 'Folder'
        entry = C.BookmarkEntry()
        entry.name = 'Duck Duck Go'
        entry.href = 'https://duckduckgo.com'
        arg.items.append(entry)
        out = C.folder_creator(arg)
        exp = list()
        exp.append('<DT><H3>Folder</H3>')
        exp.append('<DL><p>')
        exp.append('\t' + C.entry_creator(entry)[0])
        exp.append('</DL><p>')
        self.assertEqual(exp, out)

    def test_folder(self):
        arg = C.BookmarkFolder()
        arg.name = 'Folder'
        folder = C.BookmarkFolder()
        folder.name = 'Subfolder'
        arg.items.append(folder)
        out = C.folder_creator(arg)
        exp = list()
        exp.append('<DT><H3>Folder</H3>')
        exp.append('<DL><p>')
        exp.append('\t<DT><H3>Subfolder</H3>')
        exp.append('\t<DL><p>')
        exp.append('\t</DL><p>')
        exp.append('</DL><p>')
        self.assertEqual(exp, out)

    def test_folder_and_item(self):
        arg = C.BookmarkFolder()
        arg.name = 'Folder'

        entry = C.BookmarkEntry()
        entry.name = 'Duck Duck Go'
        entry.href = 'https://duckduckgo.com'
        arg.items.append(entry)

        folder = C.BookmarkFolder()
        folder.name = 'Subfolder'
        folder.items.append(entry)
        arg.items.append(folder)

        out = C.folder_creator(arg)

        exp = list()
        exp.append('<DT><H3>Folder</H3>')
        exp.append('<DL><p>')
        exp.append('\t' + C.entry_creator(entry)[0])
        exp.append('\t<DT><H3>Subfolder</H3>')
        exp.append('\t<DL><p>')
        exp.append('\t\t' + C.entry_creator(entry)[0])
        exp.append('\t</DL><p>')
        exp.append('</DL><p>')

        self.assertEqual(exp, out)


class TestItemSorting(unittest.TestCase):
    def test_items(self):
        items = list()
        items.append(C.BookmarkEntry(num=2))
        items.append(C.BookmarkEntry(num=1))
        items.append(C.BookmarkEntry(num=0))
        file = C.NetscapeBookmarksFile()
        file.bookmarks = C.BookmarkFolder()
        file.bookmarks.items.extend(items)
        file.sort_items()
        exp = list()
        exp.append(C.BookmarkEntry(num=0))
        exp.append(C.BookmarkEntry(num=1))
        exp.append(C.BookmarkEntry(num=2))
        self.assertEqual(exp, file.bookmarks.items)

    def test_folder(self):
        items = list()
        items.append(C.BookmarkEntry(num=2))
        folder = C.BookmarkFolder(num=1)
        folder.items.extend([C.BookmarkEntry(num=1), C.BookmarkEntry(num=0)])
        items.append(folder)
        items.append(C.BookmarkEntry(num=0))
        file = C.NetscapeBookmarksFile()
        file.bookmarks = C.BookmarkFolder()
        file.bookmarks.items.extend(items)
        file.sort_items()
        exp = list()
        exp.append(C.BookmarkEntry(num=0))
        folder = C.BookmarkFolder(num=1)
        folder.items.extend([C.BookmarkEntry(num=0), C.BookmarkEntry(num=1)])
        exp.append(folder)
        exp.append(C.BookmarkEntry(num=2))
        self.assertEqual(exp, file.bookmarks.items)


class TestFileCreation(unittest.TestCase):
    def test_empty(self):
        arg = C.NetscapeBookmarksFile()
        out = arg.create_file()
        exp = list()
        exp.append('<!DOCTYPE NETSCAPE-Bookmark-file-1>')
        exp.append('<!-- This is an automatically generated file.')
        exp.append('\tIt will be read and overwritten.')
        exp.append('\tDO NOT EDIT! -->')
        exp.append('<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">')
        exp.append('<TITLE>Bookmarks</TITLE>')
        exp.append('<H1>Bookmarks</H1>')
        exp.append('<DL><p>')
        exp.append('</DL><p>')
        self.assertEqual(exp, out)

    def test_root_empty(self):
        arg = C.NetscapeBookmarksFile()
        arg.bookmarks = P.BookmarkFolder()
        out = arg.create_file()
        exp = list()
        exp.append('<!DOCTYPE NETSCAPE-Bookmark-file-1>')
        exp.append('<!-- This is an automatically generated file.')
        exp.append('\tIt will be read and overwritten.')
        exp.append('\tDO NOT EDIT! -->')
        exp.append('<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">')
        exp.append('<TITLE>Bookmarks</TITLE>')
        exp.append('<H1>Bookmarks</H1>')
        exp.extend(C.folder_creator(arg.bookmarks)[1:])
        self.assertEqual(exp, out)

    def test_meta(self):
        arg = C.NetscapeBookmarksFile()
        arg.bookmarks = P.BookmarkFolder()
        arg.title = 'Title'
        arg.content_meta = 'Content'
        arg.http_equiv_meta = 'Equiv'
        arg.doc_type = 'Doc'
        out = arg.create_file()
        exp = list()
        exp.append('<!DOCTYPE Doc>')
        exp.append('<!-- This is an automatically generated file.')
        exp.append('\tIt will be read and overwritten.')
        exp.append('\tDO NOT EDIT! -->')
        exp.append('<META HTTP-EQUIV="Equiv" CONTENT="Content">')
        exp.append('<TITLE>Title</TITLE>')
        exp.append('<H1>' + arg.bookmarks.name + '</H1>')
        exp.extend(C.folder_creator(arg.bookmarks)[1:])
        self.assertEqual(exp, out)


if __name__ == '__main__':
    unittest.main()
