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
    return stringsList

def getTypeAmount(f):
    f.seek(0x40)
    stringsId = f.read(4)
    a = bytearray(stringsId)
    a.reverse()
    stringsId = bytes(a)
    stringsId = str(binascii.b2a_hex(stringsId),encoding='UTF-8')
    count = int(stringsId,16)
    return count

def getTypeItem(f,count,strLists):
    f.seek(0x44)
    type_ids_off = f.read(4)
    a = bytearray(type_ids_off)
    a.reverse()
    type_ids_off = bytes(a)
    type_ids_off = binascii.b2a_hex(type_ids_off)
    type_ids_off = str(type_ids_off,encoding='utf-8')
    type_off = int(type_ids_off,16)
    f.seek(type_off)
    print('[+] type count ==> ',end='')
    print(count)
    for i in range(count):
        typeIndex = f.read(4)
        b = bytearray(typeIndex)
        b.reverse()
        typeIndex = bytes(b)
        typeIndex = binascii.b2a_hex(typeIndex)
        typeIndex = int(str(typeIndex,encoding='UTF-8'),16)
        print('[*] typeItem ==> ',end='')
        print(strLists[typeIndex])
        type_off = type_off + 0x04
        f.seek(type_off)

if __name__ == '__main__':
    filename = str(os.path.join(sys.path[0])) + '\\1.dex'
    f = open(filename,'rb',True)
    stringsCount = getStringsCount(f)
    strList = getStrings(f,stringsCount)
    typeCount = getTypeAmount(f)
    getTypeItem(f,typeCount,strList)
    f.close()