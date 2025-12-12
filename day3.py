DAY = 3

def read_input():
    inputs = []
    with open(f"day{DAY}.txt", "r") as file:
        for line in file:
            line = line.strip()
            inputs.append(line)
    return inputs

def getJolts(string):
    max_a = 0 # number 1
    max_b = 0 # number 2

    for idx, char in enumerate(string):
        num = int(char)

        # make sure not the last character
        if num > max_a and idx != len(string)-1:
            max_a = num
            max_b = 0
        elif num > max_b:
            max_b = num

    return 10*max_a + max_b

def getJoltsAdvanced(string):
    maxes = [0] * 12

    for idx, char in enumerate(string):
        num = int(char)

        flipped = False
        for i, max_i in enumerate(maxes):
            if flipped:
                maxes[i] = 0
                continue

            if num > max_i and len(string)-idx >= 12-i:
                maxes[i] = num
                flipped = True
    
    return int("".join([str(x) for x in maxes]))

def parta():
    inputs = read_input()
    res = 0
    for inp in inputs:
        res += getJolts(inp)
    
    return res

def partb():
    inputs = read_input()
    res = 0
    for inp in inputs:
        res += getJoltsAdvanced(inp)
 
    return res

# print(parta())
print(partb())