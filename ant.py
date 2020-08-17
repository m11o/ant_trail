import random
import copy

from enums.ant_mode_enum import AntModeEnum
from enums.ant_direction_enum import AntDirectionEnum
from probs.returnee_probs_service import ReturneeProbsService
from probs.searcher_probs_service import SearcherProbsService
from probs.servant_probs_service import ServantProbsService
from pheromone import Pheromone

class Ant:
    def __init__(self, x, y, field_X, field_Y):
        self.x = x
        self.y = y
        self.field_X = field_X
        self.field_Y = field_Y
        self.mode = AntModeEnum.Searcher
        self.direction = random.choice(list(AntDirectionEnum))

    @classmethod
    def generate_ants(cls, amount, field):
        ants = []
        for i in range(amount):
            x = random.randrange(0, field.X)
            y = random.randrange(0, field.Y)

            ant = cls(x, y, field.X, field.Y)
            ants.append(ant)
            field.update_field_value(None, ant)

        return ants

    def is_searcher(self):
        return self.mode is AntModeEnum.Searcher

    def is_returnee(self):
        return self.mode is AntModeEnum.Returnee

    def is_servant(self):
        return self.mode is AntModeEnum.Servant

    def is_upleft(self):
        return self.direction is AntDirectionEnum.UpLeft

    def is_upright(self):
        return self.direction is AntDirectionEnum.UpRight

    def is_downleft(self):
        return self.direction is AntDirectionEnum.DownLeft

    def is_downright(self):
        return self.direction is AntDirectionEnum.DownRight

    def drop_pheromone(self, field):
        if not self.is_returnee():
            return

        pheromone = None
        if field.pheromones_field.has_pheromone(self.x, self.y):
            pheromone = field.pheromones_field.field[self.x][self.y]
        else:
            pheromone = Pheromone()

        pheromone.increase()
        field.pheromones_field.field[self.x][self.y] = pheromone

    def move(self, field):
        before_ant = copy.copy(self)

        if self.is_line_end():
            self.change_direction()
            return

        prob = self.__calc_prob(field)
        next_direction = self.next_move_direction(prob)
        next_position = []
        if next_direction == 0:
            next_position = self.next_left_position()
        else:
            next_position = self.next_right_position()

        self.x = next_position[0]
        self.y = next_position[1]

        self.drop_pheromone(field)
        self.change_mode(field)

        field.update_field_value(before_ant, self)

    def next_move_direction(self, prob):
        left_amount = [0] * int(prob[0] * 1000)
        right_amount = [1] * int(prob[1] * 1000)

        prob_amount = left_amount + right_amount
        return random.choice(prob_amount)

    def __calc_prob(self, field):
        if self.is_searcher():
            return SearcherProbsService.get_instance(self, field).calc()
        elif self.is_returnee():
            return ReturneeProbsService.get_instance(self, field).calc()
        elif self.is_servant():
            return ServantProbsService.get_instance(self, field).calc()

    def next_positions(self):
        if self.is_line_end():
            return []

        next_x = self.x - 1 if self.is_upleft() or self.is_upright() else self.x + 1
        next_y = self.y + 1 if self.is_upright() or self.is_downright() else self.y - 1

        return [[next_x, self.y], [self.x, next_y]]

    def next_left_position(self):
        next_positions = self.next_positions()

        if self.is_upleft() or self.is_downright():
            return next_positions[0]
        else:
            return next_positions[1]

    def next_right_position(self):
        next_positions = self.next_positions()

        if self.is_upleft() or self.is_downright():
            return next_positions[1]
        else:
            return next_positions[0]

    def change_direction(self, direction = None):
        if bool(direction):
            self.direction = direction
            return

        if self.is_upleft():
            if self.is_top_end_line() and self.is_left_end_line():
                self.direction = AntDirectionEnum.DownRight
            elif self.is_top_end_line():
                self.direction = AntDirectionEnum.DownLeft
            elif self.is_left_end_line():
                self.direction = AntDirectionEnum.UpRight
            else:
                self.direction = AntDirectionEnum.DownRight
        elif self.is_upright():
            if self.is_top_end_line() and self.is_right_end_line():
                self.direction = AntDirectionEnum.DownLeft
            elif self.is_top_end_line():
                self.direction = AntDirectionEnum.DownRight
            elif self.is_right_end_line():
                self.direction = AntDirectionEnum.UpLeft
            else:
                self.direction = AntDirectionEnum.DownLeft
        elif self.is_downright():
            if self.is_bottom_end_line() and self.is_right_end_line():
                self.direction = AntDirectionEnum.UpLeft
            elif self.is_bottom_end_line():
                self.direction = AntDirectionEnum.UpRight
            elif self.is_right_end_line():
                self.direction = AntDirectionEnum.DownLeft
            else:
                self.direction = AntDirectionEnum.UpLeft
        elif self.is_downleft():
            if self.is_bottom_end_line() and self.is_left_end_line():
                self.direction = AntDirectionEnum.UpRight
            elif self.is_bottom_end_line():
                self.direction = AntDirectionEnum.UpLeft
            elif self.is_left_end_line():
                self.direction = AntDirectionEnum.DownRight
            else:
                self.direction = AntDirectionEnum.UpRight

    def is_left_end_line(self):
        return self.y == 0

    def is_right_end_line(self):
        return self.y == (self.field_Y - 1)

    def is_top_end_line(self):
        return self.x == 0

    def is_bottom_end_line(self):
        return self.x == (self.field_X - 1)

    def is_line_end(self):
        return (self.is_top_end_line() and (self.is_upleft() or self.is_upright())) or (
                    self.is_left_end_line() and (self.is_upleft() or self.is_downleft())) or (
                           self.is_bottom_end_line() and (self.is_downleft() or self.is_downright())) or (
                           self.is_right_end_line() and (self.is_upright() or self.is_downright()))

    def change_mode(self, field):
        is_on_food = self.is_on_food(field)
        is_on_nest = self.is_on_nest(field)
        is_on_pheromone = self.is_on_pheromone(field)

        if self.is_returnee() and is_on_nest:
            self.mode = AntModeEnum.Servant
            self.change_direction()
            return
        elif self.is_returnee() and not is_on_nest:
            self.change_direction(self.change_home_direction(field))
            return
        elif self.is_searcher() and is_on_pheromone:
            self.change_thin_pheromene_direction(field)
            self.mode = AntModeEnum.Servant
            return
        elif self.is_searcher() and is_on_food:
            self.mode = AntModeEnum.Returnee
            self.change_direction(self.change_home_direction(field))
            return
        elif self.is_servant() and not is_on_pheromone:
            self.mode = AntModeEnum.Searcher
            return
        elif self.is_servant() and is_on_food:
            self.mode = AntModeEnum.Returnee
            self.change_direction()
            return

    def change_thin_pheromene_direction(self, field):
        upleft_phero = 0 if self.is_top_end_line() or self.is_left_end_line() else (field.pheromone_quantity(self.x,
                                                                                                             self.y - 1) + field.pheromone_quantity(
            self.x - 1, self.y - 1) + field.pheromone_quantity(self.x - 1, self.y)) / 3
        upright_phero = 0 if self.is_top_end_line() or self.is_right_end_line() else (field.pheromone_quantity(self.x,
                                                                                                               self.y + 1) + field.pheromone_quantity(
            self.x - 1, self.y + 1) + field.pheromone_quantity(self.x - 1, self.y)) / 3
        downright_phero = 0 if self.is_bottom_end_line() or self.is_right_end_line() else (field.pheromone_quantity(
            self.x, self.y + 1) + field.pheromone_quantity(self.x + 1, self.y + 1) + field.pheromone_quantity(
            self.x + 1, self.y)) / 3
        downleft_phero = 0 if self.is_bottom_end_line() or self.is_left_end_line() else (field.pheromone_quantity(
            self.x, self.y - 1) + field.pheromone_quantity(self.x + 1, self.y - 1) + field.pheromone_quantity(
            self.x + 1, self.y)) / 3

        hash = {
            'upleft': upleft_phero,
            'upright': upright_phero,
            'downright': downright_phero,
            'downleft': downleft_phero
        }

        sorted_hash = sorted(hash.items(), key=lambda x: x[1])
        for i in sorted_hash:
            if bool(i[1]):
                if i[0] == 'upleft':
                    self.direction = AntDirectionEnum.UpLeft
                elif i[0] == 'upright':
                    self.direction = AntDirectionEnum.UpRight
                elif i[0] == 'downright':
                    self.direction = AntDirectionEnum.DownRight
                elif i[0] == 'downleft':
                    self.direction = AntDirectionEnum.DownLeft

                break

    def change_home_direction(self, field):
        nest_position = field.nest_field.nest_position
        diff_x = self.x - nest_position[0]
        diff_y = self.y - nest_position[1]

        if diff_x >= 0 and diff_y >= 0:
            return AntDirectionEnum.UpLeft
        elif diff_x >= 0 and diff_y < 0:
            return AntDirectionEnum.UpRight
        elif diff_x < 0 and diff_y >= 0:
            return AntDirectionEnum.DownLeft
        elif diff_x < 0 and diff_y < 0:
            return AntDirectionEnum.DownRight
        else:
            return None

    def is_on_nest(self, field):
        nest_position = field.nest_field.nest_position

        return nest_position[0] == self.x and nest_position[1] == self.y

    def is_on_pheromone(self, field):
        return field.pheromones_field.has_pheromone(self.x, self.y)

    def is_on_food(self, field):
        food_positions = field.food_field.food_positions

        on_food_positions = []
        for food_position in food_positions:
            on_food_positions.append(food_position[0] == self.x and food_position[1] == self.y)

        return all(on_food_positions)