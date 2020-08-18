class Pheromone:
    INCREASING_QUANTITY_BY_STEP = 1.0
    DECREASING_QUANTITY_BY_STEP = 0.01
    MAX_QUANTITY = 10.0

    def __init__(self):
        self.quantity = self.INCREASING_QUANTITY_BY_STEP

    def increase(self):
        self.quantity += self.INCREASING_QUANTITY_BY_STEP

        if self.quantity >= self.MAX_QUANTITY:
            self.quantity = self.MAX_QUANTITY

    def decrease(self):
        if self.quantity <= 0:
            self.quantity = 0
            return

        self.quantity -= self.DECREASING_QUANTITY_BY_STEP

    def is_empty(self):
        return self.quantity == 0
