from dataclasses import dataclass


@dataclass(frozen=True)
class Car:
    new: bool
    name: str
    color: str
    year: int
    price: float

    def __repr__(self) -> str:
        return f"Car(new={self.new}, name={self.name}, color={self.color}, year={self.year}, price={self.price})"

    def __str__(self) -> str:
        return f"{self.name} ({self.year}) - {self.color}, {'New' if self.new else 'Used'}, ${self.price}"


@dataclass
class Garage:
    name: str
    cars: list[Car]  # use the previous created class

    def __repr__(self) -> str:
        return f"Garage(name={self.name!r}, cars={self.cars!r})"  # !r calls repr

    def __str__(self) -> str:
        res = f"Garage name: {self.name}\nCars:\n"
        for car in self.cars:
            res += f"  {car}\n"  # we use the __str__ reprensentation of the Car class
        return res

    def __sizeof__(self) -> int:
        return len(self.cars)


colors = ["Blue", "Red", "Green", "Yellow"]
years = [1922, 2021, 2004, 2027]
names = ["Toyota", "Honda", "Ford", "Chevrolet"]
prices = [10000.0, 20000.0, 30000.0, 40000.0]

# generate 10 cars
cars = []
for i in range(10):
    cars.append(
        Car(
            new=True,
            name=names[i % 4],
            color=colors[i % 4],
            year=years[i % 4],
            price=prices[i % 4],
        )
    )

# create a garage
garage = Garage(name="My Garage", cars=cars)

print(garage)
print(f"Number of cars in the garage: {garage.__sizeof__()}")
