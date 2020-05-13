import unittest
from NetscapeBookmarksFileParser import *
from NetscapeBookmarksFileParser import creator


class TestItemSorting(unittest.TestCase):
    def test_items(self):
        items = list()
        items.append(creator.BookmarkShortcut(num=2))
        items.append(creator.BookmarkShortcut(num=1))
        items.append(creator.BookmarkShortcut(num=0))
        file = creator.NetscapeBookmarksFile()
        file.bookmarks = creator.BookmarkFolder()
        file.bookmarks.items.extend(items)
        file.bookmarks.sort_items()
        exp = list()
        exp.append(creator.BookmarkShortcut(num=0))
        exp.append(creator.BookmarkShortcut(num=1))
        exp.append(creator.BookmarkShortcut(num=2))
        self.assertEqual(exp, file.bookmarks.items)

    def test_folder(self):
        items = list()
        items.append(creator.BookmarkShortcut(num=2))
        folder = creator.BookmarkFolder(num=1)
        folder.items.extend([creator.BookmarkShortcut(num=1), creator.BookmarkShortcut(num=0)])
        items.append(folder)
        items.append(creator.BookmarkShortcut(num=0))
        file = creator.NetscapeBookmarksFile()
        file.bookmarks = creator.BookmarkFolder()
        file.bookmarks.items.extend(items)
        file.bookmarks.sort_items()
        exp = list()
        exp.append(creator.BookmarkShortcut(num=0))
        folder = creator.BookmarkFolder(num=1)
        folder.items.extend([creator.BookmarkShortcut(num=0), creator.BookmarkShortcut(num=1)])
        exp.append(folder)
        exp.append(creator.BookmarkShortcut(num=2))
        self.assertEqual(exp, file.bookmarks.items)


if __name__ == '__main__':
    unittest.main()
