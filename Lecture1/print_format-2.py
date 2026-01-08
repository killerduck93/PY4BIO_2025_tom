# left align
print("Yes, {:10s} is my name.".format("Luka"))
print("Yes, {:<10s} is my name.".format("Luka"))
  
myName="Khan"

# left align
print("Yes, {:<10s} is my name.".format(myName))
# center align
print("Yes, {:^10s} is my name.".format(myName))
# right align
print("Yes, {:>10s} is my name.".format(myName))
