import re
import html

def escape(s:str):
    return html.escape(s)
def unescape(s:str):
    return html.unescape(s)

def striphtml(text,keeplinebreaks=True):
    """remove htmltags from text
        replace <br> and </p> by \n
        except at the end
        """
    p = re.compile(r'<.*?>')
    retval = text
    if keeplinebreaks:
        retval = re.sub("<br ?/?>$", "", retval)
        retval = re.sub("</p>$", "", retval)
        retval = re.sub("</p>", "\n", retval)
        retval = re.sub("<br ?/>", "\n", retval)
        retval = re.sub("<br ?/?>", "\n", retval)
    retval = p.sub('',unescape(retval))

    return retval