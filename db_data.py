import json

import pymysql
from Crypto.Cipher import DES3 as DES
from Crypto.Hash import SHA256 as SHA
import time


class MyDES:
    def __init__(self, key, iv):
        myhash = SHA.new()
        myhash.update(key.encode())
        tkey = myhash.digest()
        self.key = tkey[:24]
        print('key : ' + str(self.key))

        myhash.update(iv.encode())
        tiv = myhash.digest()
        self.iv = tiv[:8]
        print('iv : ' + str(self.iv))

    def enc(self, msg, input_mode):
        msg, fillernum = self.make8string(msg)
        if input_mode == DES.MODE_CBC:
            # cbc 모드
            des3 = DES.new(self.key, input_mode, self.iv)
        elif input_mode == DES.MODE_CTR:
            # ctr 모드
            des3 = DES.new(self.key, input_mode, nonce=b'')
        encmsg = des3.encrypt(msg.encode())  # 암호화 하는 자리

        return encmsg, fillernum

    def dec(self, msg, input_mode, fillernum):
        if input_mode == DES.MODE_CBC:
            # cbc 모드
            des3 = DES.new(self.key, input_mode, self.iv)
        elif input_mode == DES.MODE_CTR:
            # ctr 모드
            des3 = DES.new(self.key, input_mode, nonce=b'')
        decmsg = des3.decrypt(msg)
        decmsg = decmsg.decode()

        if fillernum != 0:
            decmsg = decmsg[:-fillernum]

        return decmsg

    def make8string(self, msg):
        msglen = len(msg)
        filler = ''
        if msglen % 8 != 0:
            filler = 'O' * (8 - msglen % 8)

        fillernum = len(filler)
        msg += filler

        return msg, fillernum


def main():
    mykey = 'tkdrms0301'
    myiv = 'tkdrms0301'

    # 암호화 mode 변경 : DES.MODE_CBC, DES.MODE_CTR
    #mode = DES.MODE_CBC
    mode = DES.MODE_CTR

    mycipher = MyDES(mykey, myiv)

    # 문자열만 입력 가능
    # bool, int, byte 타입 전부 string으로 변환 필요함
    # str(mymsg)

    # DB Connection 생성
    # user, password, db
    conn = pymysql.connect(host='localhost', user='root', password='tkd5957!@#', db='crypto', charset='utf8')
    cursor = conn.cursor()

    # query 문
    query = "SELECT * FROM dataset"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    f = open('db_data.txt', 'w')
    f.close()

    f = open('db_data.txt', 'ab')
    enc_start_time = time.time()
    for row in rows:
        encrypted, fillter_num = mycipher.enc(str(row[0]), mode)
        f.write(encrypted)
        f.write(bytes('\n'.encode()))
        f.write(bytes([fillter_num]))
        f.write(bytes('\n'.encode()))

        encrypted, fillter_num = mycipher.enc(row[1], mode)
        f.write(encrypted)
        f.write(bytes('\n'.encode()))
        f.write(bytes([fillter_num]))
        f.write(bytes('\n'.encode()))

        encrypted, fillter_num = mycipher.enc(str(row[2]), mode)
        f.write(encrypted)
        f.write(bytes('\n'.encode()))
        f.write(bytes([fillter_num]))
        f.write(bytes('\n'.encode()))

        encrypted, fillter_num = mycipher.enc(row[3], mode)
        f.write(encrypted)
        f.write(bytes('\n'.encode()))
        f.write(bytes([fillter_num]))
        f.write(bytes('\n'.encode()))

        encrypted, fillter_num = mycipher.enc(str(row[4]), mode)
        f.write(encrypted)
        f.write(bytes('\n'.encode()))
        f.write(bytes([fillter_num]))
        f.write(bytes('\n'.encode()))

    enc_end_time = time.time()

    print('time : ' + str(enc_end_time - enc_start_time))
    # 새로 암호화하거나 복화할 때 새로 생성 해주지 않으면 에러 발생함
    # https://stackoverflow.com/questions/54082280/typeerror-decrypt-cannot-be-called-after-encrypt
    # des3 = DES.new(key, DES.MODE_CBC, iv)
    # dec = des3.decrypt(enc)
    # print(dec)

    f = open('db_data.txt', 'rb')
    data_list = f.readlines()
    list = []
    count = 10

    dec_start_time = time.time()
    for i in range(int(len(data_list) / 10)):
        i = i * count;
        dictionary = dict()
        dictionary['id'] = mycipher.dec(data_list[i].replace(b'\n',b''), mode, int.from_bytes(data_list[i+1].replace(b'\n',b''), "big"))
        dictionary['name'] = mycipher.dec(data_list[i+2].replace(b'\n',b''), mode, int.from_bytes(data_list[i+3].replace(b'\n',b''), "big"))
        dictionary['age'] = mycipher.dec(data_list[i+4].replace(b'\n',b''), mode, int.from_bytes(data_list[i+5].replace(b'\n',b''), "big"))
        dictionary['email'] = mycipher.dec(data_list[i+6].replace(b'\n',b''), mode, int.from_bytes(data_list[i+7].replace(b'\n',b''), "big"))
        dictionary['sex'] = mycipher.dec(data_list[i+8].replace(b'\n',b''), mode, int.from_bytes(data_list[i+9].replace(b'\n',b''), "big"))
        print(dictionary)
        list.append(dictionary)
    dec_end_time = time.time()
    print('Decrypted  :', 'decrypted', 'time : ', dec_end_time - dec_start_time)
    print('finish')
'''
 enc_start_time = time.time()
    encrypted, fillter_num = mycipher.enc(mymsg, mode)
    enc_end_time = time.time()

    print('Plaintext  :', mymsg)
    #print(encrypted)
    print('Encrypted  :', 'encrypted', 'time : ', enc_end_time - enc_start_time)

    #dec_start_time = time.time()
    #decrypted = mycipher.dec(encrypted, mode, fillter_num)
    #dec_end_time = time.time()
    #print('Decrypted  :', 'decrypted', 'time : ', dec_end_time - dec_start_time)
'''


if __name__ == '__main__':
    main()