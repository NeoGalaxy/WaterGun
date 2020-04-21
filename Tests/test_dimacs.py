from classes import CNF
c = CNF(["5","-2","z"],["z","a","-5"],["2","-z"],["-a"])
print (c)
c.ecrDimacs("test_ecrDimacs.txt")