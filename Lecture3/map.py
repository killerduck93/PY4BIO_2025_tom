print(map(lambda x: x*3, [1,2,3]))
print(filter(lambda x: x>=1.0, [1.2,0.5,0.7,1.3]))
print(filter(lambda x: x!=0, map(lambda x: x-2, [4,2,5])))
print(reduce(lambda x,y: x+y if x<=2 else x*y, (1,2,3)))
