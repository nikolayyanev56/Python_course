class Vector:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def lenght(self):
        return (self.x**2 + self.y**2)**0.5

ab = Vector(5,5)
print(ab.x)
print(ab.y)
print(ab.lenght())