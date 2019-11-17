import os

# s - string - "2"
# i - int - 2
# f - float - 2.0
# b - bool - True False
## l - list - []
## d - dict - {}
## f - function - call()
## b - branch - if else
## g - gate - or and

filepath = (os.getcwd()+"\Example.ass")

print(">>> Running from "+str(os.getcwd()))

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
    elif command != "same" and command != "last" and command != "":
        filepath = command
    print(">>> File path: " + filepath + "\n\n>>> Interpreting file...")
    if filepath.endswith(".ass"):
        with open(filepath) as fp:
            variables = {}
            linenum = 0
            error = False
            for line in fp.readlines():
                linenum += 1
                if line.startswith("#"):
                    # COMMENT
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
                            elif inside or character != " ":
                                if before:
                                    arg1 += character
                                else:
                                    arg2 += character
                    if arg2.endswith("\n"):
                            arg2 = arg2[:-1]
                    if arg2 == "":
                        print(">>> ERROR: ARGUMENT #2 TO ADD/CONCATENATE MISSING ON LINE #"+str(linenum))
                        break
                    elif (arg1.endswith("\"") and arg1.startswith("\"")) or (arg1.endswith("'") and arg1.startswith("'")):
                        # ARG 1 = STRING RAW
                        characternum = 0
                        new = ""
                        for character in arg1:
                            characternum += 1
                            if character == "\n":
                                continue
                            elif characternum > 1 and characternum < len(arg1):
                                new += character
                        arg1 = new
                        if (arg2.endswith("\"") and arg2.startswith("\"")) or (arg2.endswith("'") and arg2.startswith("'")):
                            # ARG 2 = STRING RAW
                            characternum = 0
                            new = ""
                            for character in arg2:
                                characternum += 1
                                if character == "\n":
                                    continue
                                elif characternum > 1 and characternum < len(arg2):
                                    new += character
                            arg2 = new
                        elif "'" in arg2 or "\"" in arg2:
                            # ARG 2 STRING ERROR
                            print(">>> ERROR: STRING MISSING QUOTE ON LINE #"+str(linenum))
                            break
                        else:
                            isnumber = True
                            for character in arg2:
                                if character == "\n":
                                    continue
                                for number in "1234567890.":
                                    if character == number:
                                        break
                                    elif number == "0":
                                        isnumber = False
                                    else:
                                        continue
                            if isnumber:
                                # ARG 2 = INT/FLOAT RAW
                                arg2 = str(arg2)
                            else:
                                arg2 = str(variables[arg2])
                        print(arg1 + arg2)
                    elif "'" in arg1 or "\"" in arg1:
                        # ARG 1 = STRING ERROR
                        print(">>> ERROR: STRING MISSING QUOTE ON LINE #"+str(linenum))
                        break
                    elif arg1.startswith("s"):
                        # ARG 1 = STRING VAR
                        if (arg2.endswith("\"") and arg2.startswith("\"")) or (arg2.endswith("'") and arg2.startswith("'")):
                            # ARG 2 = STRING RAW
                            characternum = 0
                            new = ""
                            for character in arg2:
                                characternum += 1
                                if characternum > 1 and characternum < len(arg2):
                                    new += character
                            arg2 = new
                            variables[arg1] += arg2
                elif "==" in line:
                    # BRANCHES
                    section = "arg1"
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
                        elif section == "arg1":
                            if character == "=":
                                section = "arg2"
                            elif quotes = "" and (character == "'" or character == "\""):
                                quotes = character
                                inside = True
                                arg1 += character
                            elif character == quotes:
                                inside = False
                                arg1 += character
                            elif inside or character != " ":
                                arg1 += character
                        elif section == "arg2":
                            if character == "=":
                                continue
                            elif character == ",":
                                section = "branch"
                            elif quotes = "" and (character == "'" or character == "\""):
                                quotes = character
                                inside = True
                                arg2 += character
                            elif character == quotes:
                                inside = False
                                arg2 += character
                            elif inside or character != " ":
                                arg2 += character
                        else:
                            
                    
                elif "=" in line and not "==" in line:
                    # SETTING VARIABLES
                    before = True
                    characternum = 0
                    variablename = ""
                    value = ""
                    quotecount = 0
                    quotetype = ""
                    for character in line:
                        characternum += 1
                        if character == "#":
                            break
                        if character == "\n":
                            continue
                        elif character == quotetype or (quotetype == "" and (character == "\"" or character == "'")):
                            quotetype = character
                            quotecount += 1
                            continue
                        elif character == "=":
                            before = False
                            if variablename == "":
                                print(">>> ERROR: VARIABLE TO SET MISSING ON LINE #"+str(linenum))
                                error = True
                                break
                        elif characternum > 7 and character != " " and before == True:
                            variablename += character
                        elif character != " " and before == False:
                            value += character
                    if value == "":
                        print(">>> ERROR: VALUE TO SET VARIABLE TO MISSING ON LINE #"+str(linenum))
                        error = True
                        break
                    elif variablename.startswith("i"):
                        value = int(value)
                    elif variablename.startswith("f"):
                        value = float(value)
                    elif variablename.startswith("b"):
                        value = bool(value)
                    elif variablename.startswith("s"):
                        if quotecount != 2:
                            print(">>> ERROR: VARIABLE SAYS VALUE IS A STRING, NOT A STRING AT LINE #"+str(linenum))
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
                    ignore = False
                    for character in line:
                        if ignore == False and character == first:
                            break
                        ignore = False
                        if character == "\\":
                            ignore = True 
                        elif inside:
                            result += character
                        elif first == "" and (character == "'" or character == "\""):
                            first = character
                            inside = True
                        elif first != "" and character == "\n":
                            print(">>> ERROR: STRING MISSING QUOTE ON LINE #"+str(linenum))
                            error = True
                            break
                    print(result)
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
                        variablename = variablename[:-1]
                    print(variables[variablename])
                else:
                    # PASS OR ERROR
                    line_no_comment = ""
                    for character in line:
                        if character == "#":
                            break
                        else:
                            line_no_comment += character
                    if line_no_comment == "assume":
                        continue
                    else:
                        print(">>> ERROR: UNKNOWN LINE FOR LINE #"+str(linenum))
                        break
                if error:
                    # CLOSE PROGRAM ON ERROR
                    break
    else:
        print(">>> ERROR: NOT AN ASSUMPTION FILE.")
    print(">>> File ended.\n")
