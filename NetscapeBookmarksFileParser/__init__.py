from dataclasses import dataclass
from NetscapeBookmarksFileParser.parser import parse

non_parsed = dict()  # lines not parsed


@dataclass
class BookmarkItem:
    """
    Represents an item in the bookmarks. An item can be a folder
    or an entry (shortcut, feed or web slice).
    """
    num: int = 0  # the position of the item in the folder it's in
    add_date_unix: int = 0  # the creation date of the item in unix time
    last_modified_unix: int = 0  # the creation date of the item in unix time
    parent = None  # the parent folder of the item. Just the root folder have this equal None
    name: str = ''  # name of the item


@dataclass
class BookmarkFolder(BookmarkItem):
    """
    Represents a folder in the bookmarks
    """
    personal_toolbar: bool = False  # true if the folder is the bookmarks toolbar
    items = None  # list that contains all items inside this folder
    children = None  # list that contains all subfolders inside this folder
    entries = None  # list that contains all entries (shortcuts) inside this folder

    def __post_init__(self):
        self.items = []
        self.children = []
        self.entries = []


@dataclass
class BookmarkEntry(BookmarkItem):
    """
    Represents an entry (shortcut) in the bookmarks
    """
    href: str = ""  # link to the web page (or anything alike) of the entry
    last_visit_unix: int = 0  # date when the web paged was last visited, in unix time
    private: int = 0  # equals to the PRIVATE attribute
    tags = None  # tags of this entry, if present
    icon_url_fake: bool = False  # true if the ICON_URI attribute start with fake-favicon-uri.
    icon_url: str = ""  # the favicon url if icon_url_fake is false and the attribute ICON_URI is present
    icon_base64: str = ""  # the favicon encoded in base64. Commonly is a png image. The string here can be really big
    feed: bool = False  # true if the attribute FEED  is present. Legacy support for feeds
    web_slice: bool = False  # true if the attribute WEBSLICE is present
    comment: str = ""  # comment of the entry if present

    def __post_init__(self):
        self.tags = list()


@dataclass
class BookmarkFeed(BookmarkEntry):
    """
    Represents a Feed in the bookmarks
    """
    feed: bool = True
    feed_url: str = ""  # feed url


@dataclass
class BookmarkWebSlice(BookmarkEntry):
    """
    Represents an Web Slice in the bookmarks
    """
    web_slice: bool = True
    is_live_preview: bool = False  # value of the attribute ISLIVEPREVIEW
    preview_size: str = ""  # value of the attribute PREVIEWSIZE.


class NetscapeBookmarksFile(object):
    """
    Represents the Netscape Bookmark File
    """

    def __init__(self, bookmarks="", parse_automatically=True):
        self.html: str = ""
        if hasattr(bookmarks, 'read'):
            self.html = bookmarks.read()
        elif isinstance(bookmarks, str):
            self.html = bookmarks

        self.doc_type = ""
        self.http_equiv_meta = ""
        self.content_meta = ""

        self.title = ""

        self.bookmarks = BookmarkFolder()
        global non_parsed
        self.non_parsed = non_parsed

        if parse_automatically:
            self.parse_file()

    def parse_file(self):
        """
        starts the parsing of the file
        :return: None
        """
        parse(self)

    def __str__(self):
        return "NetscapeBookmarkFile(bookmarks: {0})".format(str(self.bookmarks))
