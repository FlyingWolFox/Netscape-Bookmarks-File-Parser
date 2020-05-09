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
        exp = '''<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
\tIt will be read and overwritten.
\tDO NOT EDIT! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
'''
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


class TestEntryCreator(unittest.TestCase):
    def test_empty(self):
        arg = P.BookmarkEntry()
        out = C.entry_creator(arg)
        exp = '<DT><A></A>'
        self.assertRaises()


@unittest.skip
class TestFolderCreator(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)


@unittest.skip
class TestFileCreation(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
