import binascii
import os
import sys

def byte2int(bs):
    tmp = bytearray(bs)
    tmp.reverse()
    rl = bytes(tmp)
    rl = str(binascii.b2a_hex(rl),encoding='UTF-8')
    rl = int(rl,16)
    return rl

def getStringsCount(f):
    f.seek(0x38)
    stringsId = f.read(4)
    count = byte2int(stringsId)
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
    count = byte2int(stringsId)
    return count

def getTypeItem(f,count,strLists):
    typeList = []
    f.seek(0x44)
    type_ids_off = f.read(4)
    type_off = byte2int(type_ids_off)
    f.seek(type_off)
    for i in range(count):
        typeIndex = f.read(4)
        typeIndex = byte2int(typeIndex)
        typeList.append(strLists[typeIndex])
        type_off = type_off + 0x04
        f.seek(type_off)
    return typeList

def changeDisplay(viewString):
    display = ''
    if viewString == 'V':
        display = 'void'
    elif viewString == 'Z':
        display = 'boolean'
    elif viewString == 'B':
        display = 'byte'
    elif viewString == 'S':
        display = 'short'
    elif viewString == 'C':
        display = 'char'
    elif viewString == 'I':
        display = 'int'
    elif viewString == 'J':
        display = 'long'
    elif viewString == 'F':
        display = 'float'
    elif viewString == 'D':
        display = 'double'
    elif viewString[0:1] == 'L':
        display = viewString[1:-1]
    elif viewString[0:1] == '[':
        if viewString[1:2] == 'L':
            display = viewString[2:-1] + '[]'
        else:
            if viewString[1:] == 'Z':
                display = 'boolean[]'
            elif viewString[1:] == 'B':
                display = 'byte[]'
            elif viewString[1:] == 'S':
                display = 'short[]'
            elif viewString[1:] == 'C':
                display = 'char[]'
            elif viewString[1:] == 'I':
                display = 'int[]'
            elif viewString[1:] == 'J':
                display = 'long[]'
            elif viewString[1:] == 'F':
                display = 'float[]'
            elif viewString[1:] == 'D':
                display = 'double[]'
            else:
                display = ''
    else:
        display = ''
    return display

def parserField(f,stringList,typelist):
    fieldList = []
    f.seek(0x50)
    fieldSize = byte2int(f.read(4))
    print('[+] field size ==> ',end='')
    print(fieldSize)
    fieldAddr = byte2int(f.read(4))
    for i in range(fieldSize):
        fieldStr = ''
        f.seek(fieldAddr)
        classIdx = typelist[byte2int(f.read(2))]
        f.seek(fieldAddr + 2)
        typeIdx = typelist[byte2int(f.read(2))]
        f.seek(fieldAddr + 4)
        nameIdx = stringList[byte2int(f.read(4))]
        fieldAddr += 8
        fieldStr = changeDisplay(typeIdx) + ' ' + changeDisplay(classIdx) + '.' + nameIdx
        fieldList.append(fieldStr)
    return fieldList


if __name__ == '__main__':
    filename = str(os.path.join(sys.path[0])) + '\\1.dex'
    f = open(filename,'rb',True)
    stringsCount = getStringsCount(f)
    strList = getStrings(f,stringsCount)
    typeCount = getTypeAmount(f)
    typeList = getTypeItem(f,typeCount,strList)
    fieldList = parserField(f,strList,typeList)
    print(fieldList)
    f.close()