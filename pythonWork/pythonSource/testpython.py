d1 =  {'name': 'Arc_7', 'entity': 'ENTI145', 'relations': ['RELA254', 'RELA255', 'RELA239'], 'sourceref': {'ODM': ['22F83753-485E-0A8B-38A2-6C89F1ACCD4E', '2021-02-13 15:23:42.158273']}, 'uc': 'stb', 'dc': '2019-06-01 10:52:11 UTC', 'um': None, 'dm': None}
d11 = {'name': 'Arc_7', 'entity': 'ENTI145', 'relations': ['RELA254', 'RELA255', 'RELA239'], 'sourceref': {'ODM': ('22F83753-485E-0A8B-38A2-6C89F1ACCD4E', '2021-02-13 15:23:42.158273')}, 'uc': 'stb', 'dc': '2019-06-01 10:52:11 UTC', 'um': None, 'dm': None}
d2 = {"a":[1,2,3]
      ,"b":{"c":(1,4,6), "cc":(432,1,123),"ccc":()
            }
      }
d3= d2
print ("false",d1==d2)
print ("true",d2==d3)
print ("true",d1==d11)