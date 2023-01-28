import re
l = ['5', '*', '3']
print(type(l))
print(l)
print(type(str(l)))
print(str(l))

m = 'x5*3y'
print(m)
print(re.sub(str(l), '----', m))
print( 5 ** 2)