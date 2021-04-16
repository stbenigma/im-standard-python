import re
iconnoregexp = re.compile(r"^[0-9]{2,5}$")
print (re.match(iconnoregexp, None))
