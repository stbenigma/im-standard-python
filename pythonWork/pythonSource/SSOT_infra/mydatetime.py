from datetime import datetime
import logging

DEFAULTDATETIMEFORMAT:str='%Y-%m-%d %H:%M:%S.%f'

def todatetime(val):
    if type(val) is str:
        if len(val) < 20:
            corrected = val + '.000000'
            logging.warning(f"Adding milliseconds to timestamp {val} -> {corrected}")
            val = corrected
        if val[2] == '-':
            corrected = ('20' + val)[:26]
            logging.warning(f"Fixing time format {val} -> {corrected}")
            val = corrected
        retval = datetime.strptime(val,DEFAULTDATETIMEFORMAT)
    else:
        retval = val
    return retval