class Celsius:
    def __get__(self, instance, owner):
        return (5. / 9) * (instance.fahrenheit - 32)

    def __set__(self, instance, value):
        instance.fahrenheit = (9. / 5) * value + 32


class Temperature:
    celsius = Celsius()

    def __init__(self, temp=0):
        self.fahrenheit = temp
