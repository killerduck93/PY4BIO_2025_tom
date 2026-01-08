# class definition
class Car: 
    def __init__(self, manufacturer, color, size, age):
        num_of_wheels = 4
        self.manufacturer = manufacturer
        self.color = color
        self.size = size
        self.age = age

    def run(self):
        print("Brummmmm!")

    def stop(self):
        print("Eeeeeek!")

# class instances
alfa = Car("Alfa Romeo", "red", "medium", None)
mini = Car("Ford", "blue", "small", 3)

mini.run()
print(mini.color)
mini.age += 1
print(mini.age)
