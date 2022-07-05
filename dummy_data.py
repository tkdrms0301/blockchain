import lorem
import os

# 더미 데이터 제작 string

size = 0
f = open('big_string_data/data_1MB.txt', 'w')
f.close()
while True:
    if size > 1: #1MB 10MB 100MB 1000MB 3000MB
        break
    f = open('big_string_data/data_1MB.txt', 'a')
    f.write(lorem.paragraph() * 10 + '\n')
    f.close()
    size = os.path.getsize('big_string_data/data_1MB.txt') / (1024.0 * 1024.0) #MB 단위
    print(size)