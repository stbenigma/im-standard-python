import re

def multiline2spaceseparated(text):
    retval = re.sub("\n"," ",text)
    #remove duplicate blanks
    retval = re.sub(" +"," ",retval)
    return retval

def text2crtext(text:str,maxlines:int,maxwidth:int)->str:
    if text is None: return None
    return "\n".join(text2multiline(text=text,maxlines=maxlines,maxwidth=maxwidth))

def shortenstring(text, maxwidth,withdots=False):
    """
    shortens the string to maxwidth characters
    return the rest in reststring
    """
    if len(text) == 0:
        return '', ''

    contdots = ".." if withdots else ""
    shorttext, reststring = text, ""
    idx = 0
    while len(shorttext) > 4 and len(shorttext) > maxwidth:
        removechars = 1 + (len(contdots) if shorttext.endswith(contdots) else 0)
        shorttext = shorttext[:-removechars] + contdots
        idx += 1
        reststring = text[-idx:]
    #while
    return shorttext, reststring

def text2multiline(text:str,
                   maxlines:int,maxwidth:int,
                   withdots=False)->list:
    assert not withdots,"not yet tested"
    if text is None: return None
    multilinetext=[]
    remaininglines = maxlines - 1
    shorttext = text
    for idx in range(1, maxlines + 1):
        shorttext, reststring = shortenstring(shorttext,maxwidth=maxwidth,
                                                withdots=withdots and (idx == maxlines))
        if shorttext == "":
            if len(multilinetext)==0: multilinetext.append("")
            break
        """while text is  at least 3 letters
                and last character is digit or alpha
                and reststring contains characters
                and reststring + one more character fits in 
                        width of resting line
            move one character to reststring
        """
        savest, savers = shorttext, reststring
        while (len(shorttext) > 3) \
                and re.match(r"\S|\d",shorttext[-1]) \
                and (len(reststring) > 0) \
                and re.match(r"\S|\d",reststring[0]) :
            reststring = shorttext[-1] + reststring
            shorttext = shorttext[:-1]
        # while
        """ if last character is still digit or alpha, there was no break-character
            return to original break
        """
        if (shorttext[-1].isdigit() or shorttext[-1].isalpha()):
            shorttext, reststring = savest, savers

        shorttext = shorttext.strip()  # get rid of trailing whitespace
        multilinetext.append(shorttext)
        remaininglines -= 1
        shorttext = reststring.strip()
    #for
    return multilinetext

def removenonchars(s:str)->str:
    """removes all non letters and nondigts and none _ from string"""
    if s is None: return None
    nonletterdigit=re.compile(r"[^\w]")
    return nonletterdigit.sub('',s)
