import re

str_separator = ' _:_ '


def remove_non_ansii(text):
    return re.sub(r'[^\x00-\x7f]', r' ', text)


class Container(object):
    pass
