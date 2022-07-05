from Crypto.Cipher import DES3 as DES
from Crypto.Hash import SHA256 as SHA

key = 'tkdrms0301'
iv = 'tkdrms0301'
myhash = SHA.new()
myhash.update(key.encode())
tkey = myhash.digest()
key = tkey[:24]
print(str(key)) # key 값 문자열로 파일에 저장

#파일에 저장
f = open('./key/key.txt', 'wb')
f.write(key)
f.close()

myhash.update(iv.encode())
tiv = myhash.digest()
iv = tiv[:8]
print(iv) # iv 값 문자열로 파일에 저장

#파일에 저장
f = open('./key/iv.txt', 'wb')
f.write(iv)
f.close()

#파일에서 key값 읽기
f = open('./key/key.txt', 'rb')
key_value = f.readline()
print(type(key_value))
print(key_value)
f.close()

#파일에서 iv값 읽기
f = open('./key/iv.txt', 'rb')
iv_value = f.readline()
print(type(iv_value))
print(iv_value)
f.close()

des3 = DES.new(key_value, DES.MODE_CBC, iv_value)
mymsg = 'asdfaaaa'
enc = des3.encrypt(mymsg.encode())
print(enc)

# 새로 암호화하거나 복화할 때 새로 생성 해주지 않으면 에러 발생함
# https://stackoverflow.com/questions/54082280/typeerror-decrypt-cannot-be-called-after-encrypt
des3 = DES.new(key, DES.MODE_CBC, iv)
dec = des3.decrypt(enc)
print(dec)

import sys
print(sys.version)