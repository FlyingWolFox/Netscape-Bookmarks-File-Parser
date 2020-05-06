import unittest
import warnings

import NetscapeBookmarksFileParser as Parser

attribute_finder = Parser.attribute_finder
doc_type = Parser.doc_type
folder = Parser.folder
entry = Parser.entry
item_handler = Parser.item_handler
folder_handler = Parser.folder_handler
Folder = Parser.BookmarkFolder
Entry = Parser.BookmarkEntry
Feed = Parser.BookmarkFeed
WebSlice = Parser.BookmarkWebSlice
File = Parser.NetscapeBookmarksFile
parse = Parser.parse


# noinspection SpellCheckingInspection
class TestAttributeFinder(unittest.TestCase):
    def test_meta(self):
        argument = ' HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8"'
        output = attribute_finder(argument)
        expected_output = dict()
        expected_output['HTTP-EQUIV'] = 'Content-Type'
        expected_output['CONTENT'] = 'text/html; charset=UTF-8'
        self.assertDictEqual(output, expected_output)

    def test_folder(self):
        argument = 'ADD_DATE="1548340605" LAST_MODIFIED="1587068423" PERSONAL_TOOLBAR_FOLDER="true"'
        output = attribute_finder(argument)
        expected_output = dict()
        expected_output['ADD_DATE'] = '1548340605'
        expected_output['LAST_MODIFIED'] = '1587068423'
        expected_output['PERSONAL_TOOLBAR_FOLDER'] = 'true'
        self.assertDictEqual(output, expected_output)

    # noinspection SpellCheckingInspection,SpellCheckingInspection
    def test_item_simple(self):
        argument = 'HREF="https://eludevisibility.org/" ADD_DATE="1579695523" ICON="data:image/png;base64,' \
                   'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAA' \
                   '/ElEQVQ4jZWTMY6EIBSGfzaWHOC5NbH2AJ7A2uwFtjeWxmM4rUegNvRzAWryDuAByLSzxY5kUIdx/gp++L' \
                   '/AgyfwUF3Xd3ygeZ4FAGRreJomaK3RNM3bsDEGzHx3zonsecFaC2ttMlxVVTSPAEqpZPjnOmC0EmVZBu' \
                   '/r7XkfGoYBuOz9bGssy3IIaNsW43gC4L1/CSEiSCnTAKVUshZb+OkavFJ0gmf69j8w8+ET766wart5e/dDABGFsfc' \
                   '+2ui9BxHtahABpJTJr6y1Rt/3MMYELxQxz' \
                   '/NgMjOYOQrffr8PoQL4b6YzTbSKiNB1HZxzQqxmURQftbNzTgDAH9XGWluMAOkjAAAAAElFTkSuQmCC" '
        output = attribute_finder(argument)
        expect_output = dict()
        expect_output['HREF'] = "https://eludevisibility.org/"
        expect_output['ADD_DATE'] = "1579695523"
        expect_output['ICON'] = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAA" \
                                "/ElEQVQ4jZWTMY6EIBSGfzaWHOC5NbH2AJ7A2uwFtjeWxmM4rUegNvRzAWryDuAByLSzxY5kUIdx/gp++L" \
                                "/AgyfwUF3Xd3ygeZ4FAGRreJomaK3RNM3bsDEGzHx3zonsecFaC2ttMlxVVTSPAEqpZPjnOmC0EmVZBu" \
                                "/r7XkfGoYBuOz9bGssy3IIaNsW43gC4L1/CSEiSCnTAKVUshZb+OkavFJ0gmf69j8w8+ET766wart5e" \
                                "/dDABGFsfc+2ui9BxHtahABpJTJr6y1Rt/3MMYELxQxz" \
                                "/NgMjOYOQrffr8PoQL4b6YzTbSKiNB1HZxzQqxmURQftbNzTgDAH9XGWluMAOkjAAAAAElFTkSuQmCC"
        self.maxDiff = None
        self.assertDictEqual(output, expect_output)

    def test_item_icon(self):
        argument = 'HREF="http://hiddenpalace.org/" ADD_DATE="1543525273" LAST_MODIFIED="1585439784" ' \
                   'ICON_URI="fake-favicon-uri:http://hiddenpalace.org/" ICON="data:image/png;base64,' \
                   'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAjUlEQVQ4jWNgGGjACGPYaRb' \
                   '+R5c8dL2fkZAcE0zgHwu7EJL8e2Q+VPF7bGrhBhy53AFXwMDI8B6FDxXDppaJgUJAsQEsWEX/MyhhBBxGMOIzgJHh3qFr' \
                   '/crIQnZahXcZ/jMooSsd+DCgngE2uhWCcNH/DIIofKgYNrXwQGT68' \
                   '/MdknJBKB9rUkaWG3gAAFefNAZiDEFdAAAAAElFTkSuQmCC" '
        output = attribute_finder(argument)
        expect_output = dict()
        expect_output['HREF'] = "http://hiddenpalace.org/"
        expect_output['ADD_DATE'] = '1543525273'
        expect_output['LAST_MODIFIED'] = "1585439784"
        expect_output['ICON_URI'] = "fake-favicon-uri:http://hiddenpalace.org/"
        expect_output['ICON'] = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8" \
                                "/9hAAAAjUlEQVQ4jWNgGGjACGPYaRb+R5c8dL2fkZAcE0zgHwu7EJL8e2Q" \
                                "+VPF7bGrhBhy53AFXwMDI8B6FDxXDppaJgUJAsQEsWEX/MyhhBBxGMOIzgJHh3qFr/crIQnZahXcZ" \
                                "/jMooSsd+DCgngE2uhWCcNH/DIIofKgYNrXwQGT68/MdknJBKB9rUkaWG3gAAFefNAZiDEFdAAAAAElFTkSuQmCC"
        self.maxDiff = None
        self.assertDictEqual(output, expect_output)

    def test_random(self):
        argument = 'A="1"B="2"'
        output = attribute_finder(argument)
        expected_output = dict()
        expected_output['A'] = "1"
        expected_output['B'] = "2"
        self.assertDictEqual(output, expected_output)

    def test_empty(self):
        argument = ''
        output = attribute_finder(argument)
        expected_output = dict()
        self.assertEqual(output, expected_output)


class TestDocType(unittest.TestCase):
    def test_expected(self):
        argument = '<!DOCTYPE NETSCAPE-Bookmark-file-1>'
        output = doc_type(argument)
        expected_output = 'NETSCAPE-Bookmark-file-1'
        self.assertEqual(output, expected_output)

    def test_non_expected(self):
        arg = '<!DOCTYPE html>'
        out = doc_type(arg)
        exp = 'html'
        self.assertEqual(exp, out)
        with warnings.catch_warnings(record=True) as w:
            arg = '<!DOCTYPE html>'
            doc_type(arg)
            assert (len(w) > 0)


class TestFolder(unittest.TestCase):
    def test_toolbar(self):
        arg = '<DT><H3 ADD_DATE="1548340605" LAST_MODIFIED="1587068423" PERSONAL_TOOLBAR_FOLDER="true">Barra de ' \
              'favoritos</H3>'
        out = folder(arg)
        exp = Folder()
        exp.name = 'Barra de favoritos'
        exp.add_date_unix = 1548340605
        exp.last_modified_unix = 1587068423
        exp.personal_toolbar = True
        self.assertEqual(exp, out)

    def test_common(self):
        arg = '<DT><H3 ADD_DATE="1548340605" LAST_MODIFIED="1587068423">Barra de favoritos</H3>'
        out = folder(arg)
        exp = Folder()
        exp.name = 'Barra de favoritos'
        exp.add_date_unix = 1548340605
        exp.last_modified_unix = 1587068423
        exp.personal_toolbar = False
        self.assertEqual(exp, out)


class TestEntry(unittest.TestCase):
    def test_common(self):
        arg = '<DT><A HREF="https://psvitamod.com/" ADD_DATE="1575286867">PS Vita Mod | Resources for Modding &amp; ' \
              'Hacking your PlayStation Vita Console</A>'
        out = entry(arg)
        exp = Entry()
        exp.href = 'https://psvitamod.com/'
        exp.name = 'PS Vita Mod | Resources for Modding & Hacking your PlayStation Vita Console'
        exp.add_date_unix = 1575286867
        self.assertEqual(exp, out)

    def test_icon_base64(self):
        arg = '<DT><A HREF="https://bitbuilt.net/" ADD_DATE="1571188868" ICON="data:image/png;base64,' \
              'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAADH0lEQVQ4jXWTf0zUdRjH38/n+7mDr' \
              '/cj6rtb4Abq2Q0rDpPEDVxz6mhUMttQNGDL/jyX0sLpibLAn6slOpSYFalbTucfbc5GN8VNw5NJHCYhWeStyx/5h8DuDuyu7/fz' \
              '+fRH3sag3v89z7O99n5+UexhrD8yHCnFNBFIuZyu8eLC4ojnOc+bRCTwP+KJyYTW2LFtZp4AGG6H+/Vv2y4MKaVKiCj9n4Dpwe665u' \
              '+FMEeST5K+rosnViWmEtT/4w8vBb8J3hodHV3s8/lmQTgYA7MxSFNi2ZKlZ/0' \
              '+f6dSqqi797uhaCoKu92O8EC4MLgveB3AqzMBDJBwzHUAANpPtR8KtGyO135YezM6EaVcIxfPOnMekKBoz7Wekpr6mpOzev3pt9uRm' \
              'oPrS2wOG5KxJABA0zlkSuDURydBgjAWH7OEEJwxzZqj63Fvvnd0Yf7CKiJ6zAGA2TQAQEP11gEF3LVgurojoTcCX2ymg+8cwKcDbdw' \
              'UZmZmBhEZHRuPDSml8jmkhJISxDlWl63+yu/zdwJA09GmkTOXz77YEfoMn6z7+Mn1W+Hzpimzw3d7q4Z/HuY35t/IW1xQ3M6hMTCNg' \
              'TSGqzd73zvy9ZHX/hbmM6HB0CLdo8MwDMzR9fHGTY21ANB6rDV85/c75fjXNONQQGo8BafTjs+vHS9VUpVaf1kgRrDrWahfVo+9p/f' \
              'nNuxtiAklsy6OXHpeSYWSl5c8Zoxt4TkOd/pwoC2t6RxKKAhTcCWl5na6U1OTU9nBL4NITCR4BChgNgYlFVo2tcBwGceJyKLpK6moq' \
              'Gi6P35/qdvjrtqzY0+89Vyr8efDRyh7oSy+yFvYp9k1+mXs1xWDfwxmb121BdUV1ZWzTrOysnJ30fKiWHdPd7w8UK4WrPWqnYd29mf' \
              'qfSN924sCfrVgrVdFH0X7+ExAKBTaV1dX51JKvZ/JJWmyoOt8V6cFsNNXztRIUwIA7NyeppmAjNLp9IWVH6xck9QmkZp4+gIEyJRAV' \
              'k4Wmt9utja+teGVWQ4y4pw/2LVhF0yyINMCxBkABY00K8+Td2/e3HnvEtHtfwCfJkSyZcP5lgAAAABJRU5ErkJggg==">BitBuilt ' \
              '– Giving Life to Old Consoles</A>'
        out = entry(arg)
        exp = Entry()
        exp.href = 'https://bitbuilt.net/'
        exp.add_date_unix = 1571188868
        exp.icon_base64 = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAADH0lEQVQ4jXWTf0zUdRjH38/n+7mDr/cj6rtb4Abq2Q0' \
                          'rDpPEDVxz6mhUMttQNGDL/jyX0sLpibLAn6slOpSYFalbTucfbc5GN8VNw5NJHCYhWeStyx/5h8DuDuyu7/fz+fRH3s' \
                          'ag3v89z7O99n5+UexhrD8yHCnFNBFIuZyu8eLC4ojnOc+bRCTwP+KJyYTW2LFtZp4AGG6H+/Vv2y4MKaVKiCj9n4Dpw' \
                          'e665u+FMEeST5K+rosnViWmEtT/4w8vBb8J3hodHV3s8/lmQTgYA7MxSFNi2ZKlZ/0+f6dSqqi797uhaCoKu92O8EC4' \
                          'MLgveB3AqzMBDJBwzHUAANpPtR8KtGyO135YezM6EaVcIxfPOnMekKBoz7Wekpr6mpOzev3pt9uRmoPrS2wOG5KxJAB' \
                          'A0zlkSuDURydBgjAWH7OEEJwxzZqj63Fvvnd0Yf7CKiJ6zAGA2TQAQEP11gEF3LVgurojoTcCX2ymg+8cwKcDbdwUZm' \
                          'ZmBhEZHRuPDSml8jmkhJISxDlWl63+yu/zdwJA09GmkTOXz77YEfoMn6z7+Mn1W+Hzpimzw3d7q4Z/HuY35t/IW1xQ3' \
                          'M6hMTCNgTSGqzd73zvy9ZHX/hbmM6HB0CLdo8MwDMzR9fHGTY21ANB6rDV85/c75fjXNONQQGo8BafTjs+vHS9VUpVa' \
                          'f1kgRrDrWahfVo+9p/fnNuxtiAklsy6OXHpeSYWSl5c8Zoxt4TkOd/pwoC2t6RxKKAhTcCWl5na6U1OTU9nBL4NITCR' \
                          '4BChgNgYlFVo2tcBwGceJyKLpK6moqGi6P35/qdvjrtqzY0+89Vyr8efDRyh7oSy+yFvYp9k1+mXs1xWDfwxmb121Bd' \
                          'UV1ZWzTrOysnJ30fKiWHdPd7w8UK4WrPWqnYd29mfqfSN924sCfrVgrVdFH0X7+ExAKBTaV1dX51JKvZ/JJWmyoOt8V' \
                          '6cFsNNXztRIUwIA7NyeppmAjNLp9IWVH6xck9QmkZp4+gIEyJRAVk4Wmt9utja+teGVWQ4y4pw/2LVhF0yyINMCxBkA' \
                          'BY00K8+Td2/e3HnvEtHtfwCfJkSyZcP5lgAAAABJRU5ErkJggg=='
        exp.name = 'BitBuilt – Giving Life to Old Consoles'
        self.assertEqual(exp, out)

    def test_icon_true_fav_icon(self):
        arg = '<DT><A HREF="https://archive.org/details/internetarcade?&sort=-downloads&page=2" ADD_DATE="1474332448" LAST_MODIFIED="1585439784" ICON_URI="https://archive.org/favicon.ico" ICON="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAFQElEQVRYhbWXy2tTTxTH576apOBCEbRNXHTX3iQ2uvPxD2hTitidCiI0idVuBBdZxJvUahcVCooI7l25sFRSG18USxpNti5s1NqHS/+BgMnnt3GGuUlqyw+8cLiPOXPme77ncWeEaZoIIRBCYFkWpmliWRaWZWEYBoZh4DiOGhNCYNs2gUBAiW3bmKaJYRjqLp/luxBC3eX3P+sKNUEflAYkGNM01cISsC6BQEABlfbkPB1QB4j2Adu2sW0by7K6LiSEIBwOk06nmZubI51O09fXt6uuBK57rQMTuvc9PT0dBgzDIBgMcuHCBZ49e0a1WqVer9NoNABoNBrU63VqtRpPnz5lbGyMw4cP/9UBnREVAun5uXPnGB8fp1Ao8OHDB/7v1Ww2efHiBdeuXWNkZESxJEMk70JDQk9PD/Pz8zx69Ij5+Xnm5uaYnZ1lZmaGu3fvMj09TaFQYHp62ieFQgHP8/A8j5mZGe7fv8/s7CwPHjzg4cOHPH78mOPHjysAOhNCeyAYDJLNZsnlcuRyOTzPI5/Pk8/nKRQK5PN5PM+jUCio9/Zx+ex5Hrlcjmw2y507dzh58qSPAbmmrwp6e3v/N+V7Xbdu3VLV0hECiSYQCFAul3n//j3FYpF3795RrVap1WpUKhWWlpZYWlpibW2NWq3Gx48fqVarvHnzhmKxyMrKCrVajVqtRrlcplgssri4yKdPnxgbG1NhliFXANppicfjjI+PMzAw4ItXMplkZGSkI6vj8TgXL14kHA531W9vRHovEHqzEUJw5MgRvn37BsCTJ08IBAJYlsXVq1cVnZcvX8a2bRzH4ejRo2xsbADw8uVLQqEQtm1z5coVpX/p0iVVadJhlYztH44dO6bqfGFhQfWGyclJGo0GjUaDGzduKE8jkQjr6+s0Gg1KpRKhUAghBDdv3uzQl/HXu6PQu5UE8PXrVwDevn2rWm86nVYepVIpX1eU+q9fv1aAu+nLsa5VIBmIRCI+g8FgECEEqVRKGUyn0z4A6+vrSr8bYKkvnWyTTgD1er3DoA5AZ6C/v58vX74AsLy8rLxMpVI0m01arZbS3xWA3qF0gzql+wFQKpV8DLRarf0x0A5AUloqlfYEEA6HFWPLy8s+xlqt1v4Y2C0E7ZTulgMyZ/QqyGQyHfqO4+zOgOxOehLuB0B/f39XBiYmJjoY+ysAvQz1JJRVoGd1JpNRBvSy1ZNWZ+D69es+AL4y9O1O/lDaLasnJycBaLVaTExM+ELQLQl1BqS+4zj+H5HshHoSRiIRHwDdYLPZ7AhBX1+fStpXr14pxjKZDL9///YloXTG1wnbAQwMDLC1taUAhEIhTNNkampKeTQ1NaX2eLr+ysoKvb29XfUNwyAQCHTbJQt9f4bjODx//pxfv35x+/Zt5emZM2fY2dlhe3ub06dPq++2bSv9e/fuqe9nz57l58+f7OzscOrUqd1zQC9By7IYHBwkHo9z4sQJ4vE4rusSjUaJxWIMDw+TSCRwXZdYLIbrugwODhKLxUgkEkSjUYaGhhgaGsJ1XRKJBMPDw0SjUQ4ePIjubNdd8YEDB/hXVzabxTCMjjwQ7ZScP3+e0dFRksmk2lAkk0lGR0f3FF1Pzpf2Dh06pBaWf18FQPaAhYUFKpUKq6urVCoVyuWykrW1tT1F19Xnrq6u8vnzZ2KxmMobXw5IWhYXF9ne3ubHjx9sbm6yubmpnre2tvaU3fS+f//OxsYGruv6+oA6mOit+F+Lvh/0HUz009Fu4jgOjuPsS6/bPL3+O6qg7bz2T7zudgr/D1btuaaMYsEYAAAAAElFTkSuQmCC">Internet Arcade : Free Software : Download &amp; Streaming : Internet Archive</A>'
        out = entry(arg)
        exp = Entry()
        exp.href = 'https://archive.org/details/internetarcade?&sort=-downloads&page=2'
        exp.add_date_unix = 1474332448
        exp.last_modified_unix = 1585439784
        exp.icon_url = 'https://archive.org/favicon.ico'
        exp.icon_base64 = 'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAFQElEQVRYhbWXy2tTTxTH576apOBCEbRNXHTX3iQ2uvPxD2hTitidCiI0idVuBBdZxJvUahcVCooI7l25sFRSG18USxpNti5s1NqHS/+BgMnnt3GGuUlqyw+8cLiPOXPme77ncWeEaZoIIRBCYFkWpmliWRaWZWEYBoZh4DiOGhNCYNs2gUBAiW3bmKaJYRjqLp/luxBC3eX3P+sKNUEflAYkGNM01cISsC6BQEABlfbkPB1QB4j2Adu2sW0by7K6LiSEIBwOk06nmZubI51O09fXt6uuBK57rQMTuvc9PT0dBgzDIBgMcuHCBZ49e0a1WqVer9NoNABoNBrU63VqtRpPnz5lbGyMw4cP/9UBnREVAun5uXPnGB8fp1Ao8OHDB/7v1Ww2efHiBdeuXWNkZESxJEMk70JDQk9PD/Pz8zx69Ij5+Xnm5uaYnZ1lZmaGu3fvMj09TaFQYHp62ieFQgHP8/A8j5mZGe7fv8/s7CwPHjzg4cOHPH78mOPHjysAOhNCeyAYDJLNZsnlcuRyOTzPI5/Pk8/nKRQK5PN5PM+jUCio9/Zx+ex5Hrlcjmw2y507dzh58qSPAbmmrwp6e3v/N+V7Xbdu3VLV0hECiSYQCFAul3n//j3FYpF3795RrVap1WpUKhWWlpZYWlpibW2NWq3Gx48fqVarvHnzhmKxyMrKCrVajVqtRrlcplgssri4yKdPnxgbG1NhliFXANppicfjjI+PMzAw4ItXMplkZGSkI6vj8TgXL14kHA531W9vRHovEHqzEUJw5MgRvn37BsCTJ08IBAJYlsXVq1cVnZcvX8a2bRzH4ejRo2xsbADw8uVLQqEQtm1z5coVpX/p0iVVadJhlYztH44dO6bqfGFhQfWGyclJGo0GjUaDGzduKE8jkQjr6+s0Gg1KpRKhUAghBDdv3uzQl/HXu6PQu5UE8PXrVwDevn2rWm86nVYepVIpX1eU+q9fv1aAu+nLsa5VIBmIRCI+g8FgECEEqVRKGUyn0z4A6+vrSr8bYKkvnWyTTgD1er3DoA5AZ6C/v58vX74AsLy8rLxMpVI0m01arZbS3xWA3qF0gzql+wFQKpV8DLRarf0x0A5AUloqlfYEEA6HFWPLy8s+xlqt1v4Y2C0E7ZTulgMyZ/QqyGQyHfqO4+zOgOxOehLuB0B/f39XBiYmJjoY+ysAvQz1JJRVoGd1JpNRBvSy1ZNWZ+D69es+AL4y9O1O/lDaLasnJycBaLVaTExM+ELQLQl1BqS+4zj+H5HshHoSRiIRHwDdYLPZ7AhBX1+fStpXr14pxjKZDL9///YloXTG1wnbAQwMDLC1taUAhEIhTNNkampKeTQ1NaX2eLr+ysoKvb29XfUNwyAQCHTbJQt9f4bjODx//pxfv35x+/Zt5emZM2fY2dlhe3ub06dPq++2bSv9e/fuqe9nz57l58+f7OzscOrUqd1zQC9By7IYHBwkHo9z4sQJ4vE4rusSjUaJxWIMDw+TSCRwXZdYLIbrugwODhKLxUgkEkSjUYaGhhgaGsJ1XRKJBMPDw0SjUQ4ePIjubNdd8YEDB/hXVzabxTCMjjwQ7ZScP3+e0dFRksmk2lAkk0lGR0f3FF1Pzpf2Dh06pBaWf18FQPaAhYUFKpUKq6urVCoVyuWykrW1tT1F19Xnrq6u8vnzZ2KxmMobXw5IWhYXF9ne3ubHjx9sbm6yubmpnre2tvaU3fS+f//OxsYGruv6+oA6mOit+F+Lvh/0HUz009Fu4jgOjuPsS6/bPL3+O6qg7bz2T7zudgr/D1btuaaMYsEYAAAAAElFTkSuQmCC'
        exp.name = 'Internet Arcade : Free Software : Download & Streaming : Internet Archive'
        self.assertEqual(exp, out)

    def test_icon_fake_fav_icon(self):
        arg = '<DT><A HREF="http://hiddenpalace.org/" ADD_DATE="1543525273" LAST_MODIFIED="1585439784" ICON_URI="fake' \
              '-favicon-uri:http://hiddenpalace.org/" ICON="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAY' \
              'AAAAf8/9hAAAAjUlEQVQ4jWNgGGjACGPYaRb+R5c8dL2fkZAcE0zgHwu7EJL8e2Q+VPF7bGrhBhy53AFXwMDI8B6FDxXDppaJgUJAs' \
              'QEsWEX/MyhhBBxGMOIzgJHh3qFr/crIQnZahXcZ/jMooSsd+DCgngE2uhWCcNH/DIIofKgYNrXwQGT68/MdknJBKB9rUkaWG3gAAFe' \
              'fNAZiDEFdAAAAAElFTkSuQmCC">Hidden Palace</A>'
        out = entry(arg)
        exp = Entry()
        exp.href = 'http://hiddenpalace.org/'
        exp.add_date_unix = 1543525273
        exp.last_modified_unix = 1585439784
        exp.icon_url_fake = True
        exp.icon_base64 = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAjUlEQVQ4jWNgGGjACGPYaRb+R5c8dL2fkZAcE0zgHw' \
                          'u7EJL8e2Q+VPF7bGrhBhy53AFXwMDI8B6FDxXDppaJgUJAsQEsWEX/MyhhBBxGMOIzgJHh3qFr/crIQnZahXcZ/jMo' \
                          'oSsd+DCgngE2uhWCcNH/DIIofKgYNrXwQGT68/MdknJBKB9rUkaWG3gAAFefNAZiDEFdAAAAAElFTkSuQmCC'
        exp.name = 'Hidden Palace'
        self.assertEqual(exp, out)

    def test_uncommon_attributes(self):
        arg = '<DT><A HREF="https://developer.apple.com/library/mac/releasenotes/InterapplicationCommunication/' \
              'RN-JavaScriptForAutomation/index.html#//apple_ref/doc/-%20uid/TP40014508" ADD_DATE="1414706885" ' \
              'PRIVATE="0" TAGS="javascript,mac,osx,yosemite">JavaScript for Automation Release Notes</A>'
        comment = 'This article describes JavaScript for Automation, a new feature in OS X Yosemite.'
        out = entry(arg, comment)
        exp = Entry()
        exp.href = 'https://developer.apple.com/library/mac/releasenotes/InterapplicationCommunication/RN-JavaScript' \
                   'ForAutomation/index.html#//apple_ref/doc/-%20uid/TP40014508'
        exp.add_date_unix = 1414706885
        exp.private = 0
        exp.tags = ['javascript', 'mac', 'osx', 'yosemite']
        exp.name = 'JavaScript for Automation Release Notes'
        exp.comment = 'This article describes JavaScript for Automation, a new feature in OS X Yosemite.'
        self.assertEqual(exp, out)

    def test_last_visit(self):
        arg = '<DT><A HREF="http://www.tekzoned.com" ADD_DATE="1357547237" LAST_VISIT="1357547238" ' \
              'LAST_MODIFIED="1357547239">TekZoned</A>'
        out = entry(arg)
        exp = Entry()
        exp.href = 'http://www.tekzoned.com'
        exp.add_date_unix = 1357547237
        exp.last_visit_unix = 1357547238
        exp.last_modified_unix = 1357547239
        exp.name = 'TekZoned'
        self.assertEqual(exp, out)

    def test_feed(self):
        arg = '<DT><A FEED="true" FEEDURL="https://www.nasa.gov/rss/dyn/breaking_news.rss">NASA Breaking News</A>'
        out = entry(arg)
        exp = Feed()
        exp.name = 'NASA Breaking News'
        exp.feed = True
        exp.feed_url = 'https://www.nasa.gov/rss/dyn/breaking_news.rss'
        self.assertEqual(exp, out)

    def test_web_slice(self):
        arg = '<DT><A WEBSLICE="true" ISLIVEPREVIEW="true" PREVIEWSIZE="10 x 10">Weather Now</A>'
        out = entry(arg)
        exp = WebSlice()
        exp.name = 'Weather Now'
        exp.web_slice = True
        exp.is_live_preview = True
        exp.preview_size = '10 x 10'
        self.assertEqual(exp, out)


class TestItemHandler(unittest.TestCase):
    def test_common(self):
        arg = '<DT><A HREF="https://psvitamod.com/" ADD_DATE="1575286867">PS Vita Mod | Resources for Modding &amp; ' \
              'Hacking your PlayStation Vita Console</A>'
        out = item_handler(0, arg)
        exp = Entry()
        exp.href = 'https://psvitamod.com/'
        exp.name = 'PS Vita Mod | Resources for Modding & Hacking your PlayStation Vita Console'
        exp.add_date_unix = 1575286867
        self.assertEqual(exp, out)

    def test_uncommon_attributes(self):
        arg = '<DT><A HREF="https://developer.apple.com/library/mac/releasenotes/InterapplicationCommunication/' \
              'RN-JavaScriptForAutomation/index.html#//apple_ref/doc/-%20uid/TP40014508" ADD_DATE="1414706885" ' \
              'PRIVATE="0" TAGS="javascript,mac,osx,yosemite">JavaScript for Automation Release Notes</A>'
        comment = 'This article describes JavaScript for Automation, a new feature in OS X Yosemite.'
        out = item_handler(0, arg, comment)
        exp = Entry()
        exp.href = 'https://developer.apple.com/library/mac/releasenotes/InterapplicationCommunication/RN-JavaScript' \
                   'ForAutomation/index.html#//apple_ref/doc/-%20uid/TP40014508'
        exp.add_date_unix = 1414706885
        exp.private = 0
        exp.tags = ['javascript', 'mac', 'osx', 'yosemite']
        exp.name = 'JavaScript for Automation Release Notes'
        exp.comment = 'This article describes JavaScript for Automation, a new feature in OS X Yosemite.'
        self.assertEqual(exp, out)

    def test_invalid_a_tag_start(self):
        arg = '<DT> HREF="http://www.tekzoned.com" ADD_DATE="1357547237" LAST_VISIT="1357547238" ' \
              'LAST_MODIFIED="1357547239">TekZoned</A>'
        out = item_handler(0, arg)
        exp = entry(arg)
        self.assertEqual(exp, out)
        with warnings.catch_warnings(record=True) as w:
            item_handler(0, arg)
            assert (len(w) > 0)

    def test_invalid_a_tag_end(self):
        arg = '<DT><A HREF="http://www.tekzoned.com" ADD_DATE="1357547237" LAST_VISIT="1357547238" ' \
              'LAST_MODIFIED="1357547239">TekZoned</A'
        out = item_handler(0, arg)
        exp = entry(arg)
        self.assertEqual(exp, out)
        with warnings.catch_warnings(record=True) as w:
            item_handler(0, arg)
            assert (len(w) > 0)

    def test_invalid_a_tag(self):
        arg = '<DT>A HREF="http://www.tekzoned.com" ADD_DATE="1357547237" LAST_VISIT="1357547238" ' \
              'LAST_MODIFIED="1357547239">TekZonedA>'
        out = item_handler(0, arg)
        exp = entry(arg)
        self.assertEqual(exp, out)
        with warnings.catch_warnings(record=True) as w:
            item_handler(0, arg)
            assert (len(w) > 0)


class TestFolderHandler(unittest.TestCase):
    def test_single_entry(self):
        arg1 = '<DT><H3 ADD_DATE="1548340605" LAST_MODIFIED="1587068423" PERSONAL_TOOLBAR_FOLDER="true">Barra de ' \
               'favoritos</H3>'
        arg2 = list()
        arg2.append('<DL><p>')
        arg2.append('<DT><A HREF="https://psvitamod.com/" ADD_DATE="1575286867">PS Vita Mod | Resources for Modding'
                    ' &amp Hacking your PlayStation Vita Console</A>')
        arg2.append('</DL><p>')
        out = folder_handler(0, arg1, arg2)
        exp = Folder()
        exp.name = 'Barra de favoritos'
        exp.add_date_unix = 1548340605
        exp.last_modified_unix = 1587068423
        exp.personal_toolbar = True
        exp.items.append(item_handler(2, arg2[1]))
        exp.entries.append(item_handler(2, arg2[1]))
        self.assertEqual(exp, out)

    def test_empty_folder(self):
        arg1 = '<DT><H3 ADD_DATE="1548340605" LAST_MODIFIED="1587068423">Barra de favoritos</H3>'
        arg2 = list()
        arg2.append('<DL><p>')
        arg2.append('</DL><p>')
        out = folder_handler(0, arg1, arg2)
        exp = Folder()
        exp.name = 'Barra de favoritos'
        exp.add_date_unix = 1548340605
        exp.last_modified_unix = 1587068423
        exp.personal_toolbar = False
        self.assertEqual(exp, out)

    def test_with_subfolder_empty(self):
        arg1 = '<DT><H3 ADD_DATE="1548340605" LAST_MODIFIED="1587068423">Barra de favoritos</H3>'
        arg2 = list()
        arg2.append('<DL><p>')
        arg2.append('<DT><H3 ADD_DATE="1548340605" LAST_MODIFIED="1587068423">Barra de favoritos</H3>')
        arg2.append('<DL><p>')
        arg2.append('</DL><p>')
        arg2.append('</DL><p>')
        out = folder_handler(0, arg1, arg2)
        exp = Folder()
        exp.name = 'Barra de favoritos'
        exp.add_date_unix = 1548340605
        exp.last_modified_unix = 1587068423
        exp.personal_toolbar = False
        exp.items.append(folder_handler(2, arg2[1], arg2[3:5]))
        exp.children.append(folder_handler(2, arg2[1], arg2[3:5]))
        self.assertEqual(exp, out)

    def test_with_subfolder(self):
        arg1 = '<DT><H3 ADD_DATE="1548340605" LAST_MODIFIED="1587068423">Barra de favoritos</H3>'
        arg2 = list()
        arg2.append('<DL><p>')
        arg2.append('<DT><H3 ADD_DATE="1548340605" LAST_MODIFIED="1587068423">Barra de favoritos</H3>')
        arg2.append('<DL><p>')
        arg2.append('<DT><A HREF="https://psvitamod.com/" ADD_DATE="1575286867">PS Vita Mod | Resources for Modding'
                    ' &amp Hacking your PlayStation Vita Console</A>')
        arg2.append('</DL><p>')
        arg2.append('</DL><p>')
        out = folder_handler(0, arg1, arg2)
        exp = Folder()
        exp.name = 'Barra de favoritos'
        exp.add_date_unix = 1548340605
        exp.last_modified_unix = 1587068423
        exp.personal_toolbar = False
        subfolder = folder_handler(2, arg2[1], arg2[3:6])
        exp.items.append(subfolder)
        exp.children.append(subfolder)
        self.assertEqual(exp, out)


class TestParse(unittest.TestCase):
    def test_common(self):
        self.maxDiff = None
        file = open('test.html')
        self.file = File(file)
        self.exp = File(file, parse_automatically=False)
        self.exp = File(open('test.html'), parse_automatically=False)
        self.exp.doc_type = 'NETSCAPE-Bookmark-file-1'
        self.exp.http_equiv_meta = 'Content-Type'
        self.exp.content_meta = 'text/html; charset=UTF-8'
        self.exp.title = 'Bookmarks'
        self.exp.bookmarks.name = 'Bookmarks'
        arg1 = '<DT><H3 ADD_DATE="1588614754" LAST_MODIFIED="1588614939" PERSONAL_TOOLBAR_FOLDER="true">' \
               'Barra de favoritos</H3>'
        arg2 = ''' <DL><p>
        <DT><A HREF="https://www.google.com/webhp?hl=pt-BR&ictx=2&sa=X&ved=0ahUKEwj0s7Ge45rpAhWuDbkGHflbAdEQPQgH&safe=active" ADD_DATE="1588614918" ICON="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACIklEQVQ4jYWSS0iUURTHf/fe8RvHooE2VlT2FNqUGWmNEYUR9lhEEVJhUIsoXOQuap1Rq6KHNQt3LaPAIOxhlNTChUwLMU3NR1CklUzg6xvPd1ro2KhTHjjcA/e8/uf/hzmmqsUiEheRLhHxp/2TiDxQ1aK5+ZmFeSJSrwuYiMRVNZKuMxnFz51zu9T3GX/6iPGmRqS/F5WAUMEawuUVRI5UYjwPEWl2zlUYY8YMgIjUW2vPBkPfSV6uYbKvJ+uW3rZSojfuABAEQdw5d96oajHQqr7P8IUqpL8X43lEjp3EK4mBtfgt75l4+4po7U3cytWZPbcyjUlTidv642ipDu7foX7bh2zgs92jDhHpUlWdbNmuEw15OvqweqE7ZjboCAEFADrSjs1LkRM7NAt3+bWRebfYudFx9XguwFqbwePs9z/mT/6NLdAHMBpex28W0/C1Y1Zy05VFM75nUwiAZVGT/v5sgdcA3UurOPUrxvXOFhJD7fOmdn4LeNc5NbpkfWimv5mWZ8KXFKdfXqInOYBnc6gsPEjZ8mKssbQOtvEkMczYl0oK8z3un4lgppbYkhZS3Fp7bnD0Jxeba+lODmTFviFcxq29NeRHDUEQ1DnnqtNSjohIo3Nutx+keNz9gmf9zfQkB0ChYMkK9q2KcaLwMJFQGFV9Y4w5YIwZzyBBI2lRLcD9PVXN/SdFqlokInUi0iEiE9P+UUTuqurmufl/AKTzsFGmvUNUAAAAAElFTkSuQmCC">Google</A>
    </DL><p>'''
        arg2 = arg2.splitlines()
        subfolder = folder_handler(8, arg1, arg2)
        subfolder.num = 0
        subfolder.parent = self.exp
        self.exp.bookmarks.items.append(subfolder)
        self.exp.bookmarks.children.append(subfolder)
        arg_ = '<DT><A HREF="https://www.reddit.com/" ADD_DATE="1588614939" ICON="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACdUlEQVQ4jWXTTYjVdRTG8c/5/e+945hNMhLEgFRUA1lgNYHojJjpDXduQkSqjRiKJNSu2rRJV0VQi14IKohCW8UEIRJZ05uUGESrBBOsJocayRznvvxPizup0dmcxeF5zoHzfAOSCBKybRP2SpO4SUjMSjOKV+Ooz67VhKXKdUZc75CwWzGk/neAQBXUuSi9oevp+NRFiCRMGDHqiIa2rkSNgqu3Xc5aUQwLfR9bsCO+8FcjyLzBIQ1tPR2hIVWD7ZEeforMsPLGyh331g7u6rr4xzbDnseBkltNqezW0xfRIIqqpDrSytHQGg7Tb6XZM6mzWNDQUwuP5xbrI9veU+xU61tUBHpCB+vWs3qcd9+mhYbUxDK1UKm905AmpdQTbh2n2wnj97F5F7fcRd1j7WaOv89Pp0JzKP36c2hKTMmHymJulHlgQ51/X8i8MJdZ9/N/1e9lzp3LnD+fuW+izo0y26VTXPljDvrIKl5+gn330+/R67B3gjefYdUYzSFKdUVWZD1reaRvv0rffJT6fe6epP0YVYNGi8nt3LxmYHjyWDp1Ii2Xsj5bpM+VCEX6+kNZVTy4i3s2Mf878+fZsJ32o7JqcGJ6EK8SIcxUz91mVp2PaEZx+gcREcYn0ty5cPp7fjvD8HVpZFQceSEcfjG1hDo7evYH5BavGLJfR8dlDXeuLR7YkcZuH8T4l9Ph+Af8eLLW0tfS1PVSHPPkIMqTVhh2WNM2/UgLWesITQNWulJLGo6iytA1rdjpqEtXYVpjhTEHhT2qsoygXiKqlAFVvXoBr/nTs/GdS5Y4+y/OW01hD6awesn/rDCj7/X4xJfXav4BhnocQyGrEocAAAAASUVORK5CYII=">reddit: the front page of the internet</A>'
        item = item_handler(12, arg_)
        item.num = 1
        item.parent = self.exp
        self.exp.bookmarks.items.append(item)
        self.exp.bookmarks.entries.append(item)
        self.assertDictEqual(self.exp.__dict__, self.file.__dict__)
        self.assertDictEqual(self.exp.bookmarks.__dict__, self.file.bookmarks.__dict__)
        file.close()


if __name__ == '__main__':
    unittest.main()
