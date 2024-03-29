from dataclasses import dataclass

non_parsed = dict()  # lines not parsed


@dataclass
class BookmarkItem:
    """
    Represents an item in the bookmarks. An item can be a folder
    or an shortcut (can be feed or web slice too, but it's rare nowadays).
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
    shortcuts = None  # list that contains all shortcuts inside this folder

    def __post_init__(self):
        self.items = []
        self.children = []
        self.shortcuts = []

    def sync_items(self, recursive=True):
        """
        sync the folder item list with children and shortcut lists.
        The item list is cleaned and populated with the items from
        children and shortcut lists
        :param recursive: if subfolders should have their items synced too
        :return: nothing
        """
        self.items = []
        self.items.extend(self.children)
        self.items.extend(self.shortcuts)
        if recursive:
            for child in self.children:
                child.sync_items()

    def split_items(self, recursive=True):
        """
        splits the items list into children and shortcuts
        :param self: folder to have items splitted
        :param recursive: if subfolders should have their items splitted too
        :return: nothing
        """
        for item in self.items:
            if isinstance(item, BookmarkShortcut):
                self.shortcuts.append(item)

            elif isinstance(item, BookmarkFolder):
                self.children.append(item)
                if recursive:
                    item.split_items()

    def sort_items(self, recursive=True):
        """
        sort the items list by the num of each item.
         split_items() is ran before sorting happens
        :param recursive: if subfolders will have their items sorted too
        :return: nothing
        """

        def sort_by_number(e):
            return e.num

        self.items.sort(key=sort_by_number)
        self.children.sort(key=sort_by_number)
        self.shortcuts.sort(key=sort_by_number)
        self.split_items(recursive)
        if recursive:
            for child in self.children:
                child.sort_items()

    def sort_children_and_shortcuts(self, recursive=True):
        """
        sort the children and shortcuts lists by the num of each item.
         sync_items() is ran before sorting happens
        :param recursive: if subfolders will have their children and shortcuts sorted too
        :return: nothing
        """

        def sort_by_number(e):
            return e.num

        self.children.sort(key=sort_by_number)
        self.shortcuts.sort(key=sort_by_number)
        self.sync_items(recursive)
        if recursive:
            for child in self.children:
                child.sort_children_and_shortcuts()


@dataclass
class BookmarkShortcut(BookmarkItem):
    """
    Represents a shortcut in the bookmarks
    """
    href: str = ""  # link to the web page (or anything alike) of the shortcut
    last_visit_unix: int = 0  # date when the web paged was last visited, in unix time
    private: int = 0  # equals to the PRIVATE attribute
    tags = None  # tags of this shortcut, if present
    icon_url_fake: bool = False  # true if the ICON_URI attribute start with fake-favicon-uri.
    icon_url: str = ""  # the favicon url if icon_url_fake is false and the attribute ICON_URI is present
    icon_base64: str = ""  # the favicon encoded in base64. Commonly is a png image. The string here can be really big
    feed: bool = False  # true if the attribute FEED  is present. Legacy support for feeds
    web_slice: bool = False  # true if the attribute WEBSLICE is present. Legacy support for web slices
    comment: str = ""  # comment of the shortcut if present
    shortcut_url: str = ""  # the shortcut keyword associated with the shortcut, if set. Used by firefox (see #8)

    def __post_init__(self):
        self.tags = []


@dataclass
class BookmarkFeed(BookmarkShortcut):
    """
    Represents a Feed in the bookmarks
    """
    feed: bool = True
    feed_url: str = ""  # feed url


@dataclass
class BookmarkWebSlice(BookmarkShortcut):
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

    def __init__(self, bookmarks=""):
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

    def __str__(self):
        return "NetscapeBookmarkFile(bookmarks: {0})".format(str(self.bookmarks))
