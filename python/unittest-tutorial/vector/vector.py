class Vector:
    def __init__(self, x: float, y: float):
        if not isinstance(x, (int, float)):
            raise ValueError("x must be a number")
        if not isinstance(y, (int, float)):
            raise ValueError("y must be a number")
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Vector):
            return False
        return self.x == value.x and self.y == value.y

    def __str__(self):
        return f"({self.x}, {self.y})"
