class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(f"{self.name} is eating.")


class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed

    def bark(self):
        print("Woof! Woof!")


class Cat(Animal):
    def purr(self):
        print("Meow...")

    def eat(self):
        super().eat()
        print("But the cat is eating very quietly.")
