class base():
    classvar:str = "BASE"
    @classmethod
    def clsvar(cls):
        return cls.classvar

class sup1(base):
    classvar:str = "SUP1"

class sup2(base):
    pass

print (base.clsvar())
print (sup1.clsvar())
print (sup2.clsvar())
