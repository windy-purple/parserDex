'''
                                                    __----~~~~~~~~~~~------___
                                   .  .   ~~//====......          __--~ ~~
                   -.            \_|//     |||\\  ~~~~~~::::... /~
                ___-==_       _-~o~  \/    |||  \\            _/~~-
        __---~~~.==~||\=_    -_--~/_-~|-   |\\   \\        _/~
    _-~~     .=~    |  \\-_    '-~7  /-   /  ||    \      /
  .~       .~       |   \\ -_    /  /-   /   ||      \   /
 /  ____  /         |     \\ ~-_/  /|- _/   .||       \ /
 |~~    ~~|--~~~~--_ \     ~==-/   | \~--===~~        .\
          '         ~-|      /|    |-~\~~       __--~~
                      |-~~-_/ |    |   ~\_   _-~            /\
                           /  \     \__   \/~                \__
                       _--~ _/ | .-~~____--~-/                  ~~==.
                      ((->/~   '.|||' -_|    ~~-/ ,              . _||
                                 -_     ~\      ~~---l__i__i__i--~~_/
                                 _-~-__   ~)  \--______________--~~
                               //.-~~~-~_--~- |-------~~~~~~~~
                                      //.-~~~--\
                      ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

                              神兽保佑            永无BUG

@Author: windy_ll
@Date: 2020-07-08 16:21:27
@LastEditors: windy_ll
@LastEditTime: 2020-07-14 23:45:28
@Description: file content
'''
import binascii
import re
import os
import sys

def byte2int(bs):
    tmp = bytearray(bs)
    tmp.reverse()
    rl = bytes(tmp)
    rl = str(binascii.b2a_hex(rl),encoding='UTF-8')
    rl = int(rl,16)
    return rl

def oneByte2Int(bs):
    num = str(binascii.b2a_hex(bs),encoding='UTF-8')
    num = int(num,16)
    return num

def getSmaliName(oldname):
    newname = ''
    tmpname = oldname.split('.')
    newname = str(os.path.join(sys.path[0])) + '\\smali\\' + str(tmpname[0]) + '.smali'
    return newname

def readuleb128(f,addr):
    result = [-1,-1]
    n = 0
    f.seek(addr)
    data = oneByte2Int(f.read(1))
    if data > 0x7f:
        f.seek(addr + 1)
        n = 1
        tmp = oneByte2Int(f.read(1))
        data = (data & 0x7f) | ((tmp & 0x7f) << 7)
        if tmp > 0x7f:
            f.seek(addr + 2)
            n = 2
            tmp = oneByte2Int(f.read(1))
            data |= (tmp & 0x7f) << 14
            if tmp > 0x7f:
                f.seek(addr + 3)
                n = 3
                tmp = oneByte2Int(f.read(1))
                data |= (tmp & 0x7f) << 21
                if tmp > 0x7f:
                    f.seek(addr + 4)
                    n = 4
                    tmp = oneByte2Int(f.read(1))
                    data |= tmp << 28
    result[0] = data
    result[1] = addr + n + 1
    return result

def getAccessFlags(flag):
    accessFlag = ''
    flagList = [0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x100,0x200,0x400,0x800,0x2000,0x4000,0x10000]
    flagdict = {0x01:'public',0x02:'private',0x04:'protected',0x08:'static',0x10:'final',0x20:'synchronized',0x40:'volatile',0x80:'transient',0x100:'native',\
        0x200:'interface',0x400:'abstract',0x800:'strictfp',0x2000:'annotayion',0x4000:'enum',0x10000:'constructor'}
    if flag == 0x1:
        accessFlag = 'public'
    elif flag == 0x2:
        accessFlag = 'private'
    elif flag == 0x4:
        accessFlag = 'protected'
    elif flag == 0x8:
        accessFlag = 'static'
    elif flag == 0x10:
        accessFlag = 'final'
    elif flag == 0x20:
        accessFlag = 'synchronized'
    elif flag == 0x40:
        accessFlag = 'volatile'
    elif flag == 0x80:
        accessFlag = 'transient'
    elif flag == 0x100:
        accessFlag = 'native'
    elif flag == 0x200:
        accessFlag = 'interface'
    elif flag == 0x400:
        accessFlag = 'abstract'
    elif flag == 0x800:
        accessFlag = 'strictfp'
    elif flag == 0x2000:
        accessFlag = flagdict[0x2000]
    elif flag == 0x4000:
        accessFlag = flagdict[0x4000]
    elif flag == 0x10000:
        accessFlag = flagdict[0x10000]
    else:
        mark = 0
        for k in range(14):
            if mark == 1:
                break
            for item in flagList[(k + 1):]:
                if flag == (flagList[k] | item):
                    idx1 = flagList[k]
                    idx2 = item
                    accessFlag = flagdict[idx1] + ' ' + flagdict[idx2]
                    mark = 1
                    break
    return accessFlag

def parseTypeList(f,addr,tList):
    paramList = []
    f.seek(addr)
    size = byte2int(f.read(4))
    if size == 0:
        return paramList
    else:
        addr = addr + 4
        for k in range(size):
            f.seek(addr + (k * 2))
            paramString = typeList[byte2int(f.read(2))]
            paramList.append(paramString)
    return paramList

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

def getTypeAmount(f):
    f.seek(0x40)
    stringsId = f.read(4)
    count = byte2int(stringsId)
    return count

def getclassCount(f):
    f.seek(0x60)
    class_num = f.read(4)
    class_size = byte2int(class_num)
    return class_size

def getStringsCount(f):
    f.seek(0x38)
    stringsId = f.read(4)
    count = byte2int(stringsId)
    return count

def getStrings(f,stringAmount):
    stringsList = []
    f.seek(0x3c)
    stringOff = f.read(4)
    Off = byte2int(stringOff)
    f.seek(Off)
    for i in range(stringAmount):
        addr = f.read(4)
        address = byte2int(addr)
        byteArr = getStringByteArr(f,address)
        stringItem = BytesToString(byteArr)
        stringsList.append(stringItem)
        Off = Off + 4
        f.seek(Off)
    return stringsList

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

def parserField(f,stringList,typelist):
    fieldList = []
    f.seek(0x50)
    fieldSize = byte2int(f.read(4))
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
        fieldStr = nameIdx + ':' + typeIdx
        fieldList.append(fieldStr)
    return fieldList

def parseProtold(f,typeList,stringList):
    pList = []
    f.seek(0x48)
    protoldSizeTmp = f.read(4)
    protoldSize = byte2int(protoldSizeTmp)
    f.seek(0x4c)
    protoldAddr = byte2int(f.read(4))
    for i in range(protoldSize):
        f.seek(protoldAddr)
        AllString = stringList[byte2int(f.read(4))]
        protoldAddr += 4
        f.seek(protoldAddr)
        returnString = typeList[byte2int(f.read(4))]
        protoldAddr += 4
        f.seek(protoldAddr)
        paramAddr = byte2int(f.read(4))
        if paramAddr == 0:
            protoldAddr += 4
            pList.append(returnString + '()')
            continue
        f.seek(paramAddr)
        paramSize = byte2int(f.read(4))
        paramList = []
        if paramSize == 0:
            pass
        else:
            paramAddr = paramAddr + 4
            for k in range(paramSize):
                f.seek(paramAddr + (k * 2))
                paramString = typeList[byte2int(f.read(2))]
                paramList.append(paramString)
        protoldAddr += 4
        paramTmp = []
        for paramItem in paramList:
            paramTmp.append(paramItem)
        param = returnString + '(' + ','.join(paramTmp) + ')'
        pList.append(param)
    return pList

def parserMethod(f,stringlist,typelist,protoldlist):
    methodlist = []
    f.seek(0x58)
    methodSize = byte2int(f.read(4))
    f.seek(0x5c)
    methodAddr = byte2int(f.read(4))
    for i in range(methodSize):
        f.seek(methodAddr)
        classIdx = typelist[byte2int(f.read(2))]
        f.seek(methodAddr + 2)
        protoldIdx = protoldlist[byte2int(f.read(2))]
        f.seek(methodAddr + 4)
        nameIdx = stringlist[byte2int(f.read(4))]
        tmp = protoldIdx.split('(',1)
        methodItem = nameIdx + '(' + str(tmp[1]) + str(tmp[0])
        methodlist.append(methodItem)
        methodAddr += 8
    return methodlist

def parseBytecode(f,addr,bytecount,stringsList,fieldsList,methodsList):
    codestr = ''
    n = 0
    while True:
        f.seek(addr)
        op = byte2int(f.read(1))
        if op == 0x0e:
            codestr += '\treturn-void\r\n'
            addr = addr + 2
            n += 2
        elif op == 0x1a:
            f.seek(addr + 1)
            register = oneByte2Int(f.read(1))
            f.seek(addr + 2)
            idx = byte2int(f.read(2))
            stringIdx = stringsList[idx]
            re.sub("[\n]","",stringIdx)
            re.sub("[\r]","",stringIdx)
            codestr += '\tconst-string v' + str(register) + ', "' + stringIdx + '"\r\n'
            addr = addr + 4
            n += 4
        elif op == 0x62:
            f.seek(addr + 1)
            register = oneByte2Int(f.read(1))
            f.seek(addr + 2)
            idx = byte2int(f.read(2))
            codestr += '\tset-object v' + str(register) + ', ' + fieldsList[idx] + '\r\n'
            addr = addr + 4
            n += 4
        elif op == 0x70 or op == 0x6e:
            f.seek(addr + 1)
            data = oneByte2Int(f.read(1))
            f.seek(addr + 4)
            data1 = oneByte2Int(f.read(1))
            f.seek(addr + 5)
            data2 = oneByte2Int(f.read(1))
            f.seek(addr + 2)
            idx = byte2int(f.read(2))
            registerNum = (data & 0xf0) >> 4
            register = ''
            if registerNum == 1:
                register_1 = data & 0xf
                register = '{v' + str(register_1) + '}, '
            elif registerNum == 2:
                register_1 = data & 0xf
                register_2 = (data1 & 0xf0) >> 4
                register = '{v' + str(register_1) + ', v' + str(register_2) + '}, '
            elif registerNum == 3:
                register_1 = data & 0xf
                register_2 = (data1 & 0xf0) >> 4
                register_3 = data1 & 0xf
                register = '{v' + str(register_1) + ', v' + str(register_2) + ', v' + str(register_3) + '}, '
            elif registerNum == 4:
                register_1 = data & 0xf
                register_2 = (data1 & 0xf0) >> 4
                register_3 = data1 & 0xf
                register_4 = (data2 & 0xf0) >> 4
                register = '{v' + str(register_1) + ', v' + str(register_2) + ', v' + str(register_3) + ', v' + str(register_4) + '}, '
            else:
                register_1 = data & 0xf
                register_2 = (data1 & 0xf0) >> 4
                register_3 = data1 & 0xf
                register_4 = (data2 & 0xf0) >> 4
                register_5 = data2 & 0xf
                register = '{v' + str(register_1) + ', v' + str(register_2) + ', v' + str(register_3) + ', v' + str(register_4) + ', v' + str(register_5) + '}, '
            if op == 0x70:
                codestr += '\tinvoke-direct ' + register + methodsList[idx] + '\r\n'
            else:
                codestr += '\tinvoke-virtual ' + register + methodsList[idx] + '\r\n'
            addr = addr + 6
            n += 6
        else:
            pass
        if n == bytecount:
            break
    return codestr
        

def parseCode(f,addr,fn,slist,flist,mlist):
    f.seek(addr)
    register_size = byte2int(f.read(2))
    f.seek(addr + 2)
    ins_size = byte2int(f.read(2))
    f.seek(addr + 4)
    out_size = byte2int(f.read(2))
    f.seek(addr + 6)
    try_size = byte2int(f.read(2))
    f.seek(addr + 8)
    debug_off = byte2int(f.read(4))
    f.seek(addr + 12)
    insns_size = byte2int(f.read(4))
    address = addr + 16
    bytecount = insns_size * 2
    registerString = '\t.register ' + str(register_size) + '\r\n'
    fn.write(registerString)
    codestr = parseBytecode(f,address,bytecount,slist,flist,mlist)
    fn.write(codestr)
    endstr = '.end method\r\n'
    fn.write(endstr)

def parseClassData(f,addr,fn,fList,mList,strsList):
    re = readuleb128(f,addr)
    static_fields_size = re[0]
    address = re[1]
    re = readuleb128(f,address)
    instance_fields_size = re[0]
    address = re[1]
    re = readuleb128(f,address)
    direct_method_size = re[0]
    address = re[1]
    re = readuleb128(f,address)
    virtual_method_size = re[0]
    address = re[1]
    fieldStr = ''
    if static_fields_size != 0:
        fieldStr += '# static fields\r\n'
        for i in range(static_fields_size):
            re = readuleb128(f,address)
            fieldidx = re[0]
            address = re[1]
            re = readuleb128(f,address)
            accflag = re[0]
            address = re[1]
            fieldStr += '.field ' + getAccessFlags(accflag) + ' ' + fList[fieldidx] + '\r\n'
        fieldStr += '\r\n\r\n'
        fn.write(fieldStr)
    fieldStr = ''
    if instance_fields_size != 0:
        fieldStr += '# instance fields\r\n'
        for i in range(instance_fields_size):
            re = readuleb128(f,address)
            fieldidx = re[0]
            address = re[1]
            re = readuleb128(f,address)
            accflag = re[0]
            address = re[1]
            fieldStr += '.field ' + getAccessFlags(accflag) + ' ' + fList[fieldidx] + '\r\n'
        fieldStr += '\r\n\r\n'
        fn.write(fieldStr)
    methodStr = ''
    if direct_method_size != 0:
        methodStr += '# direct methods\r\n'
        fn.write(methodStr)
        for i in range(direct_method_size):
            re = readuleb128(f,address)
            methodidx = re[0]
            address = re[1]
            re = readuleb128(f,address)
            accflag = re[0]
            address = re[1]
            re = readuleb128(f,address)
            code_off = re[0]
            address = re[1]
            methodStr = '.method ' + getAccessFlags(accflag) + ' ' + mList[methodidx] + '\r\n'
            fn.write(methodStr)
            parseCode(f,code_off,fn,strsList,fList,mList)
        methodStr = '\r\n\r\n'
        fn.write(methodStr)
    methodStr = ''
    if virtual_method_size != 0:
        methodStr = '# virtual methods\r\n'
        fn.write(methodStr)
        for i in range(virtual_method_size):
            re = readuleb128(f,address)
            methodidx = re[0]
            address = re[1]
            re = readuleb128(f,address)
            accflag = re[0]
            address = re[1]
            re = readuleb128(f,address)
            code_off = re[0]
            address = re[1]
            methodStr = '.method ' + getAccessFlags(accflag) + ' ' + mList[methodidx] + '\r\n'
            fn.write(methodStr)
            parseCode(f,code_off,fn,strsList,fList,mList)
        methodStr = '\r\n\r\n'
        fn.write(methodStr)

def parseClassDefItem(f,class_num,tList,sList,fieldlist,methodlist):
    f.seek(0x64)
    addr = byte2int(f.read(4))
    for i in range(class_num):
        f.seek(addr)
        classIdx = tList[byte2int(f.read(4))]
        f.seek(addr + 4)
        accessFlags = getAccessFlags(byte2int(f.read(4)))
        if accessFlags != 'error':
            pass
        f.seek(addr + 8)
        superclass_idx = tList[byte2int(f.read(4))]
        f.seek(addr + 12)
        interfaces_off = byte2int(f.read(4))
        if interfaces_off == 0:
            pass
        else:
            parseTypeList(f,interfaces_off,tList)
        f.seek(addr + 16)
        sourceFileIdx = sList[byte2int(f.read(4))]
        f.seek(addr + 20)
        annotions_off = byte2int(f.read(4))
        address = 0
        f.seek(addr + 24)
        class_data_off = byte2int(f.read(4))
        f.seek(addr + 28)
        static_value_off = byte2int(f.read(4))
        fname = getSmaliName(sourceFileIdx)
        fn = open(fname,'a+',True)
        headstr = '.class ' + str(accessFlags) + ' ' + str(classIdx) + '\r\n'
        headstr += '.super ' + str(superclass_idx) + '\r\n'
        headstr += '.source ' + '"' + str(sourceFileIdx) + '"\r\n\r\n'
        fn.write(headstr)
        if class_data_off != 0:
            parseClassData(f,class_data_off,fn,fieldlist,methodlist,sList)
        fn.close()
        print('[*] %s文件的类%s写入完毕！'%(fname,classIdx))
        addr += 32
    

if __name__ == '__main__':
    filename = str(os.path.join(sys.path[0])) + '\\Hello.dex'
    dir = str(os.path.join(sys.path[0])) + '\\smali'
    if not os.path.exists(dir):
        os.makedirs(dir)
    f = open(filename,'rb',True)
    stringsCount = getStringsCount(f)
    strList = getStrings(f,stringsCount)
    typeCount = getTypeAmount(f)
    typeList = getTypeItem(f,typeCount,strList)
    fieldList = parserField(f,strList,typeList)
    protoldList = parseProtold(f,typeList,strList)
    methodList = parserMethod(f,strList,typeList,protoldList)
    classNum = getclassCount(f)
    parseClassDefItem(f,classNum,typeList,strList,fieldList,methodList)
    f.close()