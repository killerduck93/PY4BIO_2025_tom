# Step 1: Analyze and execute the given code snippet
z = range(2, 7)
squared_values = list(map(lambda x: x**2, z))
print("Squared values:", squared_values)

# Step 2: Use filter and lambda function to show the even values in the list z
even_values = list(filter(lambda x: x % 2 == 0, z))
print("Even values:", even_values)