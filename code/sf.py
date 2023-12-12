#fingerprints the message using SHA-256 algorithm
#using sha256 algorithm to hash the message along with the timestamp
#the timestamp is using ISO 8601 format
from datetime import datetime

# 获取当前日期和时间
current_datetime = datetime.now()

# 格式化输出
formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
print(formatted_datetime)

input = 'temperature37_' + '2023-10-23 14:30:00'

binaries = input.encode('utf8')

M = binaries + b'\x80' + b'\x00'*(64-len(binaries)-1-8) + (len(binaries)*8).to_bytes(8, byteorder='big')
#print(M.hex())

#predefined 
# initHash stands for the initial hash value
# const stands for the predefined constants
# messSchedule stands for the message schedule
initHash = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]

const = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2]

messSchedule = [0] * 64

for temp in range(0, 16):
    messSchedule[temp] = M[temp * 4:temp * 4 + 4]
    messSchedule[temp] = int(messSchedule[temp].hex(), 16)
#print(W[0:16])

def ROTR(x, n):
    x = (x >> n) | (x << 32 - n)
    return x

for i in range(16, 64):
    S1 = ROTR(messSchedule[i - 2], 17) ^ ROTR(messSchedule[i - 2], 19) ^ (messSchedule[i - 2]>>10)
    S0 = ROTR(messSchedule[i - 15], 7) ^ ROTR(messSchedule[i - 15], 18) ^ (messSchedule[i - 15] >> 3)
    messSchedule[i] = (S1 + messSchedule[i-7] + S0 + messSchedule[i-16]) & 0xFFFFFFFF
#print(W)
a = initHash[0]
b = initHash[1]
c = initHash[2]
d = initHash[3]
e = initHash[4]
f = initHash[5]
g = initHash[6]
h = initHash[7]

for j in range(0, 64):
    S1 = ROTR(e, 6) ^ ROTR(e, 11) ^ ROTR(e, 25)
    Ch = (e & f) ^ ((~e) & g)
    S0 = ROTR(a, 2) ^ ROTR(a, 13) ^ ROTR(a, 22)
    Maj = (a & b) ^ (a & c) ^ (b & c)
    T1 = h + S1 + Ch + const[j] + messSchedule[j]
    T2 = S0 + Maj
    h = g
    g = f
    f = e
    e = (d + T1) & 0xFFFFFFFF
    d = c
    c = b
    b = a
    a = (T1 + T2) & 0xFFFFFFFF


initHash[0] = a + initHash[0] & 0xFFFFFFFF
initHash[1] = b + initHash[1] & 0xFFFFFFFF
initHash[2] = c + initHash[2] & 0xFFFFFFFF
initHash[3] = d + initHash[3] & 0xFFFFFFFF
initHash[4] = e + initHash[4] & 0xFFFFFFFF
initHash[5] = f + initHash[5] & 0xFFFFFFFF
initHash[6] = g + initHash[6] & 0xFFFFFFFF
initHash[7] = h + initHash[7] & 0xFFFFFFFF

sha256 = ''
for sha in initHash:
    #print(hex(sha))
    sha256 = sha256 + sha.to_bytes(4, byteorder='big').hex()
print(sha256)


# import hashlib
# print(hashlib.sha256(binaries).hexdigest())
# if sha256 == hashlib.sha256(binaries).hexdigest():
#     print('the same outcome with hashlib.sha256')
    