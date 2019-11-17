# i - int - 1
# f - float - 1.0
# b - bool - True False
## l - list - []
## d - dict - {}
## f - function - call()
## s - scope - if else
## g - gate - or and

while True:
    filepath = input(">>> What file do you want to interpret?\n> ")
    print("\n>>> Interpreting file: " + filepath)
    if filepath.endswith(".ass"):
        with open(filepath) as fp:
            variables = {}
            linenum = 0
            error = False
            for line in fp.readlines():
                linenum += 1
                if not line.startswith("assume"):
                    # ASSUME MISSING ERROR
                    print(">>> ERROR: COMMAND MISSING ON LINE #"+str(linenum))
                    break
                elif "+" in line:
                    # 1 + 2 = 1 with a 2 at the end
                    arg1 = ""
                    arg2 = ""
                    
                elif "=" in line and not "==" in line:
                    # SETTING VARIABLES
                    before = True
                    characternum = 0
                    variablename = ""
                    value = ""
                    quotecount = 0
                    for character in line:
                        characternum += 1
                        if character == "#":
                            break
                        elif character == "\"" or character == "'":
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
                    print(variables[variablename])
                else:
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
                    break
    else:
        print(">>> ERROR: NOT AN ASSUMPTION FILE.")
    print(">>> File ended.\n")
