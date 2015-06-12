developmentSet = []
developedSet = []

with open('development.set', 'r') as in_test:
    with open('developed.set', 'r') as in_dev:
        for line in in_test:
            developmentSet.append(line)
        
        for line in in_dev:
            developedSet.append(line)
        
        index = 0
        for item in developmentSet:
            split = item.split()
            equal = developedSet[index].split()
            print(split, equal)
            if (split[0] != equal[0]):
                developmentSet.pop(index)
            
            with open('developmentfix.set', 'a') as fixedfile:
                fixedfile.write(item)
            index += 1
            
            
        #columns = line.split()
        #if len(columns) > 5:
        #    with open('developmentfix.set', 'a') as fixedfile:
        #        fixedfile.write(line)


print("Done")
