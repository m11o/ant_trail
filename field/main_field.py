from field.field import Field
import numpy as np

class MainField(Field):
    def __init__(self, X, Y):
        super().__init__(X, Y)
        self.food_field = MainField.FoodField(X, Y)
        self.nest_field = MainField.NestField(X, Y)
        self.pheromones_field = MainField.PheromonesField(X, Y)

        self.__init_field()

    def __init_field(self):
        nest_position = self.nest_field.nest_position
        food_positions = self.food_field.food_positions

        self.field[nest_position[0]][nest_position[1]] = 0.6
        for food_position in food_positions:
            self.field[food_position[0]][food_position[1]] = 0.3

    def pheromone_quantity(self, x, y):
        return self.pheromones_field.quantity(x, y)

    def update_field_value(self, before_ant, after_ant):
        if bool(before_ant):
            self.field[before_ant.x][before_ant.y] = 0

        self.field[after_ant.x][after_ant.y] = 1
        self.__init_field()


    class FoodField(Field):
        def __init__(self, X, Y):
            super().__init__(X, Y)

            self.food_position_size = 1
            self.food_positions = self.__assign_food_positions()

        def __assign_food_positions(self):
            food_positions = []
            for i in range(self.food_position_size):
                food_positions.append(super().shuffle_position())

            return food_positions


    class NestField(Field):
        def __init__(self, X, Y):
            super().__init__(X, Y)

            self.nest_position = super().shuffle_position()
            self.__assign_nest()

        def __assign_nest(self):
            nest_position_x = self.nest_position[0]
            nest_position_y = self.nest_position[1]

            self.field[nest_position_x][nest_position_y] = 1


    class PheromonesField(Field):
        def __init__(self, X, Y):
            super().__init__(X, Y)
            self.field = np.zeros((X, Y), dtype=object)

        def has_pheromone(self, x, y):
            return bool(self.field[x][y])

        def quantity(self, x, y):
            if (not self.has_pheromone(x, y)) or self.field[x][y].is_empty():
                return 0

            return self.field[x][y].quantity
