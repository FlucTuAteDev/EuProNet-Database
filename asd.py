class Car:
    def __init__(self, color):
        self.color = color

    def __repr__(self):
        return "{}".format(self.color)

myCar = Car("white")
myCar2 = Car("black")
print(myCar, myCar2)