import math
DAY = 6

def read_input():
    inputs = []

    with open(f"day{DAY}.txt", "r") as file:
        for line in file:
            line = line.strip()
            line = line.split()
            inputs.append(line)

    return inputs

def parta():
    inputs = read_input()
    total = 0
    # transpose the inputs
    inputs = [list(i) for i in zip(*inputs)]
    
    for calc in inputs:
        operator = calc[-1]
        values = [int(i) for i in calc[:-1]]
        if operator == "*":
            total += int(math.prod(values))
        else:
            total += sum(values)

    return total

# helper function for part (b)
# takes list of numbers with spaces on different columns and reads their values in columns
def merge(lst):
    return [int("".join(list(i)).strip()) for i in zip(*lst)]

def partb():
    # modified input to put the operators at the top so i can count number of digits for column
    inputs = []
    lengths = []
    with open(f"day{DAY}.txt", "r") as file:
        for line in file:
            if "+" in line:
                # operator line
                # find lengths
                length = 1
                for i in line[1:]:
                    if i == "+" or i == "*":
                        lengths.append(length-1)
                        length = 1

                    else:
                        length += 1
                lengths.append(length-1)
                inputs.append(line.strip().split())
            
            else:
                # number line
                # go in spaces of lengths
                numbers = []
                idx = 0
                for length in lengths:
                    numbers.append(line[idx:idx+length])
                    idx += length+1
                inputs.append(numbers)

    # this is where actual part b starts
    inputs = [list(i) for i in zip(*inputs)]
    total = 0

    for calc in inputs:
        operator = calc[0]
        values = merge(calc[1:])
        if operator == "*":
            total += int(math.prod(values))
        else:
            total += sum(values)

    return total 

# print(parta())
print(partb())