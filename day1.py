DAY = 1

def read_input():
    inputs = []
    with open(f"day{DAY}.txt", "r") as file:
        for line in file:
            line = line.strip()
            inputs.append(line)
    
    return inputs

def parta():
    zero_count = 0
    state = 50
    inputs = read_input()

    for inp in inputs:
        direction = inp[0]
        count = int(inp[1:])
        if direction == "L": count *= -1

        state = (state+count)%100
        if state == 0:
            zero_count += 1

    return zero_count

def partb():
    zero_count = 0
    state = 50
    inputs = read_input()

    for inp in inputs:
        direction = inp[0]
        count = int(inp[1:])
        if direction == "L": count *= -1

        flag = False
        previous_state = state
        state = state+count

        # immediately just add 1 and move on
        if state == 0 and previous_state != 0:
            zero_count += 1
            continue

        # dealing with overflows in the positive direction
        if state >= 100:
            zero_count += state//100
            state %= 100
        
        # now dealing with the negative ones (some edge cases)
        elif state <= -100:
            zero_count += abs(state)//100
            state = -(abs(state)%100)
            flag = True

        if state < 0:
            zero_count += 1
            state += 100
            flag = True

        if flag and previous_state == 0: zero_count -= 1

        if flag and state == 0: zero_count += 1


    return zero_count

print(parta())
print(partb())