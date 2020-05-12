import unittest
from NetscapeBookmarksFileParser import *
from NetscapeBookmarksFileParser import parser
from NetscapeBookmarksFileParser import creator


class TestCreatorEqualParsed(unittest.TestCase):
    def test(self):
        self.maxDiff = None
        with open('test.html') as real_file:
            file = NetscapeBookmarksFile(real_file)
            file.parse()
            file_created = file.create_file()
            with open('created_file.html', 'w') as created_file:
                created_file.write('\n'.join(file_created))

        with open('test.html') as real_file:
            with open('created_file.html') as created_file:
                real = real_file.read()
                created = created_file.read()
                self.assertEqual(real, created)


if __name__ == '__main__':
    unittest.main()
