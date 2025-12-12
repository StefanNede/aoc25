DAY = 5

def read_input():
    intervals = []
    flag = False
    ingredients = []

    with open(f"day{DAY}.txt", "r") as file:
        for line in file:
            line = line.strip()
            if line == "":
                flag = True
                continue

            if flag:
                ingredients.append(int(line))
            else:
                intervals.append([int(x) for x in line.split("-")])

    return intervals, ingredients

def parta():
    intervals, ingredients = read_input()
    count = 0
    intervals.sort(key = lambda x : x[0])
    ingredients.sort()
    intervalIndex = 0

    for ingredient in ingredients:
        while intervalIndex < len(intervals):
            start, end = intervals[intervalIndex]
            if ingredient < start:
                break
            elif ingredient >= start and ingredient <= end:
                count += 1
                break
            else:
                intervalIndex += 1

    return count

def merge(intervals):
    intervals.sort()
    i = 0
    while True:
        if i >= len(intervals) -1: break
        first = intervals[i]
        second = intervals[i+1]
        x1,y1 = first
        x2,y2 = second
        if y1 >= x2:
            # overlap so merge
            intervals[i] = [x1, max(y1,y2)]
            intervals = intervals[:i+1] + intervals[i+2:]
        else:
            i += 1
    return intervals

def partb():
    # just merge intervals and count
    intervals, _ = read_input()
    count = 0
    intervals = merge(intervals)

    count = sum([end-start+1 for start,end in intervals])

    return count

print(parta())
print(partb())