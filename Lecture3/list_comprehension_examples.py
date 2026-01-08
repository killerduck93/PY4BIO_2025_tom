sentence = 'I like MySQL but not Python'
print([(w.lower(), len(w)) for w in sentence.split()])

generator = ((x-2)*3 for x in range(10))

generator_iterator = iter(generator)
while generator_iterator:
    try:
        my_number = next(generator_iterator)
        print(my_number)
    except StopIteration:
        break

my_numbers = (1,0,-1,6,3,-2,3,4)
my_sum = sum([x for x in my_numbers if x >0])
print('sum: ', my_sum)
