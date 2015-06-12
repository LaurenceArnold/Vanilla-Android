with open('developed.set', 'r') as in_f:
    for line in in_f:
        newLine = ""
        cols = line.split()
        if len(cols) > 6:
            word = cols[4]
            if cols[6] == "ENT":
                if word != word.title():
                    print(line)
                    cols.pop(7)
                    cols.pop(6)
                    newLine = ' '.join(cols)
                    
        with open('developedfix.set', 'a') as fixedfile:
            if(newLine):
                fixedfile.write(newLine)
            else:
                fixedfile.write(line)
print("Done")
