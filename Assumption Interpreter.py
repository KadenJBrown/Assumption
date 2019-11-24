import os
import time

debug = False

# s - string - "2"
# i - int - 2
# f - float - 2.0
# b - bool - True False
## l - list - []
## d - dict - {}
## f - function - call()
## b - branch - if else
## g - gate - or and

def stringtocontent(x):
    characternum = 0
    new = ""
    ignore = False
    for character in x:
        characternum += 1
        if character == "n" and ignore:
            new += "\n"
            ignore = False
            continue
        ignore = False
        if character == "\n":
            continue
        elif character == "\\":
            ignore = True
        elif characternum > 1 and characternum < len(x):
            new += character
    return new

def isnumber(x):
    isnumber = True
    for character in str(x):
        if character == "\n":
            continue
        for number in "-1234567890.":
            if character == number:
                break
            elif number == ".":
                isnumber = False
            else:
                continue
    return isnumber

filepath = (os.getcwd()+"\Example.ass")

print(">>> Running from "+str(os.getcwd()))

InUse = True

while True:
    command = input(">>> What file do you want to interpret?\n> ")
    if command.startswith("%cd%"):
        filepath = os.getcwd()
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
    else:
        filepath = command
    print(">>> File path: " + filepath + "\n\n>>> Interpreting file...")
    if filepath.endswith(".ass"):
        with open(filepath) as fp:
            try:
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
                                print(">>> Found line:\n["+waitfor+"]")
                        waitfor = ""
                        if "input" in line:
                            invar = input("> ")
                            invar2 = ""
                            for character in invar:
                                if character != "\n" and character != "\t":
                                    invar2 += character
                            newinput = ("\""+invar2+"\"")
                            line = (line[:line.find("input")]+newinput+line[line.find("input")+7:])
                        #print(line)
                        #everyline[linenum-1] = line
                        if line == "\n" or line == "":
                            continue
                        elif not line.startswith("assume"):
                            # ASSUME MISSING ERROR
                            print(">>> ERROR: COMMAND MISSING ON LINE #"+str(linenum))
                            break
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
                                    if ignore and character == "n":
                                        if before:
                                            arg1 += "\\n"
                                        else:
                                            arg2 += "\\n"
                                        ignore = False
                                        continue
                                    if character == quote and ignore == False:
                                        inside = False
                                    ignore = False
                                    if character == "+":
                                        quote = ""
                                        before = False
                                        if arg1 == "":
                                            print(">>> ERROR: ARGUMENT #1 TO ADD/CONCATENATE MISSING ON LINE #"+str(linenum))
                                            error = True
                                            break
                                    elif character == "#":
                                        break
                                    elif quote == "" and (character == "'" or character == "\""):
                                        quote = character
                                        inside = True
                                        if before:
                                            arg1 += character
                                        else:
                                            arg2 += character
                                    elif character == "\\":
                                        ignore = True
                                    elif inside or (character != " " and character != "\t"):
                                        if before:
                                            arg1 += character
                                        else:
                                            arg2 += character
                            if arg2.endswith("\n"):
                                    arg2 = arg2[:-1]
                            if arg2 == "":
                                print(">>> ERROR: ARGUMENT #2 TO ADD/CONCATENATE MISSING ON LINE #"+str(linenum))
                                break
                            if (arg1.endswith("\"") and arg1.startswith("\"")) or (arg1.endswith("'") and arg1.startswith("'")):
                                # ARG 1 = STRING RAW
                                arg1 = stringtocontent(arg1)
                                if (arg2.endswith("\"") and arg2.startswith("\"")) or (arg2.endswith("'") and arg2.startswith("'")):
                                    # ARG 2 = STRING RAW
                                    arg2 = stringtocontent(arg2)
                                elif "'" in arg2 or "\"" in arg2:
                                    # ARG 2 STRING ERROR
                                    print(">>> ERROR: STRING MISSING QUOTE ON LINE #"+str(linenum))
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
                                print(">>> ERROR: STRING MISSING QUOTE ON LINE #"+str(linenum))
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
                                    print(">>> ERROR: STRING MISSING QUOTE ON LINE #"+str(linenum))
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
                                    print(">>> ERROR: CAN'T ADD ARG2 TO INTEGER OF ARG1 ON LINE #"+str(linenum))
                                    break
                            if debug:
                                print(">>> ARG1 of line #"+str(linenum)+" is "+str(arg1))
                                print(">>> ARG2 of line #"+str(linenum)+" is "+str(arg2))
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
                                            print(">>> ERROR: MISSING ARGUMENT #1 IN CONVERSION ON LINE #"+str(linenum))
                                            error = True
                                            break
                                        before = False
                                    elif before:
                                        old += character
                                    else:
                                        new += character
                            if new == "":
                                print(">>> ERROR: MISSING ARGUMENT #2 ON LINE #"+str(linenum))
                                break
                            else:
                                try:
                                    old = variables[old]
                                    if new.startswith("s"):
                                        variables[new] = str(old)
                                    elif new.startswith("i"):
                                        variables[new] = int(old)
                                    elif new.startswith("f"):
                                        variables[new] = float(old)
                                    elif new.startswith("b"):
                                        variables[new] = bool(old)
                                    else:
                                        print(">>> ERROR: UNKNOWN TYPE ON LINE #"+str(linenum))
                                        break
                                except ValueError:
                                    print(">>> ERROR: INVALID CONVERSION ON LINE #"+str(linenum))
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
                                            print(">>> ERROR: ARGUMENT #1 MISSING ON LINE #"+str(linenum))
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
                                            print(">>> ERROR: ARGUMENT #2 MISSING ON LINE #"+str(linenum))
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
                                        print(">>> ERROR: UNEXPECTED SPACE ON LINE #"+str(linenum))
                                        error = True
                                        break
                                    elif character == "\n":
                                        if branch == "":
                                            print(">>> ERROR: BRANCH MISSING ON LINE #"+str(linenum))
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
                                print(">>> ERROR: STRING MISSING QUOTE ON LINE #"+str(linenum))
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
                                        print(">>> ERROR: STRING MISSING QUOTE ON LINE #"+str(linenum))
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
                                    print(">>> Waiting for "+str(waitfor)+" because "+str(arg1)+" and "+str(arg2)+" are equal.")
                            else:
                                waitfor = ""
                                if debug:
                                    print(">>> Not waiting for anything because "+str(arg1)+" and "+str(arg2)+" aren't equal.")
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
                                        print(">>> ERROR: VARIABLE TO SET MISSING ON LINE #"+str(linenum))
                                        error = True
                                        break
                                elif characternum > 7 and character != " " and character != "\t" and before == True:
                                    variablename += character
                                elif ((character != " " and character != "\t") or inside) and before == False:
                                    value += character
                            if value == "" and not variablename.startswith("s"):
                                print(">>> ERROR: VALUE TO SET VARIABLE TO MISSING ON LINE #"+str(linenum))
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
                                    print(">>> ERROR: VARIABLE SAYS VALUE IS A STRING, BUT IT'S NOT A STRING AT LINE #"+str(linenum))
                                    break
                            elif not variablename.startswith("l") and not variablename.startswith("d"):
                                print(">>> ERROR: TYPE OF VARIABLE UNKNOWN ON LINE #"+str(linenum))
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
                                    print(">>> ERROR: STRING MISSING QUOTE ON LINE #"+str(linenum))
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
                                print(">>> ERROR: UNKNOWN LINE FOR LINE #"+str(linenum))
                                break
                    else:
                        if debug:
                            print(">>> Skipping line #"+str(linenum))
                            print("["+line+"]")
            except KeyError:
                print(">>> ERROR: KeyError ON LINE #"+str(linenum))
    else:
        print(">>> ERROR: NOT AN ASSUMPTION FILE.")
    print(">>> File ended.\n")
