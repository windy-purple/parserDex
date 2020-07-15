import binascii

def CalculationVar(srcByte,vara,varb):
	varA = vara
	varB = varb
	icount = 0
	listAB = []
	
	while icount < len(srcByte):
		varA = (varA + srcByte[icount]) % 65521
		varB = (varB + varA) % 65521
		icount += 1
	
	listAB.append(varA)
	listAB.append(varB)
	
	return listAB
	
def getCheckSum(varA,varB):
	Output = (varB << 16) + varA
	return Output
	
if __name__ == '__main__':
	filename = 'E:\\py\\Hello.dex'
	f = open(filename, 'rb', True)
	f.seek(0x0c)
	VarA = 1
	VarB = 0
	flag = 0
	CheckSum = 0
	while True:
		srcBytes = []
		for i in range(1024):               #一次只读1024个字节，防止内存占用过大
			ch = f.read(1)
			if not ch:                      #如果读取到末尾，设置标识符，然后退出读取循环
				flag = 1
				break
			else:
				ch = binascii.b2a_hex(ch)              #将字节转为int类型，然后添加到数组中
				ch = str(ch,encoding='utf-8')
				ch = int(ch,16)
				srcBytes.append(ch)
		varList = CalculationVar(srcBytes,VarA,VarB)
		VarA = varList[0]
		VarB = varList[1]
		if flag == 1:
			CheckSum = getCheckSum(VarA,VarB)
			break
	print(f'[*] DEX FILENAME: {filename}')
	print(f'[+] CheckSum = {hex(CheckSum)}')
