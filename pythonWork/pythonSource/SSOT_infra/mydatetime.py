from datetime import datetime
import logging

DEFAULTDATETIMEFORMAT: str = '%Y-%m-%d %H:%M:%S.%f'

DEFAULTDATETIMEFORMAT_WITH_TIMEZONE: str = '%Y-%m-%d %H:%M:%S.%f %Z'


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
        format = DEFAULTDATETIMEFORMAT
        if val.endswith('UTC'):
            format = DEFAULTDATETIMEFORMAT_WITH_TIMEZONE
        try:
            retval = datetime.strptime(val, format)
        except ValueError as e:
            raise ValueError(f"Cannot covert {val} with pattern {format}") from e

    else:
        retval = val
    return retval
