
from IM_OBJECTS import schnittstelleattr

if (__name__ == '__main__'):
    s = schnittstelleattr.Schnittstelleattr()
    print (os.system('pwd'),sys.path)
    print(s.__dict__,s.scha_id)
    s.select()
    print (s.anker())