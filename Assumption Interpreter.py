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
                    print(">>> ERROR: COMMAND MISSING ON LINE #"+str(linenum))
                    break
                elif "=" in line and not "==" in line:
                    before = True
                    characternum = 0
                    variablename = ""
                    value = ""
                    for character in line:
                        characternum += 1
                        if character == "=":
                            before = False
                            if variablename == "":
                                print(">>> ERROR: VARIABLE TO SET MISSING ON LINE #"+str(linenum))
                                error = True
                                break
                        elif characternum > 7 and character != " " and before == True:
                            variablename += character
                        elif character != " " and before == False:
                            value += character
                        elif character == "#"
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
                    elif variablename.startswith("l"):
                        # LIST
                    elif variablename.startswith("d"):
                        # DICTIONARY
                    elif not variablename.startswith("s"):
                        print(">>> ERROR: TYPE OF VARIABLE UNKNOWN ON LINE #"+str(linenum))
                        break
                elif line.startswith("assume '") or line.startswith("assume \""):
                    inside = False
                    result = ""
                    first = ""
                    for character in line:
                        if character == first:
                            break
                        elif inside:
                            result += character
                        elif first == "" and (character == "'" or character == "\""):
                            first = character
                            inside = True
                    print(result)
                if error:
                    break
    else:
        print(">>> ERROR: NOT AN ASSUMPTION FILE.")
    print(">>> File ended.\n")
