class Car:
    def __init__(self, color):
        self.color = color

    def __repr__(self):
        return "{}".format(self.color)

myCar = Car("white")

print(myCar)