import os
import sys
import time

debug = False

# v - variable - vInput
# s - string - "2"
# i - int - 2
# f - float - 2.0
# b - bool - True False
## l - list - []
## d - dict - {}
## f - function - call()
## b - branch - if else
## g - gate - or and

os.system("cls")
os.system("title Assumption Interpreter")
os.system("color 0F")

class bcolors:
    Reset = "\u001b[0m"
    Black = "\u001b[30m"
    Red = "\u001b[31m"
    Green = "\u001b[32m"
    Yellow = "\u001b[33m"
    Blue = "\u001b[34m"
    Magenta = "\u001b[35m"
    Cyan = "\u001b[36m"
    White = "\u001b[37m"
    BBlack = "\u001b[30;1m"
    BRed = "\u001b[31;1m"
    BGreen = "\u001b[32;1m"
    BYellow = "\u001b[33;1m"
    BBlue = "\u001b[34;1m"
    BMageneta = "\u001b[35;1m"
    BCyan = "\u001b[36;1m"
    BWhite = "\u001b[37;1m"
    BackBlack = "\u001b[40m"
    BackRed = "\u001b[41m"
    BackGreen = "\u001b[42m"
    BackYellow = "\u001b[43m"
    BackBlue = "\u001b[44m"
    BackMagenta = "\u001b[45m"
    BackCyan = "\u001b[46m"
    BackWhite = "\u001b[47m"
    BackBBlack = "\u001b[40;1m"
    BackBRed = "\u001b[41;1m"
    BackBGreen = "\u001b[42;1m"
    BackBYellow = "\u001b[43;1m"
    BackBBlue = "\u001b[44;1m"
    BackBMageneta = "\u001b[45;1m"
    BackBCyan = "\u001b[46;1m"
    BackBWhite = "\u001b[47;1m"
    Bold = "\u001b[1m"
    Underline = "\u001b[4m"
    Reversed = "\u001b[7m"

def stringtocontent(x):
    characternum = 0
    new = ""
    ignore = False
    for character in x:
        characternum += 1
        if character == "n" and ignore:
            new += "\n"
        elif character == "t" and ignore:
            new += "\n"
        elif character == "l" and ignore:
            new += "\x00"
        elif character == "\\" and ignore:
            new += "\\"
        if ignore == True:
            ignore = False
            continue
        if character == "\n":
            continue
        elif character == "\\":
            ignore = True
        elif characternum > 1 and characternum < len(x):
            new += character
    return new

def isnumber(x):
    if str(x).find("-") != -1 and str(x).find("-") != 0:
        return False
    isnumber = True
    points = 0
    for character in str(x):
        if character == "\n":
            continue
        for number in "-1234567890.":
            if character == number:
                if character == ".":
                    points += 1
                    if points >= 2:
                        return False
                break
            elif number == ".":
                isnumber = False
            else:
                continue
    return isnumber

def showvars():
    print(bcolors.BackBBlack+bcolors.Blue+"Variables = "+str(variables)+"\nWaitfor = "+str(waitfor)+bcolors.Reset)

def showlines():
    print(bcolors.BackBBlack+bcolors.Blue+str(everyline)+bcolors.Reset)

try:
    openedfp = sys.argv[1]
except IndexError:
    openedfp = "UNKNOWN"

if "-d" in sys.argv or "--debug" in sys.argv:
    debug = True

loopfile = True
if not ("-l" in sys.argv or "--loop" in sys.argv):
    loopfile = False

onefile = False
if openedfp.endswith(".ass"):
    onefile = True

print(bcolors.BackBBlack+bcolors.Magenta + ">>> Running from "+str(os.path.dirname(__file__))+bcolors.Reset)

looping = True
while looping:
    looping = loopfile
    if onefile:
        command = openedfp
    else:
        command = input(bcolors.BackBBlack+bcolors.Yellow+">>> What file do you want to interpret?\n"+bcolors.Cyan+"> "+bcolors.Reset)
    if command.startswith("%cd%"):
        filepath = os.path.dirname(__file__)
        characternum = 0
        for character in command:
            characternum += 1
            if characternum > 4:
                filepath += character
        if not filepath.endswith(".ass"):
            filepath += ".ass"
    elif command == "same" or command == "last":
        pass
    elif command == "d" or command == "debug":
        debug = not debug
        continue
    elif command == "":
        break
    elif command == "vars":
        showvars()
        continue
    elif command == "everyline":
        showlines()
        continue
    else:
        filepath = command
    print(bcolors.BackBBlack+bcolors.Yellow+">>> File path: " + filepath + "\n\n"+bcolors.Green+">>> Interpreting file..."+bcolors.Reset)
    if filepath.endswith(".ass"):
        os.system("title Assumption Interpreter - " + filepath)
        try:
            with open(filepath) as fp:
                ####################################################################################################################
                #leave = False
                waitfor = ""
                variables = {}
                #while not leave:
                everyline = []
                currentline = ""
                commented = False
                for character in fp.read():
                    if character == "\n":
                        while currentline.endswith(" "):
                            currentline = currentline[:len(currentline)]
                        everyline.append(currentline)
                        currentline = ""
                        commented = False
                    elif character == "#":
                        commented = True
                    elif not commented and character != "\t":
                        currentline += character
                if currentline != "":
                    everyline.append(currentline)
                    currentline = ""
                error = False
                linenum = -1
                while linenum < len(everyline):
                    if error:
                        # CLOSE PROGRAM ON ERROR
                        break
                    else:
                        if linenum + 1 >= len(everyline):
                            if waitfor == "":
                                #leave = True
                                linenum += 1
                            else:
                                linenum = 0
                        else:
                            linenum += 1
                    try:
                        line = everyline[linenum]
                    except IndexError:
                        break
                    if waitfor == "" or (waitfor != "" and waitfor == everyline[linenum]):
                        if debug and waitfor != "":
                                print(bcolors.BackBBlack+bcolors.Blue+">>> Found line:\n["+waitfor+"]"+bcolors.Reset)
                        waitfor = ""
                        if "vInput" in line:
                            invar = input(bcolors.BackBBlack+bcolors.Cyan+"> "+bcolors.Reset)
                            invar2 = ""
                            for character in invar:
                                if character != "\n" and character != "\t":
                                    invar2 += character
                            newinput = ("\""+invar2+"\"")
                            line = (line[:line.find("vInput")]+newinput+line[line.find("vInput")+8:])
                        #print(line)
                        #everyline[linenum-1] = line
                        if line == "\n" or line == "":
                            continue
                        elif not line.startswith("assume"):
                            # ASSUME MISSING ERROR
                            print(bcolors.BackBBlack+bcolors.Red+">>> ERROR: COMMAND MISSING ON LINE #"+str(linenum)+bcolors.Reset)
                            break
                        elif line.startswith("assume item "):
                            # SLICE
                            # assume
                            # item
                            num = ""
                            # from
                            full = ""
                            # as
                            part = ""
                            # assume item 4 from "hello" as sHello
                            inside = False
                            quote = ""
                            ignore = False
                            characternum = -1
                            for character in line[line.find("item "):line.find(" from")]:
                                characternum += 1
                                if characternum >= 5:
                                    if character != " ":
                                        num += character
                            if debug:
                                print(bcolors.BackBBlack+bcolors.Blue+"ARG1 = "+str(num)+bcolors.Reset)
                            characternum = -1
                            for character in line[line.find("from "):line.find(" as")]:
                                characternum += 1
                                if characternum >= 5:
                                    if character == quote and not ignore:
                                        inside = False
                                        full += character
                                    ignore = False

                                    if character == "\\":
                                        if ignore == False:
                                            ignore = True
                                        full += character
                                    elif quote == "" and (character == "\"" or character == "'"):
                                        inside = True
                                        quote = character
                                        full += character
                                    elif character != " " or (character == " " and inside == True):
                                        full += character
                            if debug:
                                print(bcolors.BackBBlack+bcolors.Blue+"ARG2 = "+str(full)+bcolors.Reset)
                            characternum = -1
                            for character in line[line.find("as "):]:
                                characternum += 1
                                if characternum >= 3:
                                    if character != " ":
                                        part += character
                            if debug:
                                print(bcolors.BackBBlack+bcolors.Blue+"ARG3 = "+str(part)+bcolors.Reset)
                            if isnumber(num):
                                num = int(num)
                            else:
                                try:
                                    num = int(variables[num])
                                except ValueError:
                                    print(bcolors.BackBBlack+bcolors.Red+">>> ERROR: ARGUMENT #1 MUST BE A NUMBER ON LINE #"+str(linenum)+bcolors.Reset)
                            if (full.endswith("\"") and full.startswith("\"")) or (full.endswith("'") and full.startswith("'")):
                                full = stringtocontent(full)
                            elif "\"" in full or "'" in full:
                                print(bcolors.BackBBlack+bcolors.Red+">>> ERROR: ARGUMENT #2 MISSING QUOTE ON LINE #"+str(linenum)+bcolors.Reset)
                            elif isnumber(full):
                                if "." in full:
                                    full = float(full)
                                else:
                                    full = int(full)
                            else:
                                full = variables[full]
                            try:
                                variables[part] = full[num]
                            except KeyError:
                                print(bcolors.BackBBlack+bcolors.Red+">>> ERROR: ARGUMENT #1 MUST BE A NUMBER ON LINE #"+str(linenum)+bcolors.Reset)
                        elif "+" in line:
                            # ADDITION/CONCATENATION
                            arg1 = ""
                            arg2 = ""
                            before = True
                            characternum = 0
                            inside = False
                            ignore = False
                            quote = ""
                            for character in line:
                                characternum += 1
                                if characternum > 7:
                                    if character == quote and ignore == False:
                                        inside = False
                                    ignore = False
                                    if character == "+":
                                        quote = ""
                                        before = False
                                        if arg1 == "":
                                            print(bcolors.BackBBlack+bcolors.Red+">>> ERROR: ARGUMENT #1 TO ADD/CONCATENATE MISSING ON LINE #"+str(linenum)+bcolors.Reset)
                                            error = True
                                            break
                                    elif quote == "" and (character == "'" or character == "\""):
                                        quote = character
                                        inside = True
                                        if before:
                                            arg1 += character
                                        else:
                                            arg2 += character
                                    elif inside or (character != " " and character != "\t"):
                                        if before:
                                            arg1 += character
                                        else:
                                            arg2 += character
                            if arg2.endswith("\n"):
                                    arg2 = arg2[:-1]
                            if arg2 == "":
                                print(bcolors.BackBBlack+bcolors.Red+">>> ERROR: ARGUMENT #2 TO ADD/CONCATENATE MISSING ON LINE #"+str(linenum)+bcolors.Reset)
                                break
                            if (arg1.endswith("\"") and arg1.startswith("\"")) or (arg1.endswith("'") and arg1.startswith("'")):
                                # ARG 1 = STRING RAW
                                arg1 = stringtocontent(arg1)
                                if (arg2.endswith("\"") and arg2.startswith("\"")) or (arg2.endswith("'") and arg2.startswith("'")):
                                    # ARG 2 = STRING RAW
                                    arg2 = stringtocontent(arg2)
                                elif "'" in arg2 or "\"" in arg2:
                                    # ARG 2 STRING ERROR
                                    print(bcolors.BackBBlack+bcolors.Red+">>> ERROR: STRING MISSING QUOTE ON LINE #"+str(linenum)+bcolors.Reset)
                                    break
                                else:
                                    if isnumber(arg2):
                                        # ARG 2 = INT/FLOAT RAW
                                        arg2 = str(arg2)
                                    else:
                                        arg2 = str(variables[arg2])
                                print(arg1 + arg2)
                            elif "'" in arg1 or "\"" in arg1:
                                # ARG 1 = STRING ERROR
                                print(bcolors.BackBBlack+bcolors.Red+">>> ERROR: STRING MISSING QUOTE ON LINE #"+str(linenum)+bcolors.Reset)
                                break
                            elif isnumber(arg1) and not "." in str(arg1):
                                # ARG 1 - INT RAW
                                time.sleep(int(arg1)-1)
                            elif isnumber(arg1) and "." in str(arg1):
                                # ARG 1 - FLOAT RAW
                                time.sleep(float(arg1))
                            elif arg1.startswith("s"):
                                # ARG 1 = STRING VAR
                                if (arg2.endswith("\"") and arg2.startswith("\"")) or (arg2.endswith("'") and arg2.startswith("'")):
                                    # ARG 2 = STRING RAW
                                    variables[arg1] += stringtocontent(arg2)
                                elif "'" in arg2 or "\"" in arg2:
                                    # ARG 2 STRING ERROR
                                    print(bcolors.BackBBlack+bcolors.Red+">>> ERROR: STRING MISSING QUOTE ON LINE #"+str(linenum)+bcolors.Reset)
                                    break
                                else:
                                    if isnumber(arg2):
                                        # ARG 2 = INT/FLOAT RAW
                                        variables[arg1] += str(arg2)
                                    else:
                                        variables[arg1] += str(variables[arg2])
                            elif arg1.startswith("i"):
                                # ARG 1 - INT VAR
                                if isnumber(arg2) and not "." in str(arg2):
                                    variables[arg1] += int(arg2)
                                elif arg2.startswith("i"):
                                    variables[arg1] += variables[arg2]
                                else:
                                    print(bcolors.BackBBlack+bcolors.Red+">>> ERROR: CAN'T ADD ARG2 TO INTEGER OF ARG1 ON LINE #"+str(linenum)+bcolors.Reset)
                                    break
                            if debug:
                                print(bcolors.BackBBlack+bcolors.Blue+">>> ARG1 of line #"+str(linenum)+" is "+str(arg1)+bcolors.Reset)
                                print(bcolors.BackBBlack+bcolors.Blue+">>> ARG2 of line #"+str(linenum)+" is "+str(arg2)+bcolors.Reset)
                        elif "-->" in line:
                            # CONVERT
                            characternum = 0
                            before = True
                            old = ""
                            new = ""
                            for character in line:
                                characternum += 1
                                if characternum > 7:
                                    if character == "\t" or character == " " or character == "-" or character == ">":
                                        if old == "":
                                            print(bcolors.BackBBlack+bcolors.Red+">>> ERROR: MISSING ARGUMENT #1 IN CONVERSION ON LINE #"+str(linenum)+bcolors.Reset)
                                            error = True
                                            break
                                        before = False
                                    elif before:
                                        old += character
                                    else:
                                        new += character
                            if new == "":
                                print(bcolors.BackBBlack+bcolors.Red+">>> ERROR: MISSING ARGUMENT #2 ON LINE #"+str(linenum)+bcolors.Reset)
                                break
                            else:
                                try:
                                    old = variables[old]
                                    if new.startswith("s"):
                                        variables[new] = str(old)
                                    elif new.startswith("i"):
                                        if isnumber(old):
                                            variables[new] = int(old)
                                        else:
                                            variables[new] = 0
                                            for character in old:
                                                variables[new] += ord(character)
                                    elif new.startswith("f"):
                                        variables[new] = float(old)
                                    elif new.startswith("b"):
                                        variables[new] = bool(old)
                                    else:
                                        print(bcolors.BackBBlack+bcolors.Red+">>> ERROR: UNKNOWN TYPE ON LINE #"+str(linenum)+bcolors.Reset)
                                        break
                                except ValueError:
                                    print(bcolors.BackBBlack+bcolors.Red+">>> ERROR: INVALID CONVERSION ON LINE #"+str(linenum)+bcolors.Reset)
                                    break
                        elif "==" in line:
                            # BRANCHES
                            section = "prefix"
                            characternum = 0
                            inside = False
                            quotes = ""
                            arg1 = ""
                            arg2 = ""
                            branch = ""
                            for character in line:
                                characternum += 1
                                if character == "\n":
                                    continue
                                elif section == "prefix":
                                    if characternum > 6:
                                        section = "arg1"
                                elif section == "arg1":
                                    if character == "=":
                                        if arg1 == "":
                                            print(bcolors.BackBBlack+bcolors.Red+">>> ERROR: ARGUMENT #1 MISSING ON LINE #"+str(linenum)+bcolors.Reset)
                                            error = True
                                            break
                                        else:
                                            section = "arg2"
                                    elif quotes == "" and (character == "'" or character == "\""):
                                        quotes = character
                                        inside = True
                                        arg1 += character
                                    elif character == quotes:
                                        inside = False
                                        arg1 += character
                                    elif inside or (character != " " and character != "\t"):
                                        arg1 += character
                                elif section == "arg2":
                                    if character == "=":
                                        continue
                                    elif character == ",":
                                        if arg2 == "":
                                            print(bcolors.BackBBlack+bcolors.Red+">>> ERROR: ARGUMENT #2 MISSING ON LINE #"+str(linenum)+bcolors.Reset)
                                            error = True
                                            break
                                        else:
                                            section = "branch"
                                    elif quotes == "" and (character == "'" or character == "\""):
                                        quotes = character
                                        inside = True
                                        arg2 += character
                                    elif character == quotes:
                                        inside = False
                                        arg2 += character
                                    elif inside or (character != " " and character != "\t"):
                                        arg2 += character
                                elif section == "branch":
                                    if character == " " or character == "\t":
                                        print(bcolors.BackBBlack+bcolors.Red+">>> ERROR: UNEXPECTED SPACE ON LINE #"+str(linenum)+bcolors.Reset)
                                        error = True
                                        break
                                    elif character == "\n":
                                        if branch == "":
                                            print(bcolors.BackBBlack+bcolors.Red+">>> ERROR: BRANCH MISSING ON LINE #"+str(linenum)+bcolors.Reset)
                                            error = True
                                        break
                                    else:
                                        branch += character
                                        if characternum == len(line):
                                            break
                            impossible = False
                            if (arg1.endswith("\"") and arg1.startswith("\"")) or (arg1.endswith("'") and arg1.startswith("'")):
                                # ARG 1 - STRING RAW
                                arg1 = stringtocontent(arg1)
                                if (arg2.endswith("\"") and arg2.startswith("\"")) or (arg2.endswith("'") and arg2.startswith("'")):
                                    # ARG 2 - STRING RAW
                                    arg2 = stringtocontent(arg2)
                                elif arg2.startswith("s"):
                                    # ARG 2 - STRING VAR
                                    arg2 = variables[arg2]
                                else:
                                    # ARG 2 - NOT STRING RAW
                                    impossible = True
                            elif "'" in arg1 or "\"" in arg1:
                                print(bcolors.BackBBlack+bcolors.Red+">>> ERROR: STRING MISSING QUOTE ON LINE #"+str(linenum)+bcolors.Reset)
                                error = True
                                break
                            elif isnumber(arg1):
                                if "." in arg1:
                                    # ARG 1 - FLOAT
                                    arg1 = float(arg1)
                                    if isnumber(arg2) and "." in arg2:
                                        # ARG 2 - FLOAT RAW
                                        arg2 = float(arg2)
                                    elif arg2.startswith("f"):
                                        # ARG 2 - FLOAT VAR
                                        arg2 = variables[arg2]
                                    else:
                                        # ARG 2 - NOT FLOAT
                                        impossible = True
                                else:
                                    # ARG 1 - INT
                                    arg1 = int(arg1)
                                    if isnumber(arg2) and not "." in str(arg2):
                                        # ARG 2 - INT
                                        arg2 = int(arg2)
                                    elif arg2.startswith("i"):
                                        arg2 = variables[arg2]
                                    else:
                                        # ARG 2 - NOT INT
                                        impossible = True
                            else:
                                if arg1.startswith("s"):
                                    # ARG 1 - STRING VAR
                                    if (arg2.endswith("\"") and arg2.startswith("\"")) or (arg2.endswith("'") and arg2.startswith("'")):
                                        # ARG 2 - STRING RAW
                                        arg2 = stringtocontent(arg2)
                                    elif "'" in arg2 or "\"" in arg2:
                                        # ARG 2 - STRING ERROR
                                        print(bcolors.BackBBlack+bcolors.Red+">>> ERROR: STRING MISSING QUOTE ON LINE #"+str(linenum)+bcolors.Reset)
                                        break
                                    else:
                                        if arg2.startswith("s") or arg2.startswith("i") or arg2.startswith("f"):
                                            # ARG 2 - STRING VAR
                                            arg2 = str(variables[arg2])
                                        else:
                                            # ARG 2 - NOT STRING
                                            impossible = True
                                elif arg1.startswith("b"):
                                    # ARG 1 - BOOL VAR
                                    if arg2.startswith("b"):
                                        arg2 = variables[arg2]
                                    elif arg2 == "True":
                                        arg2 = True
                                    elif arg2 == "False":
                                        arg2 = False
                                    else:
                                        impossible = True
                                elif arg1.startswith("i"):
                                    # ARG 1 - INT VAR
                                    if arg2.startswith("i"):
                                        arg2 = variables[arg2]
                                    if isnumber(arg2) and not "." in str(arg2):
                                        arg2 = int(arg2)
                                    else:
                                        impossible = True
                                elif arg1.startswith("f"):
                                    # ARG 1 - FLOAT VAR
                                    if arg2.startswith("f"):
                                        arg2 = variables[arg2]
                                    if isnumber(arg2) and "." in arg2:
                                        arg2 = float(arg2)
                                    else:
                                        impossible = True
                                arg1 = variables[arg1]
                            if (not impossible) and arg1 == arg2:
                                waitfor = ("assume " + branch)
                                if debug:
                                    print(bcolors.BackBBlack+bcolors.Blue+">>> Waiting for "+str(waitfor)+" because "+str(arg1)+" and "+str(arg2)+" are equal."+bcolors.Reset)
                            else:
                                waitfor = ""
                                if debug:
                                    print(bcolors.BackBBlack+bcolors.Blue+">>> Not waiting for anything because "+str(arg1)+" and "+str(arg2)+" aren't equal."+bcolors.Reset)
                        elif "=" in line and not "==" in line:
                            # SETTING VARIABLES
                            before = True
                            characternum = 0
                            variablename = ""
                            value = ""
                            quotecount = 0
                            quotetype = ""
                            inside = False
                            ignore = False
                            for character in line:
                                characternum += 1
                                if character == "\n" or character == "\t":
                                    continue
                                elif character == "\\":
                                    ignore = True
                                    continue
                                elif ignore == False and (character == quotetype or (quotetype == "" and (character == "\"" or character == "'"))):
                                    quotetype = character
                                    quotecount += 1
                                    if quotecount == 1:
                                        inside = True
                                    else:
                                        inside = False
                                    continue
                                ignore = False
                                if character == "=":
                                    before = False
                                    if variablename == "":
                                        print(bcolors.BackBBlack+bcolors.Red+">>> ERROR: VARIABLE TO SET MISSING ON LINE #"+str(linenum)+bcolors.Reset)
                                        error = True
                                        break
                                elif characternum > 7 and character != " " and character != "\t" and before == True:
                                    variablename += character
                                elif ((character != " " and character != "\t") or inside) and before == False:
                                    value += character
                            if value == "" and not variablename.startswith("s"):
                                print(bcolors.BackBBlack+bcolors.Red+">>> ERROR: VALUE TO SET VARIABLE TO MISSING ON LINE #"+str(linenum)+bcolors.Reset)
                                break
                            elif variablename.startswith("i"):
                                if isnumber(value) and not "." in value:
                                    value = int(value)
                                else:
                                    value = int(variables[value])
                            elif variablename.startswith("f"):
                                if isnumber(value) and "." in value:
                                    value = float(value)
                                else:
                                    value = float(variable[value])
                            elif variablename.startswith("b"):
                                if value == "True" or value == "False":
                                    value = bool(value)
                                else:
                                    value = bool(variable[value])
                            elif variablename.startswith("s"):
                                if (value.startswith("s") or value.startswith("i") or value.startswith("f") or value.startswith("b")) and quotecount == 0:
                                    value = str(variables[value])
                                elif quotecount != 2:
                                    print(bcolors.BackBBlack+bcolors.Red+">>> ERROR: VARIABLE SAYS VALUE IS A STRING, BUT IT'S NOT A STRING AT LINE #"+str(linenum)+bcolors.Reset)
                                    break
                            elif not variablename.startswith("l") and not variablename.startswith("d"):
                                print(bcolors.BackBBlack+bcolors.Red+">>> ERROR: TYPE OF VARIABLE UNKNOWN ON LINE #"+str(linenum)+bcolors.Reset)
                                break
                            variables[variablename] = value
                        elif line.startswith("assume '") or line.startswith("assume \""):
                            # PRINT STRING RAW
                            inside = False
                            result = ""
                            first = ""
                            ignore = -10
                            characternum = 0
                            for character in line:
                                characternum += 1
                                if (characternum-ignore) >= 1 and character == first:
                                    break
                                if character == "\\":
                                    ignore = characternum
                                elif character == "n" and (characternum-ignore) <= 1:
                                    result += "\n"
                                elif character == "t" and (characternum-ignore) <= 1:
                                    result += "\t"
                                elif inside:
                                    result += character
                                elif first == "" and (character == "'" or character == "\""):
                                    first = character
                                    inside = True
                                elif first != "" and character == "\n":
                                    print(bcolors.BackBBlack+bcolors.Red+">>> ERROR: STRING MISSING QUOTE ON LINE #"+str(linenum)+bcolors.Reset)
                                    error = True
                                    break
                            print(result[:len(result)])
                        elif line.startswith("assume f") or line.startswith("assume i"):
                            time.sleep(variables[line[7:]]-1)
                        elif line.startswith("assume s"):
                            # PRINT STRING VAR
                            characternum = 0
                            variablename = ""
                            for character in line:
                                characternum += 1
                                if character == "\n":
                                    continue
                                elif characternum > 7:
                                    variablename += character
                            while variablename.endswith("\n"):
                                variablename = variablename[:len(variablename)]
                            print(variables[variablename])
                        elif line.startswith("assume b"):
                            continue
                        else:
                            try:
                                time.sleep(int(line[7:]))
                            except ValueError:
                                # ERROR
                                print(bcolors.BackBBlack+bcolors.Red+">>> ERROR: UNKNOWN LINE FOR LINE #"+str(linenum)+bcolors.Reset)
                                break
                    else:
                        if debug:
                            print(bcolors.BackBBlack+bcolors.Blue+">>> Skipping line #"+str(linenum)+bcolors.Reset)
                            print(bcolors.BackBBlack+bcolors.Blue+"["+line+"]"+bcolors.Reset)
        except KeyError:
            print(bcolors.BackBBlack+bcolors.Red+">>> ERROR: UNDEFINED VARIABLE ON LINE #"+str(linenum)+bcolors.Reset)
        except FileNotFoundError:
            print(bcolors.BackBBlack+bcolors.Red+">>> ERROR: FILE ["+str(filepath)+"] NOT FOUND."+bcolors.Reset)
        except KeyboardInterrupt:
            print(bcolors.BackBBlack+bcolors.Yellow+">>> FILE STOPPED WITH CTRL+C"+bcolors.Reset)
            if debug:
                showvars()
                showlines()
    else:
        print(bcolors.BackBBlack+bcolors.Red+">>> ERROR: NOT AN ASSUMPTION FILE."+bcolors.Reset)
    print(bcolors.BackBBlack+bcolors.Green+">>> File ended.\n"+bcolors.Reset)
input(bcolors.BackBBlack+bcolors.Magenta+">>> Press enter to close"+bcolors.Reset)
