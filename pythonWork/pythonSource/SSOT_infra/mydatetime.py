from datetime import datetime
DEFAULTDATETIMEFORMAT:str='%Y-%m-%d %H:%M:%S.%f'

def todatetime(val):
    if type(val) is str:
        retval = datetime.strptime(val,DEFAULTDATETIMEFORMAT)
    else:
        retval = val
    return retval