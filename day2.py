DAY = 2

def read_input():
    inputs = []
    with open(f"day{DAY}.txt", "r") as file:
        for line in file:
            line = line.strip()
            all_intervals= line.split(",")
            for interval in all_intervals:
                interval = [int(i) for i in interval.split("-")]
                inputs.append(interval)
    
    return inputs

def isRepeated(string):
    if len(string)%2 == 1:
        return False
    
    mid = len(string)//2
    if string[:mid] == string[mid:]:
        return True
    
    return False

def isInvalid(string):
    for i in range(1, len(string)):
        subString = string[:i]
        if len(string) % len(subString) != 0: continue

        desiredCount = len(string) // len(subString)

        if string.count(subString) == desiredCount:
            return True
        
    return False

def parta():
    intervals = read_input()
    res = 0
    for start, end in intervals:
        for i in range(start, end+1):
            if isRepeated(str(i)): res += i

    return res

def partb():
    intervals = read_input()
    res = 0
    for start, end in intervals:
        for i in range(start, end+1):
            if isInvalid(str(i)): res += i

    return res

print(parta())
print(partb())