from datetime import datetime

"""
Library functions for special string handling
"""
def escapestr(instr):
    """
    escape all characters in a string not suitable for dataspot
    :param instr:
    :return:
    """
    if instr is None: return instr
    retval = instr.replace('"', '\\"'). \
        replace("\n", " "). \
        replace("\u00a0", " "). \
        replace("\u0013", "-"). \
        replace("\u0014", "-")
    return retval

def custom_split(input_string, delimiter, quote='"'):
    """
    my version of split. can handle delimiters enclosed in "" (quote)
    remove all characters not suitable for dataspot

    :param input_string:  string to be split
    :param delimiter:  delimiter to split
    :param quote:  Quote (") where delimiters within are not splitted
    :return:
    """
    result = []
    current_segment = []
    in_quotes = False
    if input_string is None: return result

    for char in input_string:
        if char == quote:
            in_quotes = not in_quotes
        elif char == delimiter and not in_quotes:
            result.append(escapestr(''.join(current_segment)))
            current_segment = []
        else:
            current_segment.append(char)

    result.append(escapestr(''.join(current_segment)))
    return result

def fullescapestr(instr):
    """ escape string and then enclose string in "" if it contains / or . """
    retval = escapestr(instr)
    if retval is not None and (("/" in instr) or ('.' in instr)):
        retval = f'"{retval}"'
    return retval
