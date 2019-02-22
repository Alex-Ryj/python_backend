import re

str_separator = ' _:_ '


def removeNonAnsii(text):
    return re.sub(r'[^\x00-\x7f]',r' ',text)  