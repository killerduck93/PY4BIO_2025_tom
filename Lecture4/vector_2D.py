class Vector2D: 
    def __init__ (self, x, y): 
        self.x, self.y = x, y

    def size (self):
        return (self.x ** 2 + self.y ** 2) ** 0.5


v = Vector2D(3, 4) # Make instance.