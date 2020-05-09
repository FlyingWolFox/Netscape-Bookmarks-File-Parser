class ParserException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return


class TagNotPresentException(ParserException):
    pass


class EmptyFileException(ParserException):
    pass


class RootBookmarksFolderNotFoundException(ParserException):
    pass


class CreatorException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return


class ValueEmptyException(CreatorException):
    pass
