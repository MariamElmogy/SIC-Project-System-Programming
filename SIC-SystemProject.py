'''
    Name:   Mariam Mohamed Elmogy
    Reg#:   19101076
'''
import collections
import re
import converter

labels_list = []
instruction_list = []
reference_list = []
LocCtr = []
Obj_Code = []

i = 0
######################################################################################

file = open("inSIC.txt", "r")  # Open For Read The File

#   Read File
with file:
    for line in file:   # Loop To Read The Line
        lines_split = re.split('\s+', line)
        lines = collections.deque(lines_split)  # To Help Rotate The Last Line

        if "end".lower() == "END".lower():  # if in line found end add # and rotate
            lines.append("######")   # Replace "End" With "#"
            lines.rotate(-5)    # Rotate The Last Line To Put The # In The Label List

        if line.startswith('\t'):   # If There Is A Space Then Add "#"
            labels_list.append("######")    # Add #'s in labels_list

        else:
            labels_list.append(lines[i])    # Read The Lines And Add It In Labels
        instruction_list.append(lines[i + 1])
        reference_list.append(lines[i + 2])
file.close()
######################################################################################


#   Pass 1
for i in range(2):
        LocCtr.append(reference_list[0])   # Here I Add At Index 0 and 1 Of LocCtr The Value Of The Reference Of Index 0

for i in range(1, len(labels_list)):    # Start To Loop From 1
    StrLocation = LocCtr[i]
    location_counter = int(StrLocation, 16)     # To Convert The Location Counter Values To Hex
    if instruction_list[i].upper() != 'End'.upper():   # If It's not equal to end

        if instruction_list[i].upper() == 'RESW'.upper():  # If found RESW
            LocCtr.append(format((int(reference_list[i]) * 3)+location_counter, 'X'))

        elif instruction_list[i].upper() == 'RESB'.upper():  # If found RESB
            LocCtr.append(format((int(reference_list[i]) * 1)+location_counter, 'X'))

        elif instruction_list[i].upper() == 'BYTE'.upper():   # If found BYTE
            if reference_list[i].startswith('C'.lower()) or reference_list[i].startswith('C'.upper()):  # First Option It Contains C
                LocCtr.append(format((len(reference_list[i]) - 3) + location_counter, 'X'))
            elif reference_list[i].upper().startswith('X'.upper()):    # Second Option It Contains X
                LocCtr.append(format(int((len(reference_list[i]) - 3)/2) + location_counter, 'X'))

        else:
            LocCtr.append(format(location_counter + 3, 'X'))    # Increment +3

######################################################################################


#   Pass 2
for i in range(len(instruction_list)):     # To Get The Object Code
    # If Not Found End Then Start The If Condition
    if instruction_list[i].upper() != 'End'.upper():
        # If Found RESW or RESB or Start Then Add empty value in Object Code cuz it has no object code
        if instruction_list[i].upper() == 'RESW'.upper() or instruction_list[i].upper() =='RESB'.upper() or instruction_list[i].upper() == 'Start'.upper():
            Obj_Code.append("\t")
        elif instruction_list[i].upper() == 'Word'.upper():
            reference = int(reference_list[i], 10)
            Obj_Code.append(format(reference, '06x'))

        # If Found BYTE There Is 2 Options:
        elif instruction_list[i].upper() == 'BYTE'.upper():

            # First If C Then Check The Value In ASCII Code Then Convert It To Hex
            if reference_list[i].upper().startswith('C'.upper()):
                refSplit = reference_list[i].split('C')
                refSplit.remove('')
                NewrefSplit = refSplit[0].replace("'", "")
                ASCII_values = [ord(character) for character in NewrefSplit]
                for i in range(len(NewrefSplit)):
                    ASCII_values.append(format(ASCII_values[i], 'X'))
                listToStr = ' '.join([str(elem) for elem in ASCII_values])
                Obj_Code.append(listToStr[8:])

            # Second Add The Value As It Is
            elif reference_list[i].upper().startswith('X'.upper()):
                refSplit = reference_list[i].split('X')
                refSplit.remove('')
                NewrefSplit = refSplit[0].replace("'", "")
                Obj_Code.append(NewrefSplit)

        else:
            for k in range(len(converter.OPTAB)):  # To Loop For All Elements
                if instruction_list[i] == converter.OPTAB[k][0]:  # To search if the instruction is available in OPTAB
                    # If Found RSUB Search For The OPCODE Of RSUB And Then Add four 0's
                    if instruction_list[i].upper().startswith('RSUB'.upper()):
                        Obj_Code.append(converter.OPTAB[k][2] + "0000")
                        break

                    # If It includes ,X (x = 1) then convert it to binary
                    # Add 1
                    # Convert To Hex
                    for y in range(len(labels_list)):
                        if reference_list[i].upper().endswith(',X'.upper()):
                            ref = []
                            ref = str(reference_list[i]).split(',')
                            if ref[0] == labels_list[y]:
                                ConvBin = LocCtr[y]
                                b = int(ConvBin, 16)
                                convert_binary = format(b, "015b")
                                x = 1
                                conv_hex = format(x, "b") + convert_binary
                                binary_string = conv_hex
                                decimal_representation = int(binary_string, 2)
                                hexadecimal_string = format(decimal_representation, 'X')
                                Obj_Code.append(converter.OPTAB[k][2] + hexadecimal_string)
                                break
                        elif reference_list[i].upper() in labels_list[y].upper():
                            Obj_Code.append(converter.OPTAB[k][2] + LocCtr[y])
                            break
                        else:
                            continue
                    break

    else:
        Obj_Code.append("\t")
        break

######################################################################################


# To Print As Columns And Rows
for i in range(len(Obj_Code)):
    if instruction_list[i] == "RSUB".upper() or instruction_list[i] == "RSUB".lower():
        reference_list[i] = "######"
    if instruction_list[i].startswith("Start".upper()) or instruction_list[i].startswith("Start".lower()):
        print(LocCtr[i], '|', labels_list[i], "\t|", instruction_list[i], "|", reference_list[i], "\t\t|", Obj_Code[i])
    elif len(labels_list[i]) <= 3:
        print(LocCtr[i], '|', labels_list[i], "\t\t|", instruction_list[i], "|", reference_list[i], "\t|", Obj_Code[i])
    elif len(reference_list[i]) == 4:
        print(LocCtr[i], '|', labels_list[i], "\t|", instruction_list[i], "|", reference_list[i], "\t\t|", Obj_Code[i])
    elif len(reference_list[i]) == 1:
        print(LocCtr[i], '|', labels_list[i], "\t|", instruction_list[i], "|", reference_list[i], "\t\t\t|", Obj_Code[i])
    else:
        print(LocCtr[i], '|', labels_list[i], "\t|", instruction_list[i], "\t|", reference_list[i], "\t|", Obj_Code[i])


######################################################################################


# Create A Symbol Table
symbol_table = open("symbolTable.txt", "w+")
for i in range(len(labels_list)):
    if labels_list[i].startswith("#"):
        pass
    else:
        symbol_table.write("%s | \t%s\n" % (LocCtr[i], labels_list[i]))


######################################################################################


# Create HTE
Header = []
T_record = []
End = []

#   H
for i in range(len(labels_list)):
    location_counter = []
    StrLocation = LocCtr[0]     # Start Location
    location_counter.append(int(StrLocation, 16))   # Add it in location_counter
    StrLocation = LocCtr[i]     # End
    location_counter.append(int(StrLocation, 16))   # Add it in location_counter
    # location_counter = [LocCtr[0], LocCtr[i]]
    # Get Length = End - Start
    length = location_counter[1] - location_counter[0]
# Add It To Header
Header.append((labels_list[0] + str(0) + str(0) + LocCtr[0] + format(length, '06x')))
print("-------------------------------------------\n")
print("H --> ", Header[0])


######################################################################################

#   T Record

i = 1
while i < (len(Obj_Code)):
    startAddr = LocCtr[i]   # Create a startAdd to keep all the start address that I will need in T record
    # I have 2 counter cnt & c
    cnt = 0     # To Get The T Record Length
    c = 0       # To Get The Object Codes

    if Obj_Code[i] != '\t':     # If The Object not equals \t
        T_record.append("00"+startAddr)     # Add The Start Address In The T Record
        j = i
        k = j

        while j < len(Obj_Code) and cnt < 10:
            if Obj_Code[j] == '\t':
                break
            else:
                j += 1
                cnt += 1

        length_record = str(hex(int(LocCtr[j], 16) - int(startAddr, 16))).upper()[2:4]  # To Get The Length Of T Record
        i = j - 1

        if len(length_record) == 1:
            length_record = "0" + length_record

        T_record.append(length_record)

        while k < len(Obj_Code) and c < 10:
            if Obj_Code[k] == '\t':
                break

            else:
                T_record.append(Obj_Code[k])
                k += 1
                c += 1

        print("T --> ", T_record)   # Print T Record
        del(T_record[:j+1])

    i += 1


######################################################################################

#   End
End.append(str(0) + str(0) + LocCtr[0])
print("E --> ", End[0])

