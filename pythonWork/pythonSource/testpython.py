
import os
from  SSOT_infra import transl,settransldomain,resettransldomain
print (transl("Entität"))
settransldomain("fr")
print (transl("Entität"))
settransldomain("es")
print (transl("Entität"))

#el = gettext.bindtextdomain('prompts', './SSOT_infra/locales')
#el = gettext.translation('prompts', localedir='./SSOT_infra/locales', languages=['fr','en'])
#el.install()
#_ = el.gettext # Greek
#print (_("Entität"),el.gettext("Zeitpunkt"))

#locale_folder = config.get('locale', './locale')
# el = gettext.bindtextdomain('prompts', locale_folder)


