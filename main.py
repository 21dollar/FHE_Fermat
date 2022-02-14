from TestEncryption import TestEncryption
from fhe import FHE_Fermat


h = 3
l = 3
f = h + l
E = 5

instance = FHE_Fermat(h, l, f, E)
test = TestEncryption(instance)




Z = instance.encryption_of_zero()
print(Z)
Z = instance.decrypt_number(Z)
print(Z)


Z = instance.encrypt_number(12)
print(Z)
Z = instance.decrypt_number(Z)
print(Z)