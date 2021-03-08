from calories import temperature


class Calorie:

    """ Represents optimal calorie amount a person needs to take today. """

    def __init__(self, weight, height, age, temperature):
        self.weight = weight
        self.height = height
        self.age = age
        self.temperature = temperature

    def calculate(self):
        result = (10 * self.weight) + (6.5 * self.height) - (self.temperature * 10) + 5
        
        return result