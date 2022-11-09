class LaterEntries:
    """
    List of entries who are to be handled, if all are read (cross-references in wrong order)
        {entryguid: {property:value,}
         e.f. for entities {"entity":, "color":, "superentitityguid":, "subentities":[ids], "categoryguid":}}
    """

    def __init__(self):
        self._entries = dict()

    def getkeys(self):
        return self._entries.keys()

    def setentry(self,guid, **kwargs):
        if guid not in self._entries:
            self._entries[guid] = dict()
        for key, val in kwargs.items():
            self._entries[guid][key] = val

    def getentry(self,guid, value=None):
        if guid in self._entries.keys():
            if value is None:
                #whole entry
                return self._entries.get(guid)
            else:
                #only the specified value
                return self._entries[guid].get(value)
        else:
            return None