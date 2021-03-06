from field.field import Field
import numpy as np

class MainField(Field):
    def __init__(self, X, Y, food_positions = None, nest_position = None):
        super().__init__(X, Y)
        self.food_field = MainField.FoodField(X, Y, food_positions)
        self.nest_field = MainField.NestField(X, Y, nest_position)
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
        def __init__(self, X, Y, food_positions):
            super().__init__(X, Y)

            if not bool(food_positions):
                food_positions = [super().shuffle_position()]

            self.food_position_size = len(food_positions)
            self.food_positions = food_positions

        def __assign_food_positions(self):
            food_positions = []
            for i in range(self.food_position_size):
                food_positions.append(super().shuffle_position())

            return food_positions


    class NestField(Field):
        def __init__(self, X, Y, nest_position):
            super().__init__(X, Y)

            if not bool(nest_position):
                nest_position = super().shuffle_position()

            self.nest_position = nest_position
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

        def upleft_average_quantity(self, x, y):
            if self.is_top_end_line(x) or self.is_left_end_line(y):
                return 0

            return (self.quantity(x, y - 1) + self.quantity(x - 1, y - 1) + self.quantity(x - 1, y)) / 3.0

        def upright_average_quantity(self, x, y):
            if self.is_top_end_line(x) or self.is_right_end_line(y):
                return 0

            return (self.quantity(x, y + 1) + self.quantity(x - 1, y + 1) + self.quantity(x - 1, y)) / 3.0

        def downright_average_quantity(self, x, y):
            if self.is_bottom_end_line(x) or self.is_right_end_line(y):
                return 0

            return (self.quantity(x, y + 1) + self.quantity(x + 1, y + 1) + self.quantity(x + 1, y)) / 3.0

        def downleft_average_quantity(self, x, y):
            if self.is_bottom_end_line(x) or self.is_left_end_line(y):
                return 0

            return (self.quantity(x, y - 1) + self.quantity(x + 1, y - 1) + self.quantity(x + 1, y)) / 3.0
