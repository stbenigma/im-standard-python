class Base():
      def __init__(self):
            print ('init base',self._tablename)
      @classmethod
      def select(cls):
            return cls._tablename

class E1(Base):
      _tablename='E1'
      def __init__(self):
            super().__init__()
            self.abc=1

      def getval(self,name):
            return self.__getattribute__(name)
      @classmethod
      def select(cls):
            print ('select e1',cls._tablename,super().select())
            return cls._tablename

class E2(Base):
      _tablename='E2'


e2 = E2()
e1 = E1()
print (E1.select())
print (E2.select())
print (e2.select())
print (e1.getval('abc'))
print (e1.getval('abcdd'))
