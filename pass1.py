import sys
import re

Mnemonics = {
    "+LDB": [0x68, 4],
    "MULR": [0x98, 2],
    "+SSK": [0xEC, 4],
    "WD": [0xDC, 3],
    "*STX": [0x10, 3],
    "*OR": [0x44, 3],
    "AND": [0x40, 3],
    "*LDA": [0x00, 3],
    "+JGT": [0x34, 4],
    "+STL": [0x14, 4],
    "*WD": [0xDC, 3],
    "+STI": [0xD4, 4],
    "LPS": [0xD0, 3],
    "+LDT": [0x74, 4],
    "*LDCH": [0x50, 3],
    "*LDL": [0x08, 3],
    "TIXR": [0xB8, 2],
    "SUBF": [0x5C, 3],
    "*JSUB": [0x48, 3],
    "LDX": [0x04, 3],
    "+MULF": [0x60, 4],
    "+J": [0x3C, 4],
    "SVC": [0xB0, 2],
    "STT": [0x84, 3],
    "+COMP": [0x28, 4],
    "TIX": [0x2C, 3],
    "FLOAT": [0xC0, 1],
    "LDT": [0x74, 3],
    "STA": [0x0C, 3],
    "*TD": [0xE0, 3],
    "SHIFTR": [0xA8, 2],
    "STB": [0x78, 3],
    "SIO": [0xF0, 1],
    "LDA": [0x00, 3],
    "HIO": [0xF4, 1],
    "+STS": [0x7C, 4],
    "DIVF": [0x64, 3],
    "*TIX": [0x2C, 3],
    "+JSUB": [0x48, 4],
    "LDCH": [0x50, 3],
    "+COMPF": [0x88, 4],
    "JEQ": [0x30, 3],
    "*DIV": [0x24, 3],
    "+STT": [0x84, 4],
    "+SUBF": [0x5C, 4],
    "*AND": [0x40, 3],
    "+OR": [0x44, 4],
    "SSK": [0xEC, 3],
    "+JLT": [0x38, 4],
    "*RD": [0xD8, 3],
    "LDS": [0x6C, 3],
    "*MUL": [0x20, 3],
    "+LDS": [0x6C, 4],
    "+DIV": [0x24, 4],
    "J": [0x3C, 3],
    "+MUL": [0x20, 4],
    "*COMP": [0x28, 3],
    "+STX": [0x10, 4],
    "*J": [0x3C, 3],
    "+LDA": [0x00, 4],
    "+SUB": [0x1C, 4],
    "+STB": [0x78, 4],
    "*JLT": [0x38, 3],
    "SUB": [0x1C, 3],
    "+ADDF": [0x58, 4],
    "RD": [0xD8, 3],
    "*JEQ": [0x30, 3],
    "LDB": [0x68, 3],
    "RSUB": [0x4C, 3],
    "MULF": [0x60, 3],
    "JSUB": [0x48, 3],
    "SUBR": [0x94, 2],
    "DIVR": [0x9C, 2],
    "LDL": [0x08, 3],
    "+JEQ": [0x30, 4],
    "+STCH": [0x54, 4],
    "*STL": [0x14, 3],
    "+STA": [0x0C, 4],
    "STSW": [0xE8, 3],
    "COMPF": [0x88, 3],
    "+DIVF": [0x64, 4],
    "+STF": [0x80, 4],
    "TIO": [0xF8, 1],
    "*ADD": [0x18, 3],
    "*STSW": [0xE8, 3],
    "+STSW": [0xE8, 4],
    "+LPS": [0xD0, 4],
    "JLT": [0x38, 3],
    "*JGT": [0x34, 3],
    "MUL": [0x20, 3],
    "+LDL": [0x08, 4],
    "OR": [0x44, 3],
    "COMP": [0x28, 3],
    "TD": [0xE0, 3],
    "STS": [0x7C, 3],
    "*STCH": [0x54, 3],
    "LDF": [0x70, 3],
    "ADD": [0x18, 3],
    "FIX": [0xC4, 1],
    "*RSUB": [0x4C, 3],
    "NORM": [0xC8, 1],
    "STF": [0x80, 3],
    "*LDX": [0x04, 3],
    "CLEAR": [0xB4, 2],
    "+RSUB": [0x4C, 4],
    "ADDF": [0x58, 3],
    "+WD": [0xDC, 4],
    "+LDCH": [0x50, 4],
    "+LDF": [0x70, 4],
    "+LDX": [0x04, 4],
    "STCH": [0x54, 3],
    "+ADD": [0x18, 4],
    "+AND": [0x40, 4],
    "*SUB": [0x1C, 3],
    "STX": [0x10, 3],
    "RMO": [0xAC, 2],
    "COMPR": [0xA0, 2],
    "SHIFTL": [0xA4, 2],
    "STL": [0x14, 3],
    "+TD": [0xE0, 4],
    "ADDR": [0x90, 2],
    "STI": [0xD4, 3],
    "+TIX": [0x2C, 4],
    "*STA": [0x0C, 3],
    "JGT": [0x34, 3],
    "DIV": [0x24, 3],
    "+RD": [0xD8, 4],
}

DIRECTS = ['START', 'END', 'LTORG', 'BASE', 'RESW', 'WORD', 'BYTE']
LITDIC = []

lst = open(sys.argv[1][:4] + ".lst", "w")
obj = open(sys.argv[1][:4] + ".obj", "w")


# lst.write("Test")

def litFunc(LITDIC):
    val = ""
    # print("got here2")
    for x in LITDIC:
        # print("got here3")
        if x[1] == 'C':
            # print("got here4")
            swank = x[3:len(x) - 1]
            for y in swank:
                # print("got here5")
                val = val + str(ord(y))
            # print("got here6")
            print("This is literal value: " + val)
            opCodes.append(val)
        else:
            swank = x[3:len(x) - 1]
            # print("got here7")
            # print(swank)
            for _ in swank:
                val = swank
            print("this is hex literal value: " + val)
            opCodes.append(val)
    return val


def bitStr2Hex(bitstring):
    """ Recursively returns a hex representation of a bit string. """
    hexStr = "0123456789ABCDEF"
    if len(bitstring) == 0:
        return ""
    elif len(bitstring) >= 4:
        return bitStr2Hex(bitstring[:-4]) + hexStr[int(("0b" + bitstring[-4:]), 2)]
    else:
        return hexStr[int(("0b" + bitstring), 2)]


def oppositeBit(b):
    """ b is a single char, 0 or 1.  return the other. """
    if b == '1':
        return '0'
    else:
        return '1'


def bitStr2Comp(bitstring):
    """ compute and return the 2's complement of bitstring """

    bitList = list(bitstring)
    length = len(bitList)
    broke = 0
    for i in range(length):  # Not each bit
        bitList[i] = oppositeBit(bitList[i])
    for i in range(length):  # Add one to the flipped bit string
        if bitList[length - (i + 1)] == '0':
            bitList[length - (i + 1)] = '1'
            broke = 1
            break
        else:
            bitList[length - (i + 1)] = '0'

    if broke == 0:
        return '1' + "".join(bitList)  # Account for extra carry
    else:
        return "".join(bitList)


def toBitString(val, length=24):
    """Build and return a bit string of the given length.
       val is a signed integer"""

    bits = '{:b}'.format(val)  # Convert int to bit string

    if val < 0:
        bits = bitStr2Comp(bits[1:])

    if len(bits) < length:  # Add leading 0s or 1s
        if val >= 0:
            return '0' * (length - len(bits)) + bits
        else:
            return '1' * (length - len(bits)) + bits

    else:
        return bits


# test = toBitString(-266)
# testHex =  bitStr2Hex(test)
# print("TESTING FUNCTION")
# print(test)
# print(testHex)


def flagsCompute(instruction, operand, isBase):
    val = 0
    if instruction[0] == "+":
        val = val + 1
        if operand[len(operand) - 2:len(operand)] == ",X":  # else
            val = val + 8
    else:
        if operand[len(operand) - 2:len(operand)] == ",X":  # else
            val = val + 8
        if isBase is True:
            val = val + 4
        else:
            val = val + 2
    # print(val)
    return val


def niCompute(operand):
    if str(operand).startswith("#"):
        return 1
    elif str(operand).startswith("@"):
        return 2
    else:
        return 3


def findBase(mnemonics):
    if "BASE" in mnemonics:
        return True
    else:
        print("Address Error: No base found")
        return False


def pcRel(addr, PCaddr, baseAddr):
    temp2 = int(str(addr), 16)
    fuk = int(str(PCaddr), 16)
    temp3 = temp2 - fuk
    isBase = False
    # print(temp3)
    if temp3 >= -2047 and temp3 <= 2048:
        # print("got here2")
        addr = temp2 - fuk
        tup = [addr, isBase]
        return tup
    else:
        t = findBase(mnemonics)
        if t is True:
            isBase = True
            tup = [baseFunc(addr, baseAddr), isBase]
            return tup
        else:
            return


def baseFunc(addr, baseAddr):
    shit = int(str(addr), 16)
    pee = int(str(baseAddr), 16)
    temp = pee - shit
    if temp >= 0 and temp <= 4095:
        addr = pee - shit
        return addr
    else:
        print("Address error: out of range of PC Relative and Base Relative, object code not generated")
        return


def numReturn(args):
    gank = {
        0: "labels",
        1: "mnemonics",
        2: "operand",
        3: "comment"
    }

    return gank.get(args, "nothing")


# ----Pass 1----
def calcBytes(name, operand) -> int:
    length = 0
    numBytes = -1

    if name == "RESW" or name == "WORD" or name == "RESB" or name == "BYTE":
        if name == "RESW":
            operand = int(operand)
            numBytes = operand * 3
            return numBytes
        elif name == "WORD":
            numBytes = 3
            return numBytes
        elif name == "RESB":
            operand = int(operand)
            numBytes = operand
            return numBytes
        elif name == "BYTE":
            if operand[0] == '=':
                if operand[1] == 'X':
                    length = len(operand[3: len(operand) - 1])
                    if length % 2 == 0:
                        numBytes = length // 2
                        return numBytes
                    else:
                        print("Uneven hex literal, skipping")
                        # numBytes = (length / 2) + 1
                        return numBytes
                if operand[1] == 'C':
                    length = len(operand[3: len(operand) - 1])
                    numBytes = length
                    # TEST = operand[3: len(operand) - 1]
                    # print(TEST)
                    return numBytes
    if name == ["BASE", "START", "END", "LTORG"]:
        numBytes = 0
    else:
        numBytes = Mnemonics.get(name)[1]
    return numBytes


# print(calcBytes("BYTE", "=X'124'"))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("File not found")
        sys.exit(0)
    try:
        sicProgram = open(sys.argv[1], 'r')
    except IOError:
        print("File " + sys.argv[1] + " does not exist")
        sys.exit(0)
    index = 0
    labels = []
    operands = []
    mnemonics = []
    comments = []
    address = 0
    addArray = []
    printL = False
    baseAddr = 0
    for line in sicProgram:
        if line != "":
            labels.append(" ")
            operands.append(" ")
            mnemonics.append(" ")
            comments.append(" ")
            if not line.startswith("."):
                code = line.strip("\n").split(" ")
                z = 0
                team = 0
                for x in code:
                    if x != "":
                        if z < 3:
                            if z == 0:
                                if Mnemonics.get(code[team].strip()) is None and code[team].strip() not in DIRECTS:
                                    labels[index] = code[team].strip()
                                else:
                                    mnemonics[index] = code[team].strip()
                                    z = 1
                            elif z == 1:
                                if Mnemonics.get(code[team].strip()) is not None or code[team].strip() in DIRECTS:
                                    mnemonics[index] = code[team].strip()
                                else:

                                    # print("Error Invalid Mnemonic Ignoring Line")
                                    labels[index] = " "
                                    operands[index] = line.strip(" ").strip()
                                    mnemonics[index] = " "
                                    comments[index] = " "
                                    break
                            elif z == 2:
                                operands[index] = code[team].strip()
                        else:
                            comments[index] = code[team:]
                            break
                        z = z + 1
                    team = team + 1
            else:
                comments[index] = (line.strip("\n"))
            if mnemonics[index] == 'START':
                address = "0x" + operands[index]
                oldaddress = int(address, 16)
                address = oldaddress
                addArray.append(hex(address))
                # print(addArray[index])
            elif Mnemonics.get(mnemonics[index]) is not None:
                addArray.append(str(hex(address)))
                address = address + calcBytes(mnemonics[index], operands[index])
                # print(addArray[index])
            elif mnemonics[index] in DIRECTS:
                # print("HIw")
                addArray.append(hex(address))
                if mnemonics[index] == "LTORG":
                    printL = True
                    # address = address + calcBytes(mnemonics[index], operands[index])[1]
                elif mnemonics[index] == "RESW":
                    address = address + calcBytes("RESW", operands[index])
                elif mnemonics[index] == "WORD":
                    address = address + calcBytes("WORD", operands[index])
            else:
                addArray.append(hex(address))
            if operands[index].startswith("="):
                LITDIC.append(operands[index])

        # print(format(addArray[index].upper()[2:], "<"), format(labels[index], "<"), format(mnemonics[index], "<"), format(operands[index], "<"), " ".join(comments[index]))
        if printL:
            i = 0
            while i <= len(LITDIC) - 1:
                address = address + calcBytes("BYTE", LITDIC[i])
                labels.append(" ")
                mnemonics.append("BYTE")
                operands.append(LITDIC[i])
                comments.append(" ")
                # print(hex(address).upper()[2:], "   BYTES   ", LITDIC[i])
                addArray.append(hex(address))
                i = i + 1
                index = index + 1
            printL = False
        index = index + 1
    # print(" ")
    # print("Symbol Tables")
    # print("--------------------")
    # for x in range(len(addArray)):
    #   if labels[x] != "$":
    #        print(addArray[x].upper()[2:], labels[x])
    # ----Pass 2----
    opCodes = []

    lines = [(labels[i], mnemonics[i], operands[i], comments[i]) for i in range(len(labels))]
    daddyctr = 0
    for x in lines:
        opc = 0x00
        xbpe = 0x0
        addr = 0x000
        # print(x)
        cank, gank, wank, dank = x
        #print(addArray[daddyctr], cank, gank, wank, daddyctr)
        if "START" in gank:
            #print("JUST WENT THROW START")
            opCodes.append(hex(0xFFFFFF).upper()[2:])
        elif "RESW" in gank:
            opCodes.append(hex(0xFFFFFF).upper()[2:])
            # print(opCodes)
        elif "END" in gank:
            opCodes.append(hex(0xFFFFFF).upper()[2:])
        elif " " in gank:
            opCodes.append(" ")
            continue
            # print("I DO NOTHING")
        elif "BASE" in gank:
            ctr = 0
            test = wank.replace(",X", "").replace("#", "").replace("@", "").strip()
            for x in labels:
                if x == test:
                    baseAddr = addArray[ctr]
                ctr = ctr + 1
            # print(opCodes)
            opCodes.append(hex(0xFFFFFF).upper()[2:])
        elif "WORD" in gank:
            opCodes.append(hex(int(wank)).upper()[2:])
        elif "LTORG" in gank:
            # print("HERE")
            opCodes.append(hex(0xFFFFFF).upper()[2:])
        elif "BYTE" in gank:
            # print("got here1")
            litCode = litFunc(LITDIC)
            print("This is litCode: " + litCode)
            #opCodes.append(litCode.upper()[2:])
        else:
            opc = opc + niCompute(wank)
            if Mnemonics.get(gank) is not None:
                test = Mnemonics.get(gank)
                opc = opc + test[0]
            # print(hex(int(opc)).upper()[2:])
            if re.match(r'(([#@])?\d+)', gank):
                addr = addr + wank
            else:
                ctr = 0
                twank = wank.replace("#", "").replace("@", "").replace(",X", "").strip()
                for x in labels:
                    if x == twank:
                        addr = addArray[ctr]
                    ctr = ctr + 1
                if daddyctr <= (len(addArray) - 2):

                    addr = pcRel(addr, addArray[daddyctr + 1], baseAddr)
                    trueaddr = addr[0]
                    isBase = addr[1]
                    xbpe = flagsCompute(gank, wank, isBase)
                else:
                    addr = pcRel(addr, addArray[daddyctr], baseAddr)
                    trueaddr = addr[0]
                    isBase = addr[1]
                    xbpe = flagsCompute(gank, wank, isBase)
                # print("yuh" , trueaddr)
                # print("yuh " , xbpe)
                #print("OPCODE PARTS")
                #print(hex(opc))

                #print(trueaddr)
                #print(xbpe)

                if trueaddr != None:
                    #print("here")
                    if trueaddr < 0:
                        temp = toBitString(trueaddr)
                        trueaddr = bitStr2Hex(temp)
                    elif len(str(trueaddr)) > 3:
                        temp = trueaddr
                        trueaddr = temp[len(temp) - 3:len(temp)]
                    elif len(str(trueaddr)) < 3:
                        while len(str(trueaddr)) != 3:
                            trueaddr = "0" + str(trueaddr)
                    if len(str(opc)) < 2:
                        str(opc).zfill(6)
                    # opc = hex(int(opc))[2:]
                    # trueaddr = hex(trueaddr)[2:]

                    xbpe = hex(xbpe)[2:]
                    if xbpe == 1 | 9:
                        OPCODE = hex(int(str(opc))) + str(xbpe) + str(trueaddr[len(trueaddr) - 1:len(trueaddr)])
                        break
                    OPCODE = hex(int(str(opc))) + str(xbpe) + str(trueaddr[len(trueaddr) - 3:len(trueaddr)])
                    #print(OPCODE.upper().replace("X", ""))
                    # if len(OPCODE) != 6:
                    # \   opCodes.append(OPCODE.upper().replace("X", ""))[1:]
                    # else:
                    opCodes.append(OPCODE.upper().replace("X", ""))

                    # genLST(operands, mnemonics, labels, comments, addArray, opCodes)

                else:
                    print("NO object code generated")
                    break

        daddyctr = daddyctr + 1
    # for i in range(0, len(addArray)):
    #   lst.writelines(addArray[i][2:])
    #  lst.writelines(" ")
    # lst.writelines(opCodes[i])
    # lst.writelines(" ")
    # lst.writelines(labels[i])
    # lst.writelines(" ")
    # lst.writelines(mnemonics[i])
    # lst.writelines(" ")
    # lst.writelines(operands[i])
    # lst.writelines(" ")
    # lst.writelines(comments[i])
    # lst.write("\n")
    sicProgram.close()
    #print(sys.path)
    for i in range(0, len(addArray)):
        lst.write(str(addArray[i].upper()[2:]))
        lst.write(" ")
        lst.write(str(opCodes[i]).zfill(6))
        lst.write(" ")
        lst.write(str(labels[i]))
        lst.write(" ")
        lst.write(str(mnemonics[i]))
        lst.write(" ")
        lst.write(str(operands[i]))
        lst.write(" ")
        lst.write(str(comments[i]))
        lst.write("\n")

    lst.close()
    obj.write(addArray[1].zfill(6).upper()[2:])
    obj.write("\n")
    obj.write(str(0).zfill(6))
    obj.write("\n")
    for i in range(0, len(mnemonics)):
        if mnemonics[i] in DIRECTS:
            obj.write("\n")
            obj.write("!")
            obj.write("\n")
            obj.write(addArray[i].upper()[2:].zfill(6))
            obj.write("\n")
            obj.write(str(0).zfill(6))
        elif mnemonics[i] is "END":
            obj.write("!")
            sys.exit(0)
        obj.write("\n")
        obj.write(opCodes[i].zfill(6))
    obj.write("\n")
    obj.write("!")