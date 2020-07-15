import binascii
import os
import sys

def getStringsCount(f):
    f.seek(0x38)
    stringsId = f.read(4)
    a = bytearray(stringsId)
    a.reverse()
    stringsId = bytes(a)
    stringsId = str(binascii.b2a_hex(stringsId),encoding='UTF-8')
    count = int(stringsId,16)
    print('[+] stringSize ==> ' + str(count))
    return count

def getStringByteArr(f,addr):
    byteArr = bytearray()
    f.seek(addr + 1)
    b = f.read(1)
    b = str(binascii.b2a_hex(b),encoding='UTF-8')
    b = int(b,16)
    index = 2
    while b != 0:
        byteArr.append(b)
        f.seek(addr + index)
        b = f.read(1)
        b = str(binascii.b2a_hex(b),encoding='UTF-8')
        b = int(b,16)
        index = index + 1
    return byteArr

def BytesToString(byteArr):
    try:
        bs = bytes(byteArr)
        stringItem = str(bs,encoding='UTF-8')
        print('[*] str = ' + stringItem)
        return stringItem
    except:
        pass

def getAddress(addr):
    address = bytearray(addr)
    address.reverse()
    address = bytes(address)
    address = str(binascii.b2a_hex(address),encoding='UTF-8')
    address = int(address,16)
    return address

def getStrings(f,stringAmount):
    stringsList = []
    f.seek(0x3c)
    stringOff = f.read(4)
    Off = getAddress(stringOff)
    f.seek(Off)
    for i in range(stringAmount):
        addr = f.read(4)
        address = getAddress(addr)
        byteArr = getStringByteArr(f,address)
        stringItem = BytesToString(byteArr)
        stringsList.append(stringItem)
        Off = Off + 4
        f.seek(Off)
'''
    fn = str(os.path.join(sys.path[0])) + '\\strings.txt'
    file = open(fn,'a+',encoding='UTF-8')
    for line in stringsList:
        file.write(str(stringsList))
    print('[&] 文件' + fn + '写入完毕！')
    file.close()
'''

if __name__ == '__main__':
    filename = str(os.path.join(sys.path[0])) + '\\1.dex'
    f = open(filename,'rb',True)
    stringsCount = getStringsCount(f)
    getStrings(f,stringsCount)
    f.close()