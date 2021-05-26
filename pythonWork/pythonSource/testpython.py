from IM_OBJECTS import Languagetext


neu = {key: {'en': val,'fr':Languagetext.translNameFR[key]} for key,val in Languagetext.translNameEN.items()}
print (neu)


