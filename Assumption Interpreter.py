while True:
    filepath = input(">>> What file do you want to interpret?\n> ")
    print("\n>>> Interpreting file: " + filepath)
    if filepath.endswith(".ass"):
        with open(filepath) as fp:
            variables = {}
            linenum = 0
            for line in fp.readlines():
                linenum += 1
                if not line.startswith("assume"):
                    print(">>> ERROR: COMMAND MISSING ON LINE #"+str(linenum))
                    break
                elif "=" in line and not "==" in line:
                    before = True
                    for character in line:
                        if character == "=":
                            before = False
                        elif character != " " and before == False:
                            
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
    else:
        print(">>> ERROR: NOT AN ASSUMPTION FILE.")
    print(">>> File ended.\n")
