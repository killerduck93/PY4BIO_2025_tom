def find_max(data):
    max = data.pop()
    for x in data:
        if x > max:
            max = x
    return max

data = [1, 5, 1, 12, 3, 4, 6]
print("Data:", data)
print("Maximum: %i" % find_max(data))
