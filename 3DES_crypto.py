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
            des3 = DES.new(self.key, input_mode, nonce=b'asdf')
        encmsg = des3.encrypt(msg.encode())  # 암호화 하는 자리

        return encmsg, fillernum

    def dec(self, msg, input_mode, fillernum):
        if input_mode == DES.MODE_CBC:
            # cbc 모드
            des3 = DES.new(self.key, input_mode, self.iv)
        elif input_mode == DES.MODE_CTR:
            # ctr 모드
            des3 = DES.new(self.key, input_mode, nonce=b'asdf')
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

    f = open('./big_string_data/data_3GB.txt', 'r')
    lines = f.readlines()
    mymsg = ''
    for s in lines:
        mymsg += s

    enc_start_time = time.time()
    encrypted, fillter_num = mycipher.enc(mymsg, mode)
    enc_end_time = time.time()

    print('Plaintext  :', mymsg)
    print(encrypted)
    print('Encrypted  :', 'encrypted', 'time : ', enc_end_time - enc_start_time)

    dec_start_time = time.time()
    decrypted = mycipher.dec(encrypted, mode, fillter_num)
    dec_end_time = time.time()
    print('Decrypted  :', 'decrypted', 'time : ', dec_end_time - dec_start_time)

if __name__ == '__main__':
    main()