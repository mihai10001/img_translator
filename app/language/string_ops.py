
def clean(string):
    # Removes all whitespace characters including
    # space, tab, newline, return, formfeed (any combinations / multiples)
    return " ".join(string.split())


def word_split(string):
    # Split the string into words
    return string.split()


def word_join(iterable, separator=' '):
    # Joins the elements in the iterable by the separator
    return separator.join(iterable)
